import requests
from bs4 import BeautifulSoup
import re
import config_local


LOGIN_URL = 'https://www.last.fm/login'
PROTECTED_URL = 'https://www.last.fm/home/tracks'
REFERRER_URL = 'https://www.last.fm/home/tracks'

WHITE = config_local.WHITE
RED = config_local.RED
GREEN = config_local.GREEN
BLUE = config_local.BLUE


def lastfm_login(username=config_local.LASTFM_USERNAME,
                password=config_local.LASTFM_PASSWORD) -> str:
    with requests.Session() as session:
        csrf_token = session.get(url=LOGIN_URL).cookies['csrftoken']
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'username_or_email': username,
            'password': password,
            }
        
        head = {
            "referer": REFERRER_URL
            }
        
        post_request = session.post(LOGIN_URL, 
                data=payload, 
                headers=head
                )

        # An authorised request.
        response = session.get(url=PROTECTED_URL)
        html_file = response.text
        return html_file


def lastfm_rec_list(html_file) -> dict[str, str]:
    soup = BeautifulSoup(html_file, 'html.parser')
    recs = soup.find_all('li', class_ = 'recs-feed-item--track')
    result = {}
    
    for rec in recs:
        finds_tracks = rec.find(class_ = 'link-block-target').get_text()
        find_tracks_filtered = re.sub(r'\(\d*:\d*\)', '', finds_tracks)
        find_tracks_filtered = re.sub(r'(\s){2,}', '', find_tracks_filtered)

        finds_artist = rec.find(class_ = 'recs-feed-description').get_text().replace('\n', '')
        find_artist_filtered = re.sub(r'(\d*,){1,}(\d*) (listeners)', '', finds_artist)
        find_artist_filtered = re.sub(r'(\s){2,}', '', find_artist_filtered).replace('\n', '')

        result[find_artist_filtered] = find_tracks_filtered
    

    return result


def lastfm_check(username=config_local.LASTFM_USERNAME,
                password=config_local.LASTFM_PASSWORD) -> tuple[bool, str]:
    if username == '0' or password == '0':
        return (False, '\033[91mUpdate last.fm credentials at config.ini.\n\033[00m')
    with requests.Session() as session:
        csrf_token = session.get(url=LOGIN_URL).cookies['csrftoken']
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'username_or_email': username,
            'password': password,
            }
        
        head = {
            "referer": REFERRER_URL
            }
        
        post_request = session.post(url=LOGIN_URL, 
                data=payload, 
                headers=head
                )

    html_file_post = post_request.text
    
    soup = BeautifulSoup(html_file_post, 'html.parser')
    try:
        failed_login = soup.find('div', class_ = 'alert-danger').get_text()
        return (False, '{}Username or password for last.fm is wrong.\n{}'.format(RED, WHITE))
    except AttributeError:
        return (True, '{}Login to last.fm is Succesful.\n{}'.format(GREEN, WHITE))



def main() -> None:
    lastfm_check_creds = lastfm_check(username=config_local.LASTFM_USERNAME,
                password=config_local.LASTFM_PASSWORD)
    if lastfm_check_creds[0] == False:
        print(lastfm_check_creds[1])
        exit(0)
    else:
        print(lastfm_check_creds[1])

    return None


if __name__ =='__main__':
    main()