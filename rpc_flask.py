import requests
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from ipalib import api


app = Flask(__name__)

api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()
api.Backend.rpcclient.connect()

def get_authenticated_session():
    session = requests.Session()
    headers = {
        'referer': "https://freeipa-dev.ks.works/ipa/ui/",
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'user': 'admin',
        'password': 'Secret123'
    }
    auth_url = 'https://freeipa-dev.ks.works/ipa/session/login_password'
    response = session.post(auth_url, headers=headers, data=data, verify=False)
    
    if response.status_code == 200:
        return session
    else:
        raise Exception('Authentication failed')
    

def generate_password():
    return "new_password"

def valid_user(email):
    session = get_authenticated_session()
    try:
        
        user_find_payload = {
            "method": "user_find",
            "params": [
                [""],  
                {"all": True, "mail": email}
            ],
            "id": 0
        }
        json_rpc_url = 'https://freeipa-dev.ks.works/ipa/json'
        response = session.post(json_rpc_url, json=user_find_payload, headers=session.headers, verify=False)
        if response.json()['result']:
            user_username = response.json()['result'][0]['uid'][0]
            return user_username
        else:
            print(f"Пользователь с почтой '{email}' не был найден.")
            return None
    except Exception as e:
        print(f"Ошибка {e}.")

def send_email(recipient, password):
    sender = 'ya.alexgr4@yandex.ru'
    message = f"Временный пароль: {password}" 
    msg = MIMEText(message)
    
    msg['Subject'] = 'Временный пароль для FreeIPA' #название сообщения
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL('smtp.yandex.ru', 465) as server:
        server.login(sender, 'xsegyibpinputkgo')
        server.sendmail(sender, recipient, msg.as_string())


@app.route('/reset_email_password', methods=['GET'])   
def reset_password():
    email = request.args.get('email')
    user_username = valid_user(email)

    if user_username is None:
        return "Пользователь отсутствует"
    
    session = get_authenticated_session()
    new_password = generate_password()
    user_mod_payload = {
    "method": "user_mod",
    "params": [
        [user_username],  # Имя пользователя, которому нужно изменить пароль
        {
            "userpassword": new_password
        }
    ],
    "id": 0
}
    json_rpc_url = 'https://freeipa-dev.ks.works/ipa/json'
    response = session.post(json_rpc_url, json=user_mod_payload, headers=session.headers, verify=False)
    if response.status_code == 200:
        send_email(email, new_password)
        return f"Пароль отправлен на почту {email}"
    else:
        return "Ошибка"

@app.route('/healthcheck')   
def check():
    return 'ok'

        
if __name__ == "__main__":
    app.run(debug=True)