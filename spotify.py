import requests
import config_local
import configparser
import base64
import webbrowser
from urllib.parse import urlparse, parse_qs


config = configparser.ConfigParser()
config.read('config.ini')


def create_authentication_token() -> str:
    url = 'https://accounts.spotify.com/authorize'
    payload = {
            'client_id': CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': 'https://open.spotify.com/collection/playlists',
            'scope': 'playlist-modify-private playlist-modify-public user-read-private user-read-email',
        }
    response = requests.get(url=url, params=payload)

    auth_url = response.history[0].url
    webbrowser.open(url, new=0, autoraise=True)
    print( f"""User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.


    Opening {url} in your browser


    Enter the URL you were redirected to:""")

    aaa = input()
    parsed_url = urlparse(aaa)
    captured_value = parse_qs(parsed_url.query)['code'][0]

    return captured_value


def get_refresh_token(authentication_token) -> dict:
    auth_header = base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic {}'.format(auth_header.decode())
    }

    payload = {
        'grant_type': 'authorization_code',
        'code': authentication_token,
        'redirect_uri': 'https://open.spotify.com/collection/playlists',
    }

    access_token_request = requests.post(url=TOKEN_URL, data=payload, headers=headers)

    return access_token_request.json()


def authentication_token(REFRESH_TOKEN) -> str:
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
        'refresh_token': REFRESH_TOKEN
    }
    response = requests.post(url=url, headers=headers, params=data)

    return response.json()['access_token']


def check_access_token(SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    auth_url = 'https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju' # Carly Rae Jepsen Artist Page

    header = {
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}',
        }

    response = requests.get(
                        url=auth_url, 
                        headers=header
                        )

    return response


def generate_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) -> str:
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(
                            url=url, 
                            data=data
                        )

    access_token = response.json().get('access_token')

    return access_token


def write_to_config_spotify(
        SPOTIFY_CLIENT_ID=config_local.SPOTIFY_CLIENT_ID, 
        SPOTIFY_CLIENT_SECRET=config_local.SPOTIFY_CLIENT_SECRET, 
        SPOTIFY_ACCESS_TOKEN=config_local.SPOTIFY_ACCESS_TOKEN, 
        SPOTIFY_USERID=config_local.SPOTIFY_USERID,
        SPOTIFY_PLAYLISTID=config_local.SPOTIFY_PLAYLISTID
    ) -> None:

    config['Spotify'] = {
        'ClientID' : SPOTIFY_CLIENT_ID,
        'ClientSecret' : SPOTIFY_CLIENT_SECRET,
        'AccessToken': SPOTIFY_ACCESS_TOKEN,
        'SpotifyUserID': SPOTIFY_USERID,
        'PlaylistID': SPOTIFY_PLAYLISTID
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)

    return None


def get_track_id(TRACK_NAME, ARTIST_NAME, SPOTIFY_ACCESS_TOKEN) -> str:
    url = 'https://api.spotify.com/v1/search?q=remaster%2520'
    header = {
        'Authorization' : f'Bearer {SPOTIFY_ACCESS_TOKEN}'
    }
    
    payload = {
        'track' : f'{TRACK_NAME}',
        'artist' : f'{ARTIST_NAME}',
        'type' : 'track,artist'
    }

    response = requests.get(url=url, 
                            headers=header, 
                            params=payload
                        )

    response_json = response.json()
    
    return response_json['tracks']['items'][0]['id']

    """
    get_track_id(   TRACK_NAME='Emotion', 
                    ARTIST_NAME='Carly Rae Jepsen', 
                    SPOTIFY_ACCESS_TOKEN=SPOTIFY_ACCESS_TOKEN)
    """


def create_playlist(
        REFRESH_TOKEN,
        SPOTIFY_USERID,
        playlist_name='New Playlist', 
        playlist_description='New Playlist description'
    ) -> dict:

    access_token = authentication_token(REFRESH_TOKEN=REFRESH_TOKEN)

    url = 'https://api.spotify.com/v1/users/{}/playlists'.format(SPOTIFY_USERID)

    header = {
            'Authorization': 'Bearer {}'.format(access_token),
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
    
    return response.json()




if __name__ == '__main__':
    REFRESH_TOKEN = config_local.SPOTIFY_REFRESH_TOKEN
    # access_token_response = check_access_token(SPOTIFY_ACCESS_TOKEN=config_local.SPOTIFY_ACCESS_TOKEN)
    

    # if access_token_response.status_code != 0: # Check if the access token is still valid
    #     SPOTIFY_ACCESS_TOKEN = generate_access_token(
    #                                     SPOTIFY_CLIENT_ID=config_local.SPOTIFY_CLIENT_ID, 
    #                                     SPOTIFY_CLIENT_SECRET=config_local.SPOTIFY_CLIENT_SECRET
    #                                 )

    #     # print(SPOTIFY_ACCESS_TOKEN)
    #     write_to_config_spotify(SPOTIFY_ACCESS_TOKEN=SPOTIFY_ACCESS_TOKEN)

    # if config_local.SPOTIFY_PLAYLISTID == '0':
    #     create_playlist(
    #                 REFRESH_TOKEN=REFRESH_TOKEN,
    #                 SPOTIFY_USERID=config_local.SPOTIFY_USERID, 
    #                 playlist_name='New Playlist', 
    #                 playlist_description='New Playlist description'
    #             )