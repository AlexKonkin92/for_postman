import requests
from flask import Flask, request, jsonify
from requests.exceptions import HTTPError
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from config import Config
import secrets
import string


app = Flask(__name__)


class UserValidationError(Exception):
    pass


@app.route('/reset_email_password', methods=['POST'])
def reset_password_view():
    if not (email := request.get_json().get('email')):
        return jsonify({'error': 'email not provided'}), 400

    try:
        session = get_auth_session()
        username = validate_user(email, session)
        new_password = generate_password()
        reset_password(username, new_password, session)
        send_email(email, new_password)
    except HTTPError as e:
        return jsonify({'error': f"HTTP error during authentication or user validation: {str(e)}"}), 400
    except UserValidationError as e:
        return jsonify({'error': f"User validation error: {str(e)}"}), 400
    except SMTPException as e:
        return jsonify({'error': f"SMTP error during email sending: {str(e)}"}), 400
    
    return jsonify({'response': f"Password sent to the mail {email}"}), 200


@app.route('/healthcheck')   
def check():
    return 'ok'


def get_auth_session():
    session = requests.Session()
    session.headers.update({'referer': Config.REFERER_URL})
    data = {
        'user': Config.ADMIN_USER,
        'password': Config.ADMIN_PASS
    }
    response = session.post(Config.AUTH_URL, data=data,  verify=Config.VERIFY_SSL)
    response.raise_for_status()
    return session


def validate_user(email: str, session: requests.Session) -> str:
    user_find_payload = {
        "method": "user_find",
        "params": [
            [""],
            {"all": True, "mail": email}
        ],
        "id": 0
    }
    response = session.post(Config.JSON_RPC_URL, json=user_find_payload,  verify=Config.VERIFY_SSL)
    response.raise_for_status()
    try:
        user = response.json()['result']['result']
        if not user or not (username := user[0]['uid'][0]):
            raise UserValidationError(f"User with email {email} not found")
    except KeyError as e:
        raise UserValidationError(f"Missing key in response: {e}")
    return username


def generate_password(length=12) -> str:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


def reset_password(username: str, new_password: str, session: requests.Session) -> str:
    user_mod_payload = {
        "method": "user_mod",
        "params": [
            [username],
            {
                "userpassword": new_password
            }
        ],
        "id": 0
    }
    response = session.post(Config.JSON_RPC_URL, json=user_mod_payload,  verify=Config.VERIFY_SSL)
    response.raise_for_status()


def send_email(recipient: str, password: str) -> None:
    sender = Config.SENDER_POST
    message = f"Временный пароль: {password}"
    msg = MIMEText(message)

    msg['Subject'] = 'Временный пароль для FreeIPA'
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL(Config.SMTP_PROVIDER, Config.SMTP_PORT) as server:
        server.login(sender, Config.SMTP_PASSWORD)
        server.sendmail(sender, recipient, msg.as_string())
