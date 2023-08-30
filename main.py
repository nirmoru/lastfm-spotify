import requests
import json
import configparser
import os


config = configparser.ConfigParser()


def create_ConfigFile() -> None:
    config['last.fm'] = {
        'APIkey' : 0,
        'Sharedsecret' : 0
    }
    config['Spotify'] = {
        'ClientID' : 0,
        'ClientSecret' : 0,
        'AccessToken' : 0
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)

    return None


if os.path.isfile('config.ini') == False:
    create_ConfigFile()
    print('You need to fill out the API key and Client ID for last.fm and Spotify')
    exit(0)


config.read('config.ini')
LAST_API_KEY = config['last.fm']['APIkey']
SPOTIFY_CLIENT_ID = config['Spotify']['ClientID']
SPOTIFY_USERNAME = 'Zek'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'


def lastfm_get(payload) -> requests.models.Response:
    url = 'https://ws.audioscrobbler.com/2.0/'
    headers = {'user-agent': USER_AGENT}


    payload['api_key'] = LAST_API_KEY
    payload['format'] = 'json'


    response = requests.get(url=url, headers=headers, params=payload)

    return response


def pretty_print(obj) -> dict:
    text = json.dumps(obj, sort_keys=True, indent=4)
    return json.loads(text)


payload = {
    'artist' : 'Carly Rae Jepsen',
    'album' : 'The Loveliest Time',
    'method' : 'album.getInfo',
}

r = lastfm_get(payload=payload)
r_json = r.json()
print(type((pretty_print(r_json))))