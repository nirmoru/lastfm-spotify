# lastfm-spotify
Create Spotify playlist from last.fm recommendations.


# Usage
## Prerequisites
* You need to create an application for [Spotify](https://developer.spotify.com/dashboard).
* You need to have a [last.fm](https://last.fm) account.
* Install all of the dependencies.
```
pip install -r requirements.txt
```
## Config.ini
```
[last.fm]
lastfmusername = 0              # last.fm Username      (Needs to be entered manually)
lastfmpassword = 0              # last.fm Password      (Needs to be entered manually)

[Spotify]
clientid = 0                    # Spotify Client ID     (Needs to be entered manually)
clientsecret = 0                # Spotify Client Secret (Needs to be entered manually)
accesstoken = 0                 # Spotify Access Token  (Auto Generated)
spotifyuserid = 0               # Spotify UserID        (Auto Generated)
playlistid = 0                  # Spotify Playlist ID   (Auto Generated)
refreshtoken = 0                # Spotify Refresh Token (Auto Generated)
```

lastfmusername and lastfmpassword needs to be filled with your last.fm credentials.\
clientid and clientsecret are available on [Spotify Developer](https://developer.spotify.com/dashboard) dashboard.

## How to Use
* First 
* Then you need to run the ``main.py`` once to get the configuration file.
```
python3 main.py
```
* Then you need to fill the config.ini file as directed above.
* Running ``main.py`` once again will generate a playlist in your spotify account.

# Todo List
- [ ] Delete items from playlist when adding new items.

# Credits
[@nirmoru](https://github.com/nirmoru)


# License
This project is under MIT License.