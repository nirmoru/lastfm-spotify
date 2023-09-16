import requests
import config_local
import configparser
import base64
import webbrowser
from urllib.parse import urlparse, parse_qs


CONST_URL = 'https://api.spotify.com/'
WHITE = config_local.WHITE
RED = config_local.RED
GREEN = config_local.GREEN
BLUE = config_local.BLUE


"""
Code for config file starts here
"""


config = configparser.ConfigParser()
config.read('config.ini')


def write_to_config_spotify(spotify_client_id=config_local.SPOTIFY_CLIENT_ID, 
                            spotify_client_secret=config_local.SPOTIFY_CLIENT_SECRET, 
                            spotify_access_token=config_local.SPOTIFY_ACCESS_TOKEN, 
                            spotify_userid=config_local.SPOTIFY_USERID,
                            spotify_playlistid=config_local.SPOTIFY_PLAYLISTID,
                            spotify_refresh_token=config_local.SPOTIFY_REFRESH_TOKEN,
                            ) -> tuple[bool, str]:

    config['Spotify'] = {
        'ClientID' : spotify_client_id,
        'ClientSecret' : spotify_client_secret,
        'AccessToken': spotify_access_token,
        'SpotifyUserID': spotify_userid,
        'PlaylistID': spotify_playlistid,
        'RefreshToken': spotify_refresh_token,
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)

    return (True, '{}Config Successfully written.\n{}'.format(GREEN, WHITE))


"""
Code for config file ends here
"""


"""
Code for authentication token begins here
"""


def create_authentication_token(client_id=config_local.SPOTIFY_CLIENT_ID) -> str:
    url = 'https://accounts.spotify.com/authorize'
    payload = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': 'https://open.spotify.com/collection/playlists',
            'scope': 'playlist-read-private playlist-modify-private playlist-modify-public user-read-private user-read-email user-top-read',
        }
    response = requests.get(url=url, params=payload)

    auth_url = response.history[0].url
    webbrowser.open(auth_url, new=0, autoraise=True)
    print("""{}User authentication requires interaction with your
web browser. Once you enter your credentials and
give authorization, you will be redirected to
a url.  Paste that url you were directed to to
complete the authorization.{}


{} 
{}Click on the above link if a browser doesn't open.


Enter the URL you were redirected to: {}""".format(GREEN, WHITE, auth_url, GREEN, WHITE))

    aaa = input()
    parsed_url = urlparse(aaa)
    captured_value = parse_qs(parsed_url.query)['code'][0]

    return captured_value


def get_refresh_token(authentication_token, 
                    client_id=config_local.SPOTIFY_CLIENT_ID,
                    client_secret=config_local.SPOTIFY_CLIENT_SECRET,
                    redirect_uri=config_local.SPOTIFY_REDIRECT_URI) -> str:
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(auth_header.decode())
    }

    payload = {
        'grant_type': 'authorization_code',
        'code': authentication_token,
        'redirect_uri': redirect_uri,
    }

    access_token_request = requests.post(url=token_url, data=payload, headers=head)

    return access_token_request.json()['refresh_token']


def authentication_token(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> requests.models.Response:
    url = 'https://accounts.spotify.com/api/token'
    client_id = config_local.SPOTIFY_CLIENT_ID
    client_secret = config_local.SPOTIFY_CLIENT_SECRET
    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())

    head = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(auth_header.decode())
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url=url, 
                            headers=head, 
                            params=payload)

    return response


"""
Code for authentication token ends here
"""


"""
Code for access token starts here
"""

def check_access_token(access_token=config_local.SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    endpoint = 'v1/artists/6sFIWsNpZYqfjUpaCgueju' # Carly Rae Jepsen Artist Page

    auth_url = CONST_URL + endpoint
    
    head = {
        'Authorization': 'Bearer {}'.format(access_token),
        }

    response = requests.get(url=auth_url, 
                            headers=head)

    return response


def generate_access_token(client_id=config_local.SPOTIFY_CLIENT_ID, 
                        client_secret=config_local.SPOTIFY_CLIENT_SECRET) -> requests.models.Response:
    url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url=url, 
                            data=payload)
    
    return response

    # access_token = response.json().get('access_token')

    # return access_token



"""
Code for spotify API calls that require authentication token starts here
"""


def create_playlist(
        refresh_token=config_local.SPOTIFY_REFRESH_TOKEN,
        spotify_userid=config_local.SPOTIFY_USERID,
        playlist_name='New Playlist', 
        playlist_description='New Playlist description'
    ) -> requests.models.Response:

    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/users/{}/playlists'.format(spotify_userid)
    url = CONST_URL + endpoint

    head = {
            'Authorization': 'Bearer {}'.format(auth_token),
            'Content-Type': 'application/json'
        }

    payload = {
            'name': playlist_name,
            'description': playlist_description,
            'public': 'false'
        }
    
    response = requests.post( url=url, 
                        headers=head, 
                        json=payload)
    
    return response



def fetch_playlist(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN, 
                spotify_userid=config_local.SPOTIFY_USERID) -> requests.models.Response:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/me/playlists?limit=50'.format(spotify_userid)
    url = CONST_URL + endpoint

    head = {
            'Authorization': 'Bearer {}'.format(auth_token),
            'Content-Type': 'application/json'
        }
    
    response = requests.get(url= url,
                        headers=head)

    return response



def get_top_items(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> requests.models.Response:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']
    
    endpoint = 'v1/me/top/artists'
    url = CONST_URL + endpoint

    head = {
        'Authorization': 'Bearer {}'.format(auth_token)
    }

    response = requests.get(url=url, headers=head)

    return response


def add_item_to_playlist(track_uri, 
                        playlist_id=config_local.SPOTIFY_PLAYLISTID, 
                        refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> bool:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/playlists/{}/tracks'.format(playlist_id)
    url = CONST_URL + endpoint

    head = {
        'Authorization': 'Bearer {}'.format(auth_token),
        'Content-Type': 'application/json'
    }

    param = {
        'uris': '{}'.format(track_uri)
    }

    data = {
        'uris': [
            'string'
        ],
        'position': 0
    }

    response = requests.post(url=url, headers=head, json=data, params=param)
    if response.status_code != 201:
        return False
    else:
        return True


def get_items_from_playlist(playlist_id=config_local.SPOTIFY_PLAYLISTID,
                            refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> list[str]:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/playlists/{}/tracks'.format(playlist_id)
    endpoint_url = CONST_URL + endpoint

    head = {
        'Authorization': 'Bearer {}'.format(auth_token)
    }

    response = requests.get(url=endpoint_url,
                            headers=head)
    response_json = response.json()
    
    result = []

    for _, item in enumerate(response_json['items']):
        result.append(item['track']['uri'])
    
    return result




def del_item_from_playlist(track_uri, 
                            playlist_id=config_local.SPOTIFY_PLAYLISTID,
                            refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> bool:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/playlists/{}/tracks'.format(playlist_id)
    endpoint_url = CONST_URL + endpoint

    head = {
        'Authorization': 'Bearer {}'.format(auth_token),
        'Content-Type': 'application/json'
    }

    payload = {
        'tracks': [
            {
                'uri': track_uri
            }
        ]
    }

    response = requests.delete(url=endpoint_url,
                                headers=head,
                                json=payload)

    if response.status_code == 200:
        return True
    else:
        return False

    

def get_user_id(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> str:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/me'
    endpoint_url = CONST_URL + endpoint

    head = {
        'Authorization': 'Bearer {}'.format(auth_token)
    }

    response = requests.get(url=endpoint_url, 
                            headers=head)

    return response.json()['id']


"""
Code for spotify API calls that require authentication token ends here
"""


"""
Code for spotify API calls that require access token starts here
"""


def get_track_uri(track_name, 
                artist_name, 
                access_token=config_local.SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    
    endpoint = 'v1/search?q=remaster%2520track:{}%2520artist:{}&type=track%2Cartist'.format(track_name, artist_name)
    url = CONST_URL + endpoint
    head = {
        'Authorization' : 'Bearer {}'.format(access_token)
    }

    response = requests.get(url=url, 
                            headers=head)
    
    return response
    """
    Usage
    get_track_id(track_name='Emotion', 
                        artist_name='Carly Rae Jepsen', 
                        access_token=config_local.SPOTIFY_ACCESS_TOKEN).json()['tracks']['items'][0]['uri']
    """


"""
Code for spotify API calls that require access token ends here
"""

def spotify_check_refresh_token(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN,
                                client_id=config_local.SPOTIFY_CLIENT_ID) -> tuple[bool, str]:
    if refresh_token == "0" or authentication_token(refresh_token=refresh_token).status_code != 200:
        auth_token = create_authentication_token(client_id=client_id)
        refresh_token = get_refresh_token(authentication_token=auth_token)

        write_refresh_token = write_to_config_spotify(spotify_refresh_token=refresh_token)
        if write_refresh_token[0] == True:
            print(write_refresh_token[1])

        return (False, "{}New Refresh token generated.\nRestart the script.\n{}".format(RED, WHITE))
    else:
        return (True, "{}Refresh token is valid.\n{}".format(GREEN, WHITE))



def spotify_check_playlist(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN,
                        spotify_userid=config_local.SPOTIFY_USERID,
                        playlist_id=config_local.SPOTIFY_PLAYLISTID) -> tuple[bool, str]:
    ### Checks if playlist is present
    pl_list = fetch_playlist(refresh_token=refresh_token, 
                            spotify_userid=spotify_userid)

    pl_list_all = []
    for _, items in enumerate(pl_list.json()['items']):
        pl_list_all.append(items['id'])
    
    if playlist_id in pl_list_all:
        return (True, "{}Playlist is present.\n {}".format(GREEN, WHITE))
    else:
        print("{}PLaylist is not Present.\nCreating Playlist.\n{}".format(RED, WHITE))

        playlist_id = create_playlist(refresh_token,
                        spotify_userid=spotify_userid,
                        playlist_name='Last.fm Recommendations', 
                        playlist_description='Recommendations from last.fm').json()['id']
        

        write_playlist_id = write_to_config_spotify(spotify_playlistid=playlist_id)
        if write_playlist_id[0] == True:
            print(write_playlist_id[1])

        return (False, "{}Playlist created.\nRestart the script.\n{}".format(GREEN, WHITE))



def spotify_check_access_token(access_token=config_local.SPOTIFY_ACCESS_TOKEN,
                            client_id=config_local.SPOTIFY_CLIENT_ID,
                            client_secret=config_local.SPOTIFY_CLIENT_SECRET) -> tuple[bool, str]:
    ### Checks if acccess token is valid 
    access_token_status = check_access_token(access_token=access_token
                                            ).status_code
    
    if access_token_status != 200:
        access_token_response = generate_access_token(client_id=client_id,
                                                    client_secret=client_secret)
        access_token = access_token_response.json()['access_token']

        write_access_token = write_to_config_spotify(spotify_access_token=access_token)
        if write_access_token[0] == True:
            print(write_access_token[1])


        return (False, "{}New access token generated.\nRestart the script.\n{}".format(RED, WHITE))
    else:
        return (True, "{}Access token is valid.\n{}".format(GREEN, WHITE))


def spotify_check_userid(userid=config_local.SPOTIFY_USERID,
                        refresh_token=config_local.SPOTIFY_REFRESH_TOKEN) -> tuple[bool, str]:
    url = 'https://open.spotify.com/user/{}'.format(userid)

    response = requests.get(url=url)

    if response.status_code != 200:
        spotify_userid = get_user_id(refresh_token=refresh_token)
        write_to_config_spotify(spotify_userid=spotify_userid)

        return (False, "{}Invalid Userid.\nFetching Your User ID.\n{}".format(RED, WHITE))
    else:
        return (True, '{}Valid Userid.\n{}'.format(GREEN, WHITE))

def main() -> bool:
    refresh_token_response = spotify_check_refresh_token()
    if refresh_token_response[0] == False:
        print(refresh_token_response[1])
        exit(0)
    else:
        print(refresh_token_response[1])

    
    check_playlist = spotify_check_playlist()
    if check_playlist[0] == False:
        print(check_playlist[1])
        exit(0)
    else:
        print(check_playlist[1])
    

    access_token_response = spotify_check_access_token()
    if access_token_response[0] == False:
        print(access_token_response[1])
        exit(0)
    else:
        print(access_token_response[1])


    userid_response = spotify_check_userid()
    if userid_response[0] == False:
        print(userid_response[1])
        exit(0)
    else:
        print(userid_response[1])
    return True


if __name__ == "__main__":
    main()

