import json
# TODO: Uncomment following when re-enabling playback reporting
#from threading import Timer
from collections import namedtuple

import requests
import pygst
pygst.require('0.10')
import gst

from getpass import getpass as gp


BASE_URL = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

Mix = namedtuple('Mix', ['ident', 'name', 'track_count'])
Track = namedtuple('Track', ['artist', 'title', 'url'])


class ApiMisuseError(Exception):
    '''
    Reserved for instances where the API isn't pleased with our actions
    '''


def _build_track_from_response(json_response):
    '''
    Uses parsed JSON data to construct a Track object
    '''
    parsed_track = json_response[u'set'][u'track']

    return Track(parsed_track[u'performer'],
                 parsed_track[u'name'],
                 parsed_track[u'url'])


def gather_mixes(print_mixes=False):
    '''
    Request 8tracks' Top mixes.
    Displays id, name, and track count.
    returns trackDict to invoking function
    '''
    mixes_url = BASE_URL + 'mixes.json?api_key=' + API
    mixes_response = requests.get(mixes_url)
    mixes_parsed = json.loads(mixes_response.content)

    mixes = {}
    for ident, name, track_count in zip(
            [x[u'id'] for x in mixes_parsed[u'mixes']],
            [x[u'name'] for x in mixes_parsed[u'mixes']],
            [x[u'tracks_count'] for x in mixes_parsed[u'mixes']]):
        mixes[ident] = Mix(ident, name, track_count)
        if print_mixes:
            print("ID: {} :: Name: {}".format(ident, name.encode('utf-8')))

    return mixes


def mix_selection():
    '''
    Calls to display_mixes to present list/info.
    Allows user to select the mix.
    Returns id, noTracks to invoking function.
    '''
    mixes = gather_mixes(print_mixes=True)
    # TODO: Swap response to use user input
    #response = raw_input('Which mix do you want to listen to?: ')
    response = 1983822
    return mixes[response]


def get_play_token():
    '''
    For playing, we need to first request a new play token.
    URL FORM: BASE_URL/sets/new.json?[API]
    '''
    token_url = BASE_URL + '/sets/new.json?api_key=' + API
    token_response = requests.get(token_url)
    token = json.loads(token_response.content)
    return token[u'play_token']


def print_metadata(track):
    '''
    This prints information about what is playing.
    '''
    print('*****\nNow Playing "{}" by {}\n*****'.format(
        track.title.encode('utf-8'), track.artist.encode('utf-8')))


def report_performance(play_token, mix_id, track_id):
    '''
    8tracks needs to report each play to remain legal. A song is counted as
    "performed" at the 30 second mark.
    '''
    print("Now reporting song as performed. Yay for being legal.")
    request_url = BASE_URL + 'sets/{}/report.?track_id={}&mix_id={}&api_key={}'
    requests.get(request_url.format(play_token, track_id, mix_id, API))


def play_stream(playing):
    '''
    Updated implementation! WOO! play_stream now uses gstreamer as its
    player. Cross-Platform ready!
    '''
    def callback(bus, message):
        print('Please work, Mr. Callback!')

    player = gst.element_factory_make('playbin2', 'player')
    bus = player.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect('message', callback)
    sink = gst.element_factory_make("pulsesink", "pulse")
    player.set_property("audio-sink", sink)
    player.set_property('uri', playing)

    player.set_state(gst.STATE_PLAYING)


def next_track(play_token, mix_id):
    '''
    This will get the next URL for playing. First, let's check and make
    sure we aren't at the end of the playlist. Then, get next URL and
    feed it into the stream.
    '''
    track_response = requests.get(
        BASE_URL + 'sets/{}/next.json?mix_id={}&api_key={}'.format(
            play_token, mix_id, API))

    parsed_response = json.loads(track_response.content)
    return _build_track_from_response(parsed_response)


def skip_track(play_token, mix_id):
    '''
    Skip Track

    Checks to see if skips are allowed, if true, skip to next URL Stream.
    If false, display so to user.
    '''
    skip_response = requests.get(
        BASE_URL +
        '/sets/{}/skip.json?mix_id={}&api_version=2&api_key={}'.format(
            play_token, mix_id, API))

    parsed_response = json.loads(skip_response.content)

    if parsed_response[u'set'][u'skip_allowed'] != 'True':
        raise ApiMisuseError('You may skip again in {} seconds.'.format(
            parsed_response[u'skip_allowed_in_seconds']))

    return _build_track_from_response(parsed_response)


def start_streaming():
    '''
    Main function. First grabs a play-token from 8tracks to keep track of
    sessions Next, asks user for a mix, then starts play/next/play/next cycle.
    '''
    play_token = get_play_token()

    mix = mix_selection()

    # TODO: Following commented lines are for reporting performance.
    #       Reenable as needed.

    #query_url = (BASE_URL +
                 #'sets/{}/play.json?mix_id={}&api_version=3&api_key={}')
    #query_response = requests.get(query_url.format(
        #play_token, mix.ident, API))
    #play_request = json.loads(query_response.content)
    #track_id = play_request[u'set'][u'track'][u'id']

    for _ in range(mix.track_count):
        track = next_track(play_token, mix.ident)

        print("playing!")
        # TODO: Following commented lines are for reporting performance.
        #       Reenable as needed.

        #timer = Timer(
            #30, report_performance, args=[play_token, mix.ident, track_id])
        #timer.start()
        play_stream(track.url)


def verify_user():
    '''
    Get username and password from user. Currently unused function.
    Make an https/ssl POST request. Will return with embedded user-token
    to be used throughout site. Afterwards, return the user-token
    to invoking function.
    '''
    username = 'test'  # TODO: Uncomment following line
    #username = raw_input('Username: ')
    password = gp()
    data = 'login={}&password={}'.format(username, password)
    secureHTTPS = 'https://8tracks.com/'

    verify = requests.post(secureHTTPS + 'sessions.json', data=data)
    parsed_response = json.loads(verify.content)

    return parsed_response[u'user_token']


if __name__ == '__main__':
    start_streaming()