import config_local
try:
    import last_fm
    import spotify
except AttributeError:
    exit(0)

WHITE = config_local.WHITE
RED = config_local.RED
GREEN = config_local.GREEN
BLUE = config_local.BLUE


def add_recs_to_playlist() -> bool:
    lastfm_rec_html = last_fm.lastfm_login()
    recommendation_list = last_fm.lastfm_rec_list(html_file=lastfm_rec_html)
    
    for _, artist_name in enumerate(recommendation_list):
        track_name = recommendation_list.get(artist_name)
        spotify_track_uri = spotify.get_track_uri(track_name=track_name,
                                                artist_name=artist_name).json()['tracks']['items'][0]['uri']
        
        item_to_playlist_status = spotify.add_item_to_playlist(track_uri=spotify_track_uri)
        if item_to_playlist_status == False:
            print("{}Failed to add {} by {} to the playlist.\n{}".format(RED, track_name, artist_name, WHITE))
        else:
            print("{}Added {} by {} to the playlist.\n{}".format(BLUE, track_name, artist_name, WHITE))
    
    return (True, "{}Finished adding items to the playlsit\n.{}".format(GREEN, WHITE))


def main():
    spotify.main()
    last_fm.main()
    rec_print = add_recs_to_playlist()
    if rec_print == True:
        print(rec_print[1])


if __name__ == '__main__':
    main()
    
