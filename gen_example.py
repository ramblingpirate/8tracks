import json
from collections import namedtuple

import requests

from decorator_example import authorized


URL = 'http://8tracks.com/'
KEY = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

Track = namedtuple('Track', ['url', 'ident'])


class EndOfStream(Exception):
    """End of stream has been reached"""


@authorized
def tracks(mix_id, token):
    """Generator of Tracks from a 8tracks mix

    Iterate over `tracks` and send the result to some sort
    of program that can play audio streams:

        for track in tracks(some_mix_id):
            play_from_url(track.url)

    Each Track object has a url attribute and an ident attribute
    The ident attribute points to that track's 8tracks id (necessary
    for reporting playback). The url is the location where the stream
    can be found.
    """
    def query_url(url):
        response = requests.get(url)
        parsed_response = json.loads(response.content)

        if parsed_response[u'set'][u'at_end'] == 'true':
            raise EndOfStream()

        track = parsed_response[u'set'][u'track']
        return Track(url=track[u'url'], ident=track[u'id']) 

    track_url = URL + 'sets/{}/play.json?mix_id={}&api_key={}'.format(
        token, mix_id, KEY)
    yield query_url(track_url)

    while True:
        next_url = URL + 'sets/{}/next.json?mix_id={}&api_key={}'.format(
            token, mix_id, KEY)
        yield query_url(next_url)


if __name__ == '__main__':
    x = tracks(1915496)
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))
    print(next(x))
