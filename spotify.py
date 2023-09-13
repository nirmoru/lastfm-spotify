import requests
import config_local
import configparser
import base64
import webbrowser
from urllib.parse import urlparse, parse_qs


CONST_URL = 'https://api.spotify.com/'


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
                            ) -> None:

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

    return None


"""
Code for config file ends here
"""


"""
Code for authentication token begins here
"""


def create_authentication_token(client_id) -> str:
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
    print(f"""\033[92mUser authentication requires interaction with your
web browser. Once you enter your credentials and
give authorization, you will be redirected to
a url.  Paste that url you were directed to to
complete the authorization.\033[00m


{auth_url} 
\033[92mClick on the above link if a browser doesn't open.


Enter the URL you were redirected to: \033[00m""")

    aaa = input()
    parsed_url = urlparse(aaa)
    captured_value = parse_qs(parsed_url.query)['code'][0]

    return captured_value


def get_refresh_token(authentication_token) -> str:
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.urlsafe_b64encode((config_local.SPOTIFY_CLIENT_ID + ':' + config_local.SPOTIFY_CLIENT_SECRET).encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(auth_header.decode())
    }

    payload = {
        'grant_type': 'authorization_code',
        'code': authentication_token,
        'redirect_uri': 'https://open.spotify.com/collection/playlists',
    }

    access_token_request: str = requests.post(url=token_url, data=payload, headers=headers)

    return access_token_request.json()['refresh_token']


def authentication_token(refresh_token) -> requests.models.Response:
    url = 'https://accounts.spotify.com/api/token'
    client_id = config_local.SPOTIFY_CLIENT_ID
    client_secret = config_local.SPOTIFY_CLIENT_SECRET
    auth_header = base64.urlsafe_b64encode((client_id + ':' + client_secret).encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(auth_header.decode())
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url=url, headers=headers, params=data)

    return response


"""
Code for authentication token ends here
"""


"""
Code for access token starts here
"""

def check_access_token(access_token) -> requests.models.Response:
    auth_url = 'https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju' # Carly Rae Jepsen Artist Page

    header = {
        'Authorization': 'Bearer {}'.format(access_token),
        }

    response = requests.get(url=auth_url, 
                            headers=header)

    return response


def generate_access_token(client_id, client_secret) -> requests.models.Response:
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post(url=url, 
                            data=data)
    
    return response

    # access_token = response.json().get('access_token')

    # return access_token



"""
Code for spotify API calls that require authentication token starts here
"""


def create_playlist(
        refresh_token,
        spotify_userid,
        playlist_name='New Playlist', 
        playlist_description='New Playlist description'
    ) -> requests.models.Response:

    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/users/{}/playlists'.format(spotify_userid)
    url = CONST_URL + endpoint

    header = {
            'Authorization': 'Bearer {}'.format(auth_token),
            'Content-Type': 'application/json'
        }

    payload = {
            'name': playlist_name,
            'description': playlist_description,
            'public': 'false'
        }
    
    response = requests.post(
                        url=url, 
                        headers=header, 
                        json=payload
                    )
    
    return response



def fetch_playlist(refresh_token, spotify_userid) -> requests.models.Response:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/me/playlists?limit=50'.format(spotify_userid)
    url = CONST_URL + endpoint

    header = {
            'Authorization': 'Bearer {}'.format(auth_token),
            'Content-Type': 'application/json'
        }
    
    response = requests.get(
                        url= url,
                        headers=header
                    )

    return response



def get_top_items(refresh_token) -> requests.models.Response:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']
    
    endpoint = 'v1/me/top/artists'
    url = CONST_URL + endpoint

    header = {
        'Authorization': 'Bearer {}'.format(auth_token)
    }

    response = requests.get(url=url, headers=header)

    return response


def add_item_to_playlist(playlist_id, track_uri, refresh_token) -> requests.models.Response:
    auth_token = authentication_token(refresh_token=refresh_token).json()['access_token']

    endpoint = 'v1/playlists/{}/tracks'.format(playlist_id)
    url = CONST_URL + endpoint

    header = {
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

    response = requests.post(url=url, headers=header, json=data, params=param)
    print(response.history)

    return response

"""
Code for spotify API calls that require authentication token ends here
"""


"""
Code for spotify API calls that require access token starts here
"""


def get_track_uri(track_name, 
                artist_name, 
                access_token) -> requests.models.Response:
    
    endpoint = 'v1/search?q=remaster%2520track:{}%2520artist:{}&type=track%2Cartist'.format(track_name, artist_name)
    url = CONST_URL + endpoint
    header = {
        'Authorization' : 'Bearer {}'.format(access_token)
    }

    response = requests.get(url=url, 
                            headers=header)
    
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


if __name__ == "__main__":
    if config_local.SPOTIFY_REFRESH_TOKEN == "0" or authentication_token(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN).status_code != 200:
        auth_token = create_authentication_token(client_id=config_local.SPOTIFY_CLIENT_ID)
        refresh_token = get_refresh_token(authentication_token=auth_token)

        write_to_config_spotify(spotify_refresh_token=refresh_token)

        print("\033[91mNew Refresh token generated.\nRestart the script.\033[00m")
        exit(0)


    pl_list = fetch_playlist(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN, 
                            spotify_userid=config_local.SPOTIFY_USERID)


    for _, items in enumerate(pl_list.json()['items']):
        match items['id']:
            case config_local.SPOTIFY_PLAYLISTID:
                print("\033[092mPlaylist is present.\n \033[00m")
                break
            case _:
                print("\033[91mPLaylist not Present.\nCreating Playlist.\n\033[00m")

                playlist_id = create_playlist(refresh_token=config_local.SPOTIFY_REFRESH_TOKEN,
                                spotify_userid=config_local.SPOTIFY_USERID).json()['id']
                

                write_to_config_spotify(spotify_playlistid=playlist_id)

                print("\033[092mPlaylist created.\n\033[00m")
                break

                
    access_token_status = check_access_token(
                                            access_token=config_local.SPOTIFY_ACCESS_TOKEN
                                            ).status_code
    
    if access_token_status != 200:
        access_token_response = generate_access_token(client_id=config_local.SPOTIFY_CLIENT_ID ,
                                                    client_secret=config_local.SPOTIFY_CLIENT_SECRET)
        access_token = access_token_response.json()['access_token']

        write_to_config_spotify(spotify_access_token=access_token)

        print("\033[91mNew access token generated.\nRestart the script.\033[00m")
        exit(0)
    

    print(add_item_to_playlist(playlist_id=config_local.SPOTIFY_PLAYLISTID,
                                track_uri='spotify:track:4VCHRpdNsRh1h1hm4gZoEV',
                                refresh_token=config_local.SPOTIFY_REFRESH_TOKEN).text)