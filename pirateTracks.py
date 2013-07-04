import json
from threading import Lock  # , Timer
from collections import namedtuple

import requests
import pygst
pygst.require('0.10')
import gst
import gobject

#from getpass import getpass as gp

#We need to contact 8tracks with the API key.
#First things first, let's set up our url and API variables.

BASE_URL = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

Mix = namedtuple('Mix', ['ident', 'name', 'track_count'])


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
    #response = input('Which mix do you want to listen to?: ')
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
        print('CALLBACK!')

    player = gst.element_factory_make('playbin2', 'player')
    bus = player.get_bus()
    bus.add_signal_watch()
    bus.enable_sync_message_emission()
    bus.connect('message', callback)
    #sink = gst.element_factory_make("pulsesink", "pulse")
    sink = gst.element_factory_make('fakesink', 'fakesink')
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
    return parsed_response[u'set'][u'track'][u'url']


def start_streaming():
    '''
    Main function. First grabs a play-token from 8tracks to keep track of
    sessions Next, asks user for a mix, then starts play/next/play/next cycle.
    '''
    play_lock = Lock()
    play_token = get_play_token()

    mix = mix_selection()

    #query_url = (BASE_URL +
                 #'sets/{}/play.json?mix_id={}&api_version=3&api_key={}')
    #query_response = requests.get(query_url.format(
        #play_token, mix.ident, API))
    #play_request = json.loads(query_response.content)
    #track_id = play_request[u'set'][u'track'][u'id']

    for _ in range(mix.track_count):
        track_url = next_track(play_token, mix.ident)

        play_lock.acquire(True)
        print("playing!")
        #timer = Timer(
            #30, report_performance, args=[play_token, mix.ident, track_id])
        #timer.start()
        play_stream(track_url)
        play_lock.release()


if __name__ == '__main__':
    gobject.threads_init()
    start_streaming()
