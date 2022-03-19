import time
import spotify_client
import league_client

if __name__=="__main__":

    spotify = spotify_client.spotifyClient()
    lol = league_client.leagueClient()

    try:
        while(True):
            playerDoingGood = True
            if playerDoingGood:
                spotify.queueSong("good")
                continue

            if not playerDoingGood:
                spotify.queueSong("bad")
                continue

            # And so on for whatever we want...

            # Need to queue a song before the current one runs out
            if spotify.timeRemaining() <= 20:
                spotify.queueSong("whatever")

            time.sleep(10)

    except:
        pass