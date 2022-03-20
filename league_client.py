import pandas as pd
import requests
import urllib3
from leagueExceptions import *
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class leagueClient():
    _allPlayers = None
    _game_info = None
    _summoner_name = None
    _activePlayer = None
    _summoner_team = None
    _events = None
    _gameData = None
    
    def __init__(self):
        print("client started")

    def leagueClientRunning(self):
        hostname = 'https://127.0.0.1:2999/liveclientdata/allgamedata' #example
        response = os.system("ping -c 1 " + hostname)

        #and then check the response...
        if response == 0:
            return True
        else:
            return False

    def _getAllData(self):
        r = requests.get('https://127.0.0.1:2999/liveclientdata/allgamedata', verify=False)
        self._game_info = r.json()
        self._activePlayer = self._game_info['activePlayer']
        self._allPlayers = self._game_info['allPlayers']
        self._events = pd.DataFrame.from_dict(self._game_info['events'])
        self._gameData = self._game_info['gameData']
        #sett basic level information
        self._setPlayerStats()
        
        return True

    def _setPlayerStats(self):
        self._summoner_name = self._game_info['activePlayer']['summonerName']
        self._summoner_data = next(filter(lambda players: players['summonerName'] == self._summoner_name, self._game_info['allPlayers']))
        self._summoner_team = self._summoner_data['team']

    def _getPlayerStats(self):
        r = requests.get('https://127.0.0.1:2999/liveclientdata/playerlist', verify=False)
        self._player_stats = r.json()
        return True
        
    def populateData(self):
        #bring in all the data and identify the active player
        try:
            self._getAllData()
            self._getPlayerStats()
            return True
        except Exception as e:
            #pass up the exception this line isn't really needed here as its being caught and thrown up, but who s
            print(e)
            raise LeagueClientError('unable to retrieve data from league client')

    def getAllData(self):
        if(self._game_info):
            return(self._game_info)
        elif(self._getAllData()):
            #the game data is null this could possibly happen on the first call or before league client has started
            return(self._game_info)
        else:
            #there is no data, and the league client is not running
            raise LeagueClientError('unable to retrieve data from league client')

    def getPlayerData(self):
        if(self._game_info):
            return(self._player_stats)
        elif(self._getPlayerStats()):
            #the game data is null this could possibly happen on the first call or before league client has started
            return(self._player_stats)
        else:
            #there is no data, and the league client is not running
            raise LeagueClientError('unable to retrieve data from league client')

    #ALLPLAYER BASED METHODS
    def getFriendlyStats(self):
        return list(filter(lambda players: players['team'] == self._summoner_team, self._allPlayers))

    def getEnemyStats(self):
        return list(filter(lambda players: players['team'] != self._summoner_team, self._allPlayers))

    def getFriendlySummonerNames(self):
        return [x['summonerName'] for x in self.getFriendlyStats()]

    def getEnemySummonerNames(self):
        return [x['summonerName'] for x in self.getEnemyStats()]

    def get_player_kda(self, summoner_name):
        summoner_stats = list(filter(lambda players: players['summonerName'] == summoner_name, self._allPlayers))[0]
        return (summoner_stats['scores']['assists'] + summoner_stats['scores']['kills'])/max(1, summoner_stats['scores']['deaths'])

    def get_summoner_kda(self):
        return self.get_player_kda(self._summoner_name)

    def getFriendlyTeamKDA(self):
        [(x['scores']['assists'] + x['scores']['kills'])/max(1, x['scores']['deaths']) for x in self.getFriendlyStats()]

    def getEnemyTeamKDA(self):
        [(x['scores']['assists'] + x['scores']['kills'])/max(1, x['scores']['deaths']) for x in self.getEnemyStats()]

    def get_deathStreaks(self):
        last_kill = self._events[self._events['EventName'] == 'ChampionKill'].merge((self._events[self._events['EventName'] == 'ChampionKill'].sort_values(['EventTime']).groupby('KillerName').agg({'EventTime':'max'})).reset_index(), left_on="VictimName", right_on="KillerName", how='left', suffixes=('_main', '_lastkill'))
        last_kill['EventTime_lastkill'] = last_kill['EventTime_lastkill'].fillna(0)
        current_deathstreak = last_kill[last_kill['EventTime_main'] > last_kill['EventTime_lastkill']].groupby('VictimName').agg({'EventTime_main':'count'})
        current_deathstreak.reset_index(inplace=True)
        current_deathstreak.columns = ['VictimName', 'Deaths']
        return current_deathstreak[current_deathstreak['Deaths'] >= 5]

    def get_killStreaks(self):
        last_death = self._events[self._events['EventName'] == 'ChampionKill'].merge((self._events[self._events['EventName'] == 'ChampionKill'].sort_values(['EventTime']).groupby('VictimName').agg({'EventTime':'max'})).reset_index(), left_on="KillerName", right_on="VictimName", how='left', suffixes=('_main', '_lastdeath'))
        last_death['EventTime_lastdeath'] = last_death['EventTime_lastdeath'].fillna(0)
        current_killstreak = last_death[last_death['EventTime_main'] > last_death['EventTime_lastdeath']].groupby('KillerName').agg({'EventTime_main':'count'})
        current_killstreak.reset_index(inplace=True)
        current_killstreak.columns = ['KillerName', 'Kills']
        return current_killstreak[current_killstreak['Kills'] >= 5]

    def isEnemyOnKillStreak(self):
        return (sum([1 if x in self.getEnemySummonerNames() else 0 for x in self.get_killStreaks()['KillerName']]) >=1)
        

    def isSummonerOnKillStreak(self):
        return self._summoner_name in self.get_killStreaks()['KillerName']

    def isSummonerOnDeathStreak(self):
        return self._summoner_name in self.get_deathStreaks()['VictimName']

    def getPlayerGold(self, summoner_name):
        summoner_items = list(filter(lambda players: players['summonerName'] == summoner_name, self._allPlayers))[0]['items']
        return sum([x['price']*x['count'] for x in summoner_items])
        
    def getSummonerGold(self):
        return self.getPlayerGold(self._summoner_name)

    def getFriendlyTeamGold(self):
        return sum([self.getPlayerGold(x) for x in self.getFriendlySummonerNames()])

    def getEnemyTeamGold(self):
        return sum([self.getPlayerGold(x) for x in self.getEnemySummonerNames()])


    #roles living or dead
    #is only alive
    def getFriendlyPlayerByPosition(self, position):
        return list(filter(lambda players: players['position'] == '', self.getFriendlyStats()))[0]

    def getEnemyPlayerByPosition(self, position):
        return list(filter(lambda players: players['position'] == '', self.getFriendlyStats()))[0]

    def getPlayerPosition(self, summoner_name):
        summoner_position = list(filter(lambda players: players['summonerName'] == summoner_name, self._allPlayers))[0]['position']
        return summoner_position

    def isPlayerDead(self, summoner_name):
        return (list(filter(lambda players: players['summonerName'] == summoner_name, self._allPlayers))[0]['isDead'])
        
    def isFriendlyPositionDead(self, position):
        return self.getFriendlyPlayerByPosition(position)['isDead']

    def isAloneInBot(self):
        summonerPosition = self.getPlayerPosition(self._summoner_name)
        if(summonerPosition in ['BOTTOM', 'SUPPORT']):
            return ((summonerPosition == 'SUPPORT' and self.isFriendlyPositionDead('BOTTOM')) or (summonerPosition == 'BOTTOM' and self.isFriendlyPositionDead('SUPPORT')))
        else:
            return False

    def isAloneInGame(self):
        friends = [x for x in self.getPlayerPosition(self._summoner_name) if x != self._summoner_name] #get friendly players with summoner removed
        return ((sum([0 if self.isPlayerDead(x) else 1 for x in friends]) == 0) and not(self.isPlayerDead(self._summoner_name)))

    #EVENT BASED METHODS

    def getFriendlyTeamDragonKills(self):
        return len(self._events[(self._events['EventName'] == 'DragonKill') & (self._events['KillerName'].isin(self.getFriendlySummonerNames()))])

    def getEnemyTeamDragonKills(self):
        return len(self._events[(self._events['EventName'] == 'DragonKill') & (self._events['KillerName'].isin(self.getEnemySummonerNames()))])

    def getFriendlyTurrets(self):
        team_to_name = {"T1":"CHAOS", "T2":"ORDER"}
        turret_info = lc._events[lc._events['EventName'] == 'TurretKilled']['TurretKilled'].str.split('_',expand=True).drop([0,4], axis=1)
        turret_info.columns = ['Team','Lane','Tier']
        turret_info = turret_info.replace({"Team": team_to_name})
        return turret_info[turret_info['Team']==self._summoner_team]

    def getEnemyTurrets(self):
        team_to_name = {"T1":"CHAOS", "T2":"ORDER"}
        turret_info = lc._events[lc._events['EventName'] == 'TurretKilled']['TurretKilled'].str.split('_',expand=True).drop([0,4], axis=1)
        turret_info.columns = ['Team','Lane','Tier']
        turret_info = turret_info.replace({"Team": team_to_name})
        return turret_info[turret_info['Team']!=self._summoner_team]

    def getEnemyTurretsDestroyed(self):
        return len(self.getEnemyTurrets())

    def getFriendlyTurretsDestroyed(self):
        return len(self.getFriendlyTurrets())

    def friendlyNexusTurretsDown(self):
        friendlyTurrets = self.getFriendlyTurrets()
        return len(friendlyTurrets[(friendlyTurrets['Lane'] == 'C') & (friendlyTurrets['Tier'].isin(['01','02']))])

    def enemyNexusTurretsDown(self):
        enemyTurrets = self.getEnemyTurrets()
        return len(enemyTurrets[(enemyTurrets['Lane'] == 'C') & (enemyTurrets['Tier'].isin(['01','02']))])

    def getTurrets(self, team, events):
        try:
            turretsKilled = list(filter(lambda event: event['EventName'] == 'TurretKilled', events))
            teamTurrets = list(filter(lambda death: team in death['TurretKilled'], turretsKilled))
            return len(teamTurrets)
        except:
            return 0

    #GAMEDATA BASED METHODS
    def getGametime(self):
        return self._gameData['gameTime']

    def getGameTerrain(self):
        return self._gameData['mapTerrain']

if __name__ == "__main__":
    # Switch the comments to get real data
    lc = leagueClient()
    lc.populateData()
    #print(lc.LeagueClientRunning())
    print(lc._summoner_data)
    print("\n",len(lc.getFriendlyStats()))
    for x in lc.getFriendlyStats():
        print(x)
    print("\n")
    for x in lc.getEnemyStats():
        print(x)
    #printData(json)
