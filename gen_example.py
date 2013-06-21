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
def track_urls(token, mix_id=1915496):
    def query_url(url):
        response = requests.get(track_url)
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
    import pirateTracks

    for track in track_urls():
        pirateTracks.play_stream(track.url, blocking=True)
