from collections import namedtuple

import json, requests, urllib2
from pprint import pprint

review_info = namedtuple('User', ['review_body', 'created_at', 'user_id'])

URL = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

def search_by_tag(tag):
    '''
    Searches for mixes using tags.
    '''
    #search = raw_input('Enter a tag: ')
    Mix = namedtuple('Mix', ['ident', 'name', 'track_count'])
    tag = tag.replace(" ", "%2B")
    searchRE = requests.get(URL + 'mixes.json?tag={}&api_version=2&api_key={}'.format(tag, API))
    searchJSON = json.loads(searchRE.content)
    #pprint(searchJSON)
    mixes = {}
    for ident, name, noTracks in zip([x[u'id'] for x in searchJSON[u'mixes']],[x[u'name'] for x in searchJSON[u'mixes']],
        [x[u'tracks_count'] for x in searchJSON[u'mixes']]):
        #print('*****\nid: {}\nName: {}\nTrack Count: {}\n*****'.format(ident, name.encode('utf-8'), noTracks))
        mixes[ident] = Mix(ident, name, noTracks)
    return mixes

def search_by_artist():
    '''
    Searches for mixes by Artist
    '''
    search = raw_input('Enter artist name: ')
    searchRE = requests.get(URL + 'mixes.json?q={}&api_version=2&api_key={}'.format(search, API))
    searchJSON = json.loads(searchRE.content)
    
    for ident, name, noTracks in zip([x[u'id'] for x in searchJSON[u'mixes']],[x[u'name'] for x in searchJSON[u'mixes']], [x[u'tracks_count'] for x in searchJSON[u'mixes']]):
        print('*****\nid: {}\nName: {}\nTrack Count: {}\n*****'.format(ident, name.encode('utf-8'), noTracks))

    #mix = raw_input('Mix ID: ')
    #return mix

def sort_results():
    '''
    Sorts results by newest/popular/hot
    '''

def get_mix_reviews(mixID):
    reviews_re = requests.get(URL + '/mixes/{}/reviews.json?api_key={}'.format(mixID, API))
    reviews_JSON = json.loads(reviews_re.content)
    review_results = {}
    
    for body, created, id in zip(
        [x[u'body'] for x in reviews_JSON[u'reviews']],
        [x[u'created_at'] for x in reviews_JSON[u'reviews']],
        [x[u'id'] for x in reviews_JSON[u'reviews']]):
            review_results[id] = review_info(body, created, id)
            
    return review_results
    
def get_user_info(user_id):
    # Retrieves the user id to display the username/picture.
    try:
        user_RE = requests.get(URL + '/users/{}.json?api_key={}'.format(user_id, API))
        user_JSON = json.loads(user_RE.content)
        #pprint(user_JSON[u'user'])
        return user_JSON[u'user'][u'slug']
    except KeyError:
        return "User deleted"
    
def get_mix_cover(mixID):
    coverRE = requests.get(URL + '/mixes/{}.json?api_key={}'.format(mixID, API))
    cover_JSON = json.loads(coverRE.content)
    return cover_JSON[u'mix'][u'cover_urls'][u'original']