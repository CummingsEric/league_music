import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import random
import os
from dotenv import load_dotenv
load_dotenv('./.env')

SCOPE = "user-read-playback-state,user-modify-playback-state"
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = "https://google.com"
DEVICE_ID = os.getenv('DEVICE_ID')

class spotifyClient():
    _sp = None
    _songs = None

    def __init__(self):
        # Spotify Authentication
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI,
                                                        scope=SCOPE))
        # Transfer playback to the Raspberry Pi if music is playing on a different device
        self._sp.transfer_playback(device_id=DEVICE_ID, force_play=False)
        with open('music.json') as songFile:
            self._songs = json.load(songFile)

    def queueSong(self, type):
        try: 
            songList = self._songs[type]
            songData = random.choice(songList)
            self._sp.start_playback(device_id=DEVICE_ID, uris=[songData['id']], position_ms=songData['pos']*1000)
        except:
            pass

    def testSong(self, name):
        try: 
            for item in self._songs.values():
                for song in item:
                    if song['name']==name:
                        self._sp.start_playback(device_id=DEVICE_ID, uris=[song['id']], position_ms=song['pos']*1000)
        except:
            pass

    def timeRemaining(self):
        try:
            playerInfo = self._sp.current_playback()
            return (playerInfo['item']['duration_ms'] - playerInfo['progress_ms'])/1000
        except:
            return 0

# if __name__=="__main__":
    # spot = spotifyClient()
    # spot.testSong("Blame it on me")