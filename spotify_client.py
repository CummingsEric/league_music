import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-read-playback-state,user-modify-playback-state"
CLIENT_ID = "0c51a110dea445f49fbbed2d29d387c9"
CLIENT_SECRET = "95b5363808b34b15ae831e3e0cc5f146"
REDIRECT_URI = "https://google.com"
DEVICE_ID = 'cf9108807ab618287dc0e79e74241e383e4d7ecb'
# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE))

print(sp.devices())
# Transfer playback to the Raspberry Pi if music is playing on a different device
sp.transfer_playback(device_id=DEVICE_ID, force_play=False)

# Play the spotify track at URI with ID 45vW6Apg3QwawKzBi03rgD (you can swap this for a diff song ID below)
sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:45vW6Apg3QwawKzBi03rgD'])