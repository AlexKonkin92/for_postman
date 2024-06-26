import requests
from flask import Flask, request, jsonify
from requests.exceptions import HTTPError
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from config import Config
import secrets
import string
import logging
from requests.exceptions import HTTPError

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



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
    except HTTPError as e:
        return jsonify({'error': f"HTTP error during authentication or user validation: {str(e)}"}), 400
    except UserValidationError as e:
        return jsonify({'error': f"User validation error: {str(e)}"}), 400
    except SMTPException as e:
        return jsonify({'error': f"SMTP error during email sending: {str(e)}"}), 400
    
    return jsonify({'response': f"Password sent to the mail {email}"}), 200

def get_auth_session():
    session = requests.Session()
    session.headers.update({'referer': Config.REFERER})
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
    user = response.json()['result']['result']
    user2 = response.json()['result']
    logging.debug(f"User data: {user2}")
    logging.debug(f"User data: {user}")
    if not user or not (username := user[0]['uid'][0]):
        raise UserValidationError("Missing user or user uid")
    return username