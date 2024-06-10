# import requests
# from requests.exceptions import RequestException
# from config import Config


# def get_auth_session():
#     session = requests.Session()
#     session.headers.update({'referer': "https://freeipa-dev.ks.works/ipa/ui/"})
#     data = {
#         'user': 'admin',
#         'password': 'new_password'
#     }
#     print(f"Config.AUTH_URL: {Config.AUTH_URL}")
#     try:
#         response = session.post(Config.AUTH_URL, headers=session.headers, data=data, verify=False)
#         return session
#     except RequestException as e:
#          raise Exception('Authentication failed') from e
    
# print(get_auth_session())






# import secrets
# import string

# def generate_password(length=12):
#     alphabet = string.ascii_letters + string.digits
#     password = ''.join(secrets.choice(alphabet) for i in range(length))
#     return password
# print(generate_password())

import requests
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from requests.exceptions import RequestException
from config import Config
import secrets
import string


app = Flask(__name__)

def get_auth_session():
    session = requests.Session()
    #session.headers.update({'referer': Config.REFERER})
    data = {
        'user': Config.ADMIN_USER,
        'password': Config.ADMIN_PASS
    }
    try:
        response = session.post(Config.AUTH_URL, data=data, verify=Config.VERIFY_SSL)
        return session
    except RequestException as e:
         raise Exception('Authentication failed') from e
    
print(get_auth_session())