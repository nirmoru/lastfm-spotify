import requests
import json
import os
import config_local
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


def create_ConfigFile() -> None:
    config['last.fm'] = {
        'APIkey' : 0,
        'Sharedsecret' : 0,
        'LastFmUsername' : 0,
    }
    config['Spotify'] = {
        'ClientID' : 0,
        'ClientSecret' : 0,
        'AccessToken' : 0,
        'spotifyusername' : 0,
        'playlistid': 0,
        'refreshtoken': 0,
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)

    return None


def lastfm_get(payload) -> requests.models.Response:
    url = 'https://ws.audioscrobbler.com/2.0/'
    headers = {'user-agent': config_local.USER_AGENT}


    payload['api_key'] = config_local.LAST_API_KEY
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
# r_json = r.json()
# print(type((pretty_print(r_json))))


def lastfm_recommended(LASTFM_USERNAME) -> dict:
    url = f"https://www.last.fm/player/station/user/{config_local.LASTFM_USERNAME}/recommended"

    response = requests.get(url).text

    response_json = json.loads(response)
    playlist = response_json['playlist']

    track_artist_map = {}

    for i, j in enumerate(playlist):
        track_artist_map[playlist[i]['artists'][0]['_name']] = playlist[i]['_name']

    return track_artist_map


if __name__ == '__main__':
    if os.path.isfile('config.ini') == False:
        create_ConfigFile()
        print('\033[91mYou need to fill out the API key and Client ID for last.fm and Spotify\033[00m')
        exit(0)
