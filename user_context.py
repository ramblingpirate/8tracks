import requests, json
#import pirateTracks
#from getpass import getpass as gp

secureURL = 'https://8tracks.com/'
URL = 'http://8tracks.com/'
API = 'd9a4ca3f43e70029e3619fdc7869d1cd608141e0.'

def new_user():
    '''
    Adds a user login and password to the 8tracks servers.
    URL: https://8tracks.com/users.json
    DATA: 'user[login]=[desired username]&user[password]=[password]&user[email]=[email@email.com]&[user_agree_to_terms]=1/0' (y/n)
    
    8tracks will respond with either 201 (if successful) or 422 (if there's a validation error)
    important data is saved in [u'current-user'] including [u'id'], [u'login'], and [u'user-token']
    
    Failure will be stored in [u'notices'][u'notice']
    '''
    desiredUsername = raw_input("Desired Username: ").rstrip()
    desiredPassword = gp().rstrip()
    email = raw_input('Email: ').rstrip()
    agreement = raw_input('Do you agree? ').rstrip()
    headers = 'X-Api-Key: {}'.format(API)
    if agreement == 'n':
        print('You must agree to the Terms & Conditions.')
    else:
        userData = 'user[login]={}&user[password]={}&user[email]={}&user[agree_to_terms]=1'.format(desiredUsername,desiredPassword,email)
    
    newUser = requests.post(secureURL + 'users.json?api_version=2', data=userData)
    print newUser
    newUserJSON = json.loads(newUser.content)
    
    if newUserJSON[u'status'] == '422 Unprocessable Entity':
        print('Sorry, there was an error while we were creating your login. 8tracks says: {}'.format(newUserJSON[u'errors']))
    else:
        print('Congratulations on your new account! I\'m sure an email has been sent to your account or something.\nMake sure to remember your login and password')
    
def tracks_played(playToken, mixID):
    '''
    Displays tracks played from current mix so far. User context ignorant.
    URL FORM: http://8tracks.com/sets/[playToken]/tracks_played.json?mix_id=[mixID]
    
    Individual track data is stored in [u'tracks']. Performer and Song Title are stored @ [u'tracks'][u'track'][u'performer'] and
        [u'tracks'][u'track'][u'name'], respectively.
    '''
    tracksPlayed = requests.get(URL + 'sets/{}/tracks_played.json?mix_id={}&api_version=2&api_key={}'.format(playToken, mixID, API))
    tracksJSON = json.loads(tracksPlayed.content)
    print('Listening History:\n')
    for name, performer in zip([x[u'name'] for x in tracksJSON[u'tracks']],[x[u'performer'] for x in tracksJSON[u'tracks']]):
        print('*****\n"{}" by {}\n*****'.format(name.encode('utf-8'), performer))
    print('\n')
    
def nsfw_toggle(onOFF):
    '''
    Toggles the NSFW filter. User context aware. (Filters out NSFW mix covers, titles, etc.)
    We can either do this by injecting 'safe_browse=1' into any search OR let the user set it in their settings. Feature Coming Later.
    '''
    pass

def display_reviews(mixID):
    '''
    Returns the comments on a selected mix. User context ignorant.
    URL: http://8tracks.com/mixes/[mixID]/reviews.json
    
    The results are paginated and you can select the next page by adding 'per_page=[pageNO]' to the URL.
    
    Individual reviews are stored @ [u'reviews'][u'review'].
    Important information: [u'mix-id'], [u'user-id'], and [u'body'].
    '''
    reviewResponse = requests.get(URL + 'mixes/{}/reviews.json?per_page=10&api_version=2&api_key={}'.format(mixID, API))
    reviewJSON = json.loads(reviewResponse.content)
    
    print('Reviews\n')
    for userID, body in zip([x[u'id'] for x in reviewJSON[u'reviews']], [x[u'body'] for x in reviewJSON[u'reviews']]):
        print('*****\nUser {} said "{}"\n*****'.format(userID, body))
    print('\n')
    
def post_review(username="blank", password="blank", mixID="blank", body="STupid test"):
    '''
    Authenticates, then posts a user comment. User context aware.
    URL: http://8tracks.com/reviews.json
    DATA: "review[mix_id]=[mixID]&review[body]=STRING THAT USER TYPED IN"
    AUTH Method: requests.auth() OR http://www.python-requests.org/en/latest/user/advanced/#custom-authentication
    '''
    print("User clicked submit with '{}' as it's review. worked!".format(body))

def toggle_like(username, password, mixID):
    '''
    Authenticates, then likes a mix. User context aware.
    URL: http://8tracks.com/mixes/[mixID]/toggle_like.json
    DATA: ''
    AUTH Method: requests.auth() OR http://www.python-requests.org/en/latest/user/advanced/#custom-authentication
    '''
    pass

def toggle_favorite(username, password, trackID):
    '''
    Authenticates, then favorites a track. User context aware.
    URL: http://8tracks.com/tracks/[trackID]/toggle_like.json
    DATA: ''
    AUTH Method: requests.auth() OR http://www.python-requests.org/en/latest/user/advanced/#custom-authentication
    '''
    pass

def toggle_follow(username, password, userID):
    '''
    Authenticates, then follows a user. User context aware.
    URL: http://8tracks.com/users/[userID]/toggle_follow.json
    DATA: ''
    AUTH Method: requests.auth() OR http://www.python-requests.org/en/latest/user/advanced/#custom-authentication
    '''
    pass

def list_favorites():
    # *****
    # This needs to list all favorited tracks for logged in user.
    # *****
    print("Oh you know, that one you like.")

def list_liked_mixes():
    # *****
    # This needs to list all liked mixes for logged in user.
    # *****
    print("Oh you know, that one you like.")