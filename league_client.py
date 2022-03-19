from urllib.parse import non_hierarchical
import requests
import urllib3
import json
from leagueExceptions import *
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class leagueClient():
    _player_stats = None
    _game_info = None
    _summoner_name = None
    _player_info = None
    _myteam = None
    _player_team = non_hierarchical
    
    def __init__(self):
        print("client started")

    def LeagueClientRunning(self):
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
        #sett basic level information
        self._set_player_stats()
        
        return True

    def _set_player_stats(self):
        self._summoner_name = self._game_info['activePlayer']['summonerName']
        self._player_info = next(filter(lambda players: players['summonerName'] == self._summoner_name, self._game_info['allPlayers']))
        self._player_team = self._player_info['team']

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

    def get_all_data(self):
        if(self._game_info):
            return(self._game_info)
        elif(self._getAllData()):
            #the game data is null this could possibly happen on the first call or before league client has started
            return(self._game_info)
        else:
            #there is no data, and the league client is not running
            raise LeagueClientError('unable to retrieve data from league client')

    def get_player_data(self):
        if(self._game_info):
            return(self._player_stats)
        elif(self._getPlayerStats()):
            #the game data is null this could possibly happen on the first call or before league client has started
            return(self._player_stats)
        else:
            #there is no data, and the league client is not running
            raise LeagueClientError('unable to retrieve data from league client')

    #functions for pulling data out of json information
    def get_friendly_stats(self):
        return list(filter(lambda players: players['team'] == self._player_team, self._game_info['allPlayers']))

    def get_enemy_stats(self):
        return list(filter(lambda players: players['team'] != self._player_team, self._game_info['allPlayers']))



    def get_player_kda(self, stats):
        killsAssists = stats['scores']['assists'] + stats['scores']['kills']
        deaths = stats['scores']['deaths']
        deaths = deaths if deaths != 0 else 1
        return killsAssists / deaths

    def itemCost(self, stats):
        allItems = stats['items']
        cost = 0
        for item in allItems:
            cost += item['price']
        return cost

    def getDragons(self, summonerNames, events):
        try:
            dragonDeaths = list(filter(lambda event: event['EventName'] == 'DragonKill', events))
            teamDragons = list(filter(lambda death: death['KillerName'] in summonerNames, dragonDeaths))
            return len(teamDragons)
        except:
            return 0

    def getTurrets(self, team, events):
        try:
            turretsKilled = list(filter(lambda event: event['EventName'] == 'TurretKilled', events))
            teamTurrets = list(filter(lambda death: team in death['TurretKilled'], turretsKilled))
            return len(teamTurrets)
        except:
            return 0

if __name__ == "__main__":
    # Switch the comments to get real data
    lc = leagueClient()
    lc.populateData()
    #print(lc.LeagueClientRunning())
    print(lc._player_stats)
    #printData(json)
