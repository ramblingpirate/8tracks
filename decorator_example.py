import json
from functools import wraps

import requests


URL = 'http://8tracks.com/'
KEY = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'


def authorized(func):
    """Decorates functions requiring a 8tracks play token
    Injects a keyword argument (token) into the decorated function

    @authorized
    def foo(token):
        ...

    @authorized
    def foo(bar, token):
        ...
    """
    token_url = URL + '/sets/new.json?api_key=' + KEY
    response = requests.get(token_url)
    parsed_response = json.loads(response.content)
    play_token = parsed_response[u'play_token']

    def wrapped(*args, **kwargs):
        new_kwargs = {'token': play_token}
        new_kwargs.update(kwargs)

        return func(*args, **new_kwargs)

    wrapped.__doc__ = func.__doc__

    return wrapped
