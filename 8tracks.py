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
    mix = [x[u'name'] for x in request[u'mixes']]
    mix_id = [x[u'id'] for x in request[u'mixes']]
    mix_dict = dict(zip(mix_id, mix))
    for key, value in mix_dict.iteritems():
        print('id: %s\nName: %r' % (key, value))
'''
Now that that's done, let's ask the user for a mix selection
(For testing purposes, we're going to just assume the first one, and start playing that.)
'''
def ask_which():
    input = raw_input('Which mix do you want to listen to?: ')
    return input
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
def report_performance(play_token, mix_id, track_id):
    
    print("Now reporting song as performed. Yay for being legal.")
    #performance_soup = BeautifulSoup(play_request)
    play_token, mix_id, track_id = play_token, mix_id, track_id
    '''
    http://8tracks.com/sets/[play_token]/report.xml?track_id=[track_id]&mix_id=[mix_id]
    '''
    status = json.loads(requests.get(base_url + 'sets/%s/report.json?track_id=%s&mix_id=%s?api_key=%s' % (play_token,track_id,mix_id,API)))
    print status[u'status']

def play_stream(playing, blocking):
    '''
    Current implementation is to open mpg123 as subprocess to play stream.
    '''
    stream = subprocess.Popen(['mpg123', playing])
    #song = AudioSegment.from_file(playing, 'http')
    if blocking:
        stream.wait()
    return

def print_metadata(play_request):
    '''
    This prints information about what is playing.
    '''
    metadata = BeautifulSoup(play_request.text)
    print metadata('performer')
    track = ''
    for i in metadata('name'):
        track = i.string
        
def next(playToken, mix_id):
    '''
    This will get the next URL for playing. First, let's check and make sure we aren't
    at the end of the playlist. Then, get next URL and feed it into the stream.
    URL FORM: http://8tracks.com/sets/[play_token]/next.xml?mix_id=[mix_id]?api_key=[API]
    '''
    print playToken, mix_id
    #Are we at the end?
    next_url = json.loads(requests.get(base_url + 'sets/%s/next.json?mix_id=%s?api_key=%s' % (playToken, mix_id, API)).content)
    print requests.get(base_url + 'sets/%s/next.json?mix_id=%s?api_key=%s' % (playToken, mix_id, API))
    pprint(next_url) #for testing.

    
'''
Done. Now let's actually start the stream.
url form: http://8tracks.com/sets/play_token/play.xml?mix_id?api_key=
Note: Currently broken, but I can hack on this some more.
'''
def start_stream():
    playToken = play_token()
    mix_id = ask_which()
    play_request = json.loads(requests.get(base_url + 'sets/%s/play.json?mix_id=%s?api_key=%s' % (playToken,mix_id,API)).content)
    playing = play_request[u'set'][u'track'][u'url']
    track = play_request[u'set'][u'track'][u'id']
    threading.Timer(30, report_performance, args=[playToken, mix_id, track]).start()
    play_stream(playing, blocking=True)
    next(playToken, mix_id)

request_mixes()
start_stream()
