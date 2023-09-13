import requests
import os
import config_local
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


def lastfm_get(payload) -> requests.models.Response:
    url = 'https://ws.audioscrobbler.com/2.0/'
    headers = {'user-agent': config_local.USER_AGENT}


    payload['api_key'] = config_local.LAST_API_KEY
    payload['format'] = 'json'


    response = requests.get(url=url, headers=headers, params=payload)

    return response

    """Usage
    payload = {
    'artist' : 'Carly Rae Jepsen',
    'album' : 'The Loveliest Time',
    'method' : 'album.getInfo',url = f"https://www.last.fm/player/station/user/{config_local.LASTFM_USERNAME}/recommended"
}
    lastfm_get(payload=payload).json()
    """


def lastfm_get_recommended() -> dict:
    url = f"https://www.last.fm/player/station/user/{config_local.LASTFM_USERNAME}/recommended"

    response = requests.get(url).json()

    recommended_playlist = response['playlist']

    track_artist_map = {}

    for i, j in enumerate(recommended_playlist):
        track_artist_map[recommended_playlist[i]['artists'][0]['_name']] = recommended_playlist[i]['_name']
    
    return track_artist_map



if __name__ == '__main__':
    pass