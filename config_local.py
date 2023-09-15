import configparser


config = configparser.ConfigParser()
config.read('config.ini')


def create_config_file() -> bool:
    config['last.fm'] = {
        'LastFMUsername' : 0,       # last.fm Username      (Needs to be entered manually)
        'LastFMPassword' : 0,       # last.fm Password      (Needs to be entered manually)
    }
    config['Spotify'] = {
        'ClientID' : 0,             # Spotify Client ID     (Needs to be entered manually)
        'ClientSecret' : 0,         # Spotify Client Secret (Needs to be entered manually)
        'AccessToken' : 0,          # Spotify Access Token  (Auto Generated)
        'SpotifyUserID' : 0,        # Spotify UserID        (Auto Generated)
        'playlistid': 0,            # Spotify Playlist ID   (Auto Generated)
        'refreshtoken': 0,          # Spotify Refresh Token (Auto Generated)
    }

    with open('config.ini', 'w') as configFile:
        config.write(configFile)

    return True


def check_config_file() -> tuple[bool, str]:
    try:
        with open('config.ini', 'r') as config_file:
            config.read_file(config_file)
            return (True, '\033[92mConfig File found.\n\033[00m')
    except FileNotFoundError:
        create_config_file()
        return (False, '\033[91mYou need to fill out the API key and Client ID for last.fm and Spotify.\n\033[00m')
        exit(0)
    
    return None


WHITE = '\033[00m'  # Default
RED = '\033[91m'    # Error
GREEN = '\033[92m'  # Successful
BLUE = '\033[94m'   # Ongoing


try:
    ### Spotify
    SPOTIFY_CLIENT_ID = config['Spotify']['ClientID']
    SPOTIFY_CLIENT_SECRET = config['Spotify']['CLientSecret']
    SPOTIFY_ACCESS_TOKEN = config['Spotify']['AccessToken']
    SPOTIFY_USERID = config['Spotify']['SpotifyUserID']
    SPOTIFY_PLAYLISTID = config['Spotify']['PlaylistID']
    SPOTIFY_REFRESH_TOKEN = config['Spotify']['RefreshToken']
    SPOTIFY_REDIRECT_URI = "https://open.spotify.com/collection/playlists"


    ### Last.fm
    LASTFM_USERNAME = config['last.fm']['LastFmUsername']
    LASTFM_PASSWORD = config['last.fm']['lastfmPassword']
except KeyError:
    print(check_config_file()[1])

