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
    session.headers.update({'referer': Config.REFERER})
    data = {
        'user': Config.ADMIN_USER,
        'password': Config.ADMIN_PASS
    }
    try:
        response = session.post(Config.AUTH_URL, headers=session.headers, data=data, verify=Config.VERIFY_SSL)
        return session
    except RequestException as e:
         raise Exception('Authentication failed') from e

def generate_password():
    return "new_password"

# def generate_password(length=12):
#     alphabet = string.ascii_letters + string.digits
#     password = ''.join(secrets.choice(alphabet) for i in range(length))
#     return password

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
        response = session.post(Config.JSON_RPC_URL, json=user_find_payload, headers=session.headers, verify=Config.VERIFY_SSL)
        response.raise_for_status()
        user = response.json()['result']['result']
        if user:
            return user[0]['uid'][0]
    except RequestException as e:
        app.logger.error(f"User not found: {e}")

def send_email(recipient, password):
    sender = Config.MY_POST
    message = f"Временный пароль: {password}" 
    msg = MIMEText(message)
    
    msg['Subject'] = 'Временный пароль для FreeIPA'
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL(Config.SMTP_PROVIDER, Config.SMTP_PORT) as server:
        server.login(sender, Config.SMTP_PASSWORD)
        server.sendmail(sender, recipient, msg.as_string())

@app.route('/reset_email_password', methods=['POST'])   
def reset_password():
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
        response = session.post(Config.JSON_RPC_URL, json=user_mod_payload, headers=session.headers, verify=Config.VERIFY_SSL)
        response.raise_for_status()
        send_email(email, new_password)
        return f"Password sent to the mail {email}"
    except RequestException as e:
        app.logger.error(f"Error modifying user: {e}")

@app.route('/healthcheck')   
def check():
    return 'ok'