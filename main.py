if __name__ == '__main__':
    import configparser
    import last_fm
    import spotify
    import config_local
    
    
    config = configparser.ConfigParser()

    def create_config_file() -> None:
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

        with open('aaa.ini', 'w') as configFile:
            config.write(configFile)

        return None


    try:
        with open('aaa.ini', 'r') as config_file:
            config.read_file(config_file)
            print('\033[92mConfig File found.\033[00m')
    except FileNotFoundError:
        create_config_file()
        print('\033[91mYou need to fill out the API key and Client ID for last.fm and Spotify.\033[00m')
        exit(0)
    

    