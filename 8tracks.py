from bs4 import BeautifulSoup
import requests
import subprocess, threading
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
    request = requests.get(base_url + 'mixes.xml?api_key=' + API)
    soup = BeautifulSoup(request.text)
    counter = 0
    mix = []
    mix_id = []
    for i in soup('id'):
        mix_id.append(i.string)
    for i in soup('name'):
        mix.append(i.string)
    mix_dict = dict(zip(mix_id, mix))
    for key, value in mix_dict.iteritems():
        print('id: %s\nName: %s' % (key, value))
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
    new_request = requests.get(base_url + '/sets/new.xml?api_key=' + API)
    if new_request == '<Response [200]>':
        print "OK"
    new_soup = BeautifulSoup(new_request.text)
    play_token = ''
    for i in new_soup('play-token'):
        play_token = i.string
    return play_token
'''
8tracks needs to report each play to remain legal. A song is counted as "performed" at the 30 second mark. 
def report_performancef()
'''
def report_performance(play_request, play_token, mix_id):
    
    print("Now reporting song as performed. Yay for being legal.")
    #performance_soup = BeautifulSoup(play_request)
    track_id = ''
    performance_soup, play_token, mix_id = BeautifulSoup(play_request), play_token, mix_id
    for i in performance_soup('id'):
        track_id = i.string
    '''
    http://8tracks.com/sets/[play_token]/report.xml?track_id=[track_id]&mix_id=[mix_id]
    '''
    status = requests.get(base_url + 'sets/%s/report.xml?track_id=%s&mix_id=%s?api_key=%s' % (play_token,track_id,mix_id,API))
    print status

def play_stream(playing):
    '''
    Current implementation is to open mpg123 as subprocess to play stream.
    '''
    stream = subprocess.Popen(['mpg123', playing])
    return
    
def next(play_token, mix_id, play_request):
    '''
    This will get the next URL for playing. First, let's check and make sure we aren't
    at the end of the playlist. Then, get next URL and feed it into the stream.
    URL FORM: http://8tracks.com/sets/[play_token]/next.xml?mix_id=[mix_id]?api_key=[API]
    '''
    play_request = BeautifulSoup(play_request)
    #Are we at the end?
    at_end = ''
    for i in play_request('at-end'):
        at_end = i.string
    print at_end
    if at_end == 'false':
        next = requests.get(base_url + 'sets/%s/next.xml?mix_id=%s?api_key=%s' % (play_token, mix_id, API))
        play_stream(format_play_url(next.text))   
    else:
        print('We have a problem getting the next track. We\'re working on it.')
    
'''
Done. Now let's actually start the stream.
url form: http://8tracks.com/sets/play_token/play.xml?mix_id?api_key=
Note: Currently broken, but I can hack on this some more.
'''
def start_stream():
    playToken = play_token()
    mix_id = ask_which()
    play_request = requests.get(base_url + 'sets/%s/play.xml?mix_id=%s?api_key=%s' % (playToken,mix_id,API))
    #print play_request
    metadata = BeautifulSoup(play_request.text)
    playing = format_play_url(play_request.text)
    artist = ''
    for i in metadata('performer'):
        artist = i.string
    track = ''
    for i in metadata('name'):
        track = i.string
    print('Now playing \'%s\' by %s' % (track, artist))
    threading.Timer(30, report_performance, args=[play_request.text, playToken, mix_id]).start()
    play_stream(playing)
    #next(play_token, mix_id, play_request.text)

request_mixes()
start_stream()
