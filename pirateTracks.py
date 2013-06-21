from bs4 import BeautifulSoup
import requests, json
import subprocess, threading
from pprint import pprint
#from pydub import AudioSegment
''' 
We need to contact 8tracks with the API key.
First things first, let's set up our url and API variables.
'''
base_url = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'
'''
Formats URL's into something that mpg123 can actually understand
'''
def format_play_url(url):
    play_soup = BeautifulSoup(url)
    player = play_soup('url')
    playing = ''
    for i in player:
        playing = i.string
    return playing
'''
Now, let's make the actual request to 8tracks server function.
'''
def request_mixes():
    request = json.loads(requests.get(base_url + 'mixes.json?api_key=' + API).content)
    for ident, name in zip([x[u'id'] for x in request[u'mixes']],[x[u'name'] for x in request[u'mixes']]):
        print('id: %s\nName: %r' % (ident, name))
'''
Now that that's done, let's ask the user for a mix selection
(For testing purposes, we're going to just assume the first one, and start playing that.)
'''
def ask_which():
    response = raw_input('Which mix do you want to listen to?: ')
    return response
'''
For playing, we need to first request a new play token.
'''
def play_token():
    new_request = json.loads(requests.get(base_url + '/sets/new.json?api_key=' + API).content)
    return new_request[u'play_token']
'''
8tracks needs to report each play to remain legal. A song is counted as "performed" at the 30 second mark. 
def report_performancef()
'''
def report_performance(playToken, mix_id, track_id):
    
    print("Now reporting song as performed. Yay for being legal.")
    #performance_soup = BeautifulSoup(play_request)
    playToken, mix_id, track_id = playToken, mix_id, track_id
    '''
    http://8tracks.com/sets/[play_token]/report.xml?track_id=[track_id]&mix_id=[mix_id]
    '''
    status = requests.get(base_url + 'sets/%s/report.?track_id=%s&mix_id=%s&api_key=%s' % (play_token,track_id,mix_id,API))

def play_stream(playing, blocking):
    '''
    Current implementation is to open mpg123 as subprocess to play stream.
    '''
    stream = subprocess.Popen(['mpg123', playing])
    #song = AudioSegment.from_file(playing, 'http')
    if blocking:
        stream.wait()
    return

def print_metadata(artist, track):
    '''
    This prints information about what is playing.
    '''
    print('Now Playing "{}" by {}'.format(track, artist))
        
def next(playToken, mix_id):
    '''
    This will get the next URL for playing. First, let's check and make sure we aren't
    at the end of the playlist. Then, get next URL and feed it into the stream.
    URL FORM: http://8tracks.com/sets/[play_token]/next.xml?mix_id=[mix_id]?api_key=[API]
    '''
    print playToken, mix_id
    next_url = json.loads(requests.get(base_url + 'sets/%s/next.json?mix_id=%s&api_key=%s' % (playToken, mix_id, API)).content)
    '''
    Are we at the end of the mix?
    If so, implement next mix using 
    URL FORM: http://8tracks.com/sets/[play_token]/next_mix.json?mix_id=[mix_id]&API
    '''
    if next_url[u'set'][u'at_end'] != 'false':
        print_metadata(next_url[u'set'][u'track'][u'performer'], next_url[u'set'][u'track'][u'name'])
        play_stream(next_url[u'set'][u'track'][u'url'], blocking=True)
    else:
        next_mix = json.loads(requests.get(base_url + 'sets/%s/next_mix.json?mix_id=%s&api_key=%s' % (playToken, mix_id, API)).content)
        play_stream(next_mix[u'set'][u'track'][u'url'])
    
'''
Done. Now let's actually start the stream.
url form: http://8tracks.com/sets/play_token/play.xml?mix_id?api_key=
Note: Currently broken, but I can hack on this some more.
'''
def start_stream():
    playToken = play_token()
    mix_id = ask_which()
    play_request = json.loads(requests.get(base_url + 'sets/%s/play.json?mix_id=%s&api_key=%s' % (playToken,mix_id,API)).content)
    playing = play_request[u'set'][u'track'][u'url']
    track = play_request[u'set'][u'track'][u'id']
    threading.Timer(30, report_performance, args=[playToken, mix_id, track]).start()
    print_metadata(play_request[u'set'][u'track'][u'performer'], play_request[u'set'][u'track'][u'name'])
    play_stream(playing, blocking=True)
    next(playToken, mix_id)
    next(playToken, mix_id)
    next(playToken, mix_id)

if __name__ == '__main__':
    request_mixes()
    start_stream()
