import requests
import configparser
import base64

config = configparser.ConfigParser()
config.read('config.ini')


SPOTIFY_CLIENT_ID = config['Spotify']['ClientID']
SPOTIFY_CLIENT_SECRET = config['Spotify']['CLientSecret']
SPOTIFY_ACCESS_TOKEN = config['Spotify']['AccessToken']
# REDIRECT_URI = "https://localhost:9090/callback"



def checkAccessToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_ACCESS_TOKEN) -> requests.models.Response:
    auth_url = 'https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju' # Carly Rae Jepsen Artist Page

    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    header = {
        'Authorization' : f'Bearer {SPOTIFY_ACCESS_TOKEN}'
        }

    r = requests.get(auth_url, headers=header)

    return r


check_access_token = checkAccessToken(SPOTIFY_CLIENT_ID=SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET=SPOTIFY_CLIENT_SECRET, SPOTIFY_ACCESS_TOKEN=SPOTIFY_ACCESS_TOKEN)


def GenerateAccessToken(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) -> str:
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }

    response = requests.post(url=url, data=data)
    access_token = response.json().get('access_token')

    return access_token

if check_access_token.status_code != 200: # Checks if the access token is still valid
    SPOTIFY_ACCESS_TOKEN = GenerateAccessToken(SPOTIFY_CLIENT_ID=SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET=SPOTIFY_CLIENT_SECRET)
    config['Spotify'] = {
        'ClientID' : SPOTIFY_CLIENT_ID,
        'ClientSecret' : SPOTIFY_CLIENT_SECRET,
        'AccessToken': SPOTIFY_ACCESS_TOKEN
        }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)
