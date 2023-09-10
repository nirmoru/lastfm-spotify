import configparser


config = configparser.ConfigParser()
config.read('config.ini')


SPOTIFY_CLIENT_ID = config['Spotify']['ClientID']
SPOTIFY_CLIENT_SECRET = config['Spotify']['CLientSecret']
SPOTIFY_ACCESS_TOKEN = config['Spotify']['AccessToken']
SPOTIFY_USERID = config['Spotify']['SpotifyUserID']
SPOTIFY_PLAYLISTID = config['Spotify']['PlaylistID']
SPOTIFY_REFRESH_TOKEN = config['Spotify']['RefreshToken']
REDIRECT_URI = "https://localhost:9090/callback"
LAST_API_KEY = config['last.fm']['APIkey']
LASTFM_USERNAME = config['last.fm']['LastFmUsername']
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'