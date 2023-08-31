import requests
import configparser
import json


config = configparser.ConfigParser()
config.read('config.ini')


SPOTIFY_CLIENT_ID = config['Spotify']['ClientID']
SPOTIFY_CLIENT_SECRET = config['Spotify']['CLientSecret']
SPOTIFY_ACCESS_TOKEN = config['Spotify']['AccessToken']
# REDIRECT_URI = "https://localhost:9090/callback"



def check_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    auth_url = 'https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju' # Carly Rae Jepsen Artist Page

    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    header = {
        'Authorization' : f'Bearer {SPOTIFY_ACCESS_TOKEN}'
        }

    response = requests.get(auth_url, headers=header)

    return response


access_token_response = check_access_token(  SPOTIFY_CLIENT_ID=SPOTIFY_CLIENT_ID, 
                                        SPOTIFY_CLIENT_SECRET=SPOTIFY_CLIENT_SECRET, 
                                        SPOTIFY_ACCESS_TOKEN=SPOTIFY_ACCESS_TOKEN)


def generate_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) -> str:
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(url=url, data=data)
    access_token = response.json().get('access_token')

    return access_token


if access_token_response.status_code != 200: # Check if the access token is still valid
    SPOTIFY_ACCESS_TOKEN = generate_access_token(SPOTIFY_CLIENT_ID=SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET=SPOTIFY_CLIENT_SECRET)
    config['Spotify'] = {
        'ClientID' : SPOTIFY_CLIENT_ID,
        'ClientSecret' : SPOTIFY_CLIENT_SECRET,
        'AccessToken': SPOTIFY_ACCESS_TOKEN
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)


def get_track_id(TRACK_NAME, ARTIST_NAME, SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    url = 'https://api.spotify.com/v1/search?q=remaster%2520'
    header = {
        'Authorization' : f'Bearer {SPOTIFY_ACCESS_TOKEN}'
    }
    
    payload = {
        'track' : f'{TRACK_NAME}',
        'artist' : f'{ARTIST_NAME}',
        'type' : 'track,artist'
    }

    response = requests.get(url=url, headers=header, params=payload)

    response_json = json.loads(response.text)
    
    return response_json['tracks']['items'][0]['id']

    """
    get_track_id(   TRACK_NAME='Emotion', 
                    ARTIST_NAME='Carly Rae Jepsen', 
                    SPOTIFY_ACCESS_TOKEN=SPOTIFY_ACCESS_TOKEN)
    """
