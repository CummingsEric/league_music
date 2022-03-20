import time
import spotify_client
from event import *

if __name__=="__main__":

    spotify = spotify_client.spotifyClient()
    eg = eventGenerator(30)
    oldEvent = None
    currentEventType = None
    currentEventTime = None

    
    while(True):
        #print("getting event")
        currentEvent = eg.get_event()
        print(f'the event returned was of type {currentEvent.getEventType()} from {currentEvent.getEventSource()}')
        currentEventType = currentEvent.getEventType()
        
        if((oldEvent == None) or (currentEvent.getEventType() != oldEvent.getEventType())):
            print(f'setting new song to {currentEvent.getEventType()}')
            oldEvent = currentEvent
            spotify.queueSong(currentEvent.getEventType())
            time.sleep(20)
            continue

        # Need to queue a song before the current one runs out
        if spotify.timeRemaining() <= 20:
            spotify.queueSong(oldEvent.getEventType())

        time.sleep(5)

    #except Exception as e:
    #    print(e)
        