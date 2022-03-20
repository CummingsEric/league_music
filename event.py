from league_client import leagueClient

class eventGenerator():
    def __init__(self, recentTimeThresh):
        self.lc = leagueClient(recentTimeThresh)

    def get_event(self):
        print('populating data')
        self.lc.populateData()
        if(self.lc.wereInTheEndGameNow()):
            return event('end', 'wereInTheEndGameNow')
        elif(self.lc.objRecentlyStolenByFriendly()):
            return event('good',  'objRecentlyStolenByFriendly')
        elif(self.lc.objRecentlyStolenByEnemy()):
            return event('bad',  'objRecentlyStolenByEnemy')
        elif(self.lc.elderRecentlyKilledByFriendly()):
            return event('hype',  'elderRecentlyKilledByFriendly')
        elif(self.lc.elderRecentlyKilledByEnemy()):
            return event('bad',  'elderRecentlyKilledByEnemy')
        elif(self.lc.barronRecentlyKilledByFriendly()):
            return event('good',  'barronRecentlyKilledByFriendly')
        elif(self.lc.barronRecentlyKilledByEnemy()):
            return event('bad',  'barronRecentlyKilledByEnemy')
        elif(self.lc.elderSpawningSoon()):
            return event('rumble',  'elderSpawningSoon')
        elif(self.lc.FriendlyTeamAce()):
            return event('hype',  'FriendlyTeamAce')
        elif(self.lc.EnemyTeamAce()):
            return event('bad',  'EnemyTeamAce')
        elif(self.lc.summonerKillstreak()):
            return event('hype',  'summonerKillstreak')
        elif(self.lc.summonerDeathstreak()):
            return event('terrible',  'summonerDeathstreak')
        elif(self.lc.summonerRecentMultikill()):
            return event('good',  'summonerRecentMultikill')       
        elif(self.lc.enemyKillstreak()):
            return event('boss',  'enemyKillstreak')
        #elif(self.lc.alone()):
        #    return event('alone',  'alone')
        elif(self.lc.heraldRecentlyKilledByFriendly()):
            return event('good',  'heraldRecentlyKilledByFriendly')
        elif(self.lc.heraldRecentlyKilledByEnemy()):
            return event('bad',  'heraldRecentlyKilledByEnemy')
        elif(self.lc.summonerDoingGood()):
            return event('good',  'summonerDoingGood')
        elif(self.lc.summonerDoingBad()):
            return event('bad',  'summonerDoingBad')
        else:
            return event('jungle',  'this was the last thing left') 






class event():
    def __init__(self, eventType, eventSource):
        self.eventType = eventType
        self.eventSource = eventSource

    def getEventSource(self):
        return self.eventSource

    def getEventType(self):
        return self.eventType




if __name__ == "__main__":
    eg = eventGenerator