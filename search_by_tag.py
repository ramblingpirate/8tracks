import json, requests, urllib2

from pprint import pprint

URL = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

def search_by_tag(tag):
    '''
    Searches for mixes using tags.
    '''
    #search = raw_input('Enter a tag: ')
    searchRE = requests.get(URL + 'mixes.json?tag={}&api_version=2&api_key={}'.format(tag, API))
    searchJSON = json.loads(searchRE.content)
    #pprint(searchJSON)
    mixes = {}
    for ident, name, noTracks, desc, imgurl in zip([x[u'id'] for x in searchJSON[u'mixes']],[x[u'name'] for x in searchJSON[u'mixes']],
        [x[u'tracks_count'] for x in searchJSON[u'mixes']], [x[u'description'] for x in searchJSON[u'mixes']],
        [x[u'cover_urls'][u'original'] for x in searchJSON[u'mixes']]):
        #print('*****\nid: {}\nName: {}\nTrack Count: {}\n*****'.format(ident, name.encode('utf-8'), noTracks))
        mixes.update({ident:(name, desc, imgurl)})
        
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
