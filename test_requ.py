import requests
from requests.exceptions import RequestException
from config import Config


def get_auth_session():
    session = requests.Session()
    session.headers.update({'referer': "https://freeipa-dev.ks.works/ipa/ui/"})
    data = {
        'user': 'admin',
        'password': 'new_password'
    }
    print(f"Config.AUTH_URL: {Config.AUTH_URL}")
    try:
        response = session.post(Config.AUTH_URL, headers=session.headers, data=data, verify=False)
        return session
    except RequestException as e:
         raise Exception('Authentication failed') from e
    
print(get_auth_session())