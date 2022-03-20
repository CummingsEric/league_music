from league_client import leagueClient

class eventGenerator():
    def __init__(self, recent):
        self.lc = leagueClient(recent)

    def get_event(self):
        self.lc.populateData()

        




class event():
    def __init__(self, eventType, eventTime):
        self.eventType = eventType
        self.eventTime = eventTime
