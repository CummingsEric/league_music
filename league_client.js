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
        this.summonerName = this.activePlayer['summonerName']
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

    getPlayerStats(playerName){
        const playerStats = this.allPlayers.find(p => p['summonerName'] === playerName)
        if (playerStats === undefined) return {}
        return playerStats
    }

    getPlayerKDA(playerName) {
        const summoner_stats = this.getPlayerStats(playerName)
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

    getPlayerGold(playerName) {
        const playerStats = this.getPlayerStats(playerName)
        const summonerItems = playerStats['items']
        const goldArr = summonerItems.map(item => item['price'] *item['count'])
        return goldArr.reduce((sum, a) => sum + a, 0)
    }

    getSummonerGold() {
        return this.getPlayerGold(this.summonerName)
    }

    getFriendlyTeamGold() {
        const goldArr = this.getFriendlySummonerNames().map(n => this.getSummonerGold(n))
        return goldArr.reduce((sum, a) => sum + a, 0);
    }

    getEnemyTeamGold(){
        const goldArr = this.getEnemySummonerNames().map(n => this.getSummonerGold(n))
        return goldArr.reduce((sum, a) => sum + a, 0);
    }

    getFriendlyPlayerByPosition(position){
        const teamStats = self.getFriendlyStats();
        return teamStats.find(p => p['position'] === position);
    }

    getFriendlyPlayerByPosition(position){
        const enemyStats = self.getEnemyStats();
        return enemyStats.find(p => p['position'] === position);
    }

    getPlayerPosition(playerName) {
        const playerStats = this.getPlayerStats(playerName);
        return playerStats['position'];
    }

    isPlayerDead(playerName) {
        const playerStats = this.getPlayerStats(playerName);
        return playerStats['isDead'];
    }

    isFriendlyPositionDead(position) {
        const positionStats = this.getFriendlyPlayerByPosition(position);
        return positionStats['isDead'];
    }

    isEnemyPositionDead(position) {
        const positionStats = this.getEnemyPlayerByPosition(position);
        return positionStats['isDead'];
    }

    isAloneInBot(){
        const summonerPosition = this.getPlayerPosition(this.summonerName);
        if (summonerPosition === 'BOTTOM') {
            return this.isFriendlyPositionDead('SUPPORT');
        } 
        if (summonerPosition === 'SUPPORT') {
            return this.isFriendlyPositionDead('BOTTOM');
        }
        return false;
    }

    isAloneInGame() {
        // Can't be alone if youre dead
        if (this.isPlayerDead(this.summonerName)===true){
            return false;
        }
        const teamStats = this.getFriendlyStats()
        for (stat in teamStats) {
            // If anyone else on your team is alive you're not alone
            if (stat['summonerName'] !== this.summonerName && stat['isDead'] === 0){
                return false;
            }
        } 
        return true;
    }
}



const client = new leagueClient();
client.populateData()
