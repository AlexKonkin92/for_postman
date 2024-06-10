import requests
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from requests.exceptions import RequestException
from config import Config


app = Flask(__name__)

#auth_url = 'https://freeipa-dev.ks.works/ipa/session/login_password'
json_rpc_url = 'https://freeipa-dev.ks.works/ipa/json'
my_post = 'ya.alexgr4@yandex.ru'
session_cache = None

def get_auth_session():
    session = requests.Session()
    session.headers.update({'referer': "https://freeipa-dev.ks.works/ipa/ui/"})
    data = {
        'user': 'admin',
        'password': 'new_password'
    }
    try:
        response = session.post(Config.AUTH_URL, headers=session.headers, data=data, verify=False)
        return session
    except RequestException as e:
         raise Exception('Authentication failed') from e

def generate_password():
    return "new_password"

def valid_user(email):
    session = get_auth_session()
    user_find_payload = {
            "method": "user_find",
            "params": [
                [""],  
                {"all": True, "mail": email}
            ],
            "id": 0
        }
    try:
        response = session.post(json_rpc_url, json=user_find_payload, headers=session.headers, verify=False)
        response.raise_for_status()
        user = response.json()['result']['result']
        if user:
            return user[0]['uid'][0]
    except RequestException as e:
        app.logger.error(f"User not found: {e}")

def send_email(recipient, password):
    sender = my_post
    message = f"Временный пароль: {password}" 
    msg = MIMEText(message)
    
    msg['Subject'] = 'Временный пароль для FreeIPA'
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(sender, 'xsegyibpinputkgo')
        server.sendmail(sender, recipient, msg.as_string())

@app.route('/reset_email_password', methods=['POST'])   
def reset_password():
    #email = request.args.get('email')
    email = request.get_json().get('email')
    print(email)
    user_username = valid_user(email)
    if user_username is None:
        return "User missing"
    session = get_auth_session()
    new_password = generate_password()
    user_mod_payload = {
    "method": "user_mod",
    "params": [
        [user_username],
        {
            "userpassword": new_password
        }
    ],
    "id": 0
}
    try:
        response = session.post(json_rpc_url, json=user_mod_payload, headers=session.headers, verify=False)
        response.raise_for_status()
        send_email(email, new_password)
        return f"Password sent to the mail {email}"
    except RequestException as e:
        app.logger.error(f"Error modifying user: {e}")

@app.route('/healthcheck')   
def check():
    return 'ok'