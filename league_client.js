const https = require('https')
const axios = require('axios');

url = 'https://127.0.0.1:2999/liveclientdata/allgamedata';

class leagueClient {

    allPlayers = []
    gameInfo = {}
    activePlayer = {}

    summonerName = ""
    summonerTeam = ""
    summonerData = {}
    
    events = []
    gameData = {}
    recentTime = null

    constructor() {

    }

    async getData() {
        const instance = axios.create({
            httpsAgent: new https.Agent({  
              rejectUnauthorized: false
            })
        });

        try {
            const res = await instance.get(url);
            const data = res.data
            this.gameData = data
            this.activePlayer = data['activePlayer']
            this.allPlayers = data['allPlayers']
            this.events = data['events']
            if (res.status === 200) {
                return true;
            }
            return false;
        } catch (err) {
            return false;
        }
    }

    setPlayerStats() {
        this.summonerName = this.activePlayer.summonerName
        this.summonerData = this.allPlayers.find(p => p['summonerName'] === this.summonerName)
        this.summonerTeam = this.summonerData['team']
    }

    async populateData() {
        const isAlive = await this.getData()
        if (isAlive) {
            this.setPlayerStats()
            this.getFriendlyTeamKDA()

        }
    }

    getFriendlyStats() {
        if (!Array.isArray(this.allPlayers)) return []
        return this.allPlayers.filter(p => p['team'] === this.summonerTeam)
    }

    getEnemyStats() {
        if (!Array.isArray(this.allPlayers)) return []
        return this.allPlayers.filter(p => p['team'] !== this.summonerTeam)
    }

    getFriendlySummonerNames() {
        return this.getFriendlyStats().map(p => p['summonerName'])
    }

    getEnemySummonerNames() {
        return this.getEnemyStats().map(p => p['summonerName'])
    }

    getPlayerStats(summonerName){
        const summoner_stats = this.allPlayers.find(p => p['summonerName'] === summonerName)
        if (summoner_stats === undefined) return {}
        return summoner_stats
    }

    getPlayerKDA(summonerName) {
        const summoner_stats = this.getPlayerStats(summonerName)
        return (summoner_stats['scores']['assists'] + summoner_stats['scores']['kills'])/Math.max(1, summoner_stats['scores']['deaths'])
    }

    getSummonerKDA() {
        return this.getPlayerKDA(this.summonerName)
    }

    getFriendlyTeamKDA() {
        return this.getFriendlyStats().map(s => (s['scores']['assists'] + s['scores']['kills'])/Math.max(1, s['scores']['deaths']))
    }

    getEnemyTeamKDA() {
        return this.getEnemyStats().map(s => (s['scores']['assists'] + s['scores']['kills'])/Math.max(1, s['scores']['deaths']))
    }

    getPlayerGold(summoner_name) {
        const summoner_stats = this.getPlayerStats(summonerName)
        const summoner_items = summoner_stats['items']
        const goldArr = summoner_items.map(item => item['price'] *item['count'])
        return goldArr.reduce((sum, a) => sum + a, 0)
    }

    getSummonerGold() {
        return self.getPlayerGold(self._summoner_name)
    }

    getFriendlyTeamGold() {
        const goldArr = this.getFriendlySummonerNames().map(n => this.getSummonerGold(n))
        return goldArr.reduce((sum, a) => sum + a, 0);
    }

    getEnemyTeamGold(){
        const goldArr = this.getEnemySummonerNames().map(n => this.getSummonerGold(n))
        return goldArr.reduce((sum, a) => sum + a, 0);
    }

}



const client = new leagueClient();
client.populateData()
