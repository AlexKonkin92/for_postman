from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from ipalib import api

app = Flask(__name__)

api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()
api.Backend.rpcclient.connect()

def generate_password():
    return "new_password"

def valid_user(email):
    try:
        result = api.Command.user_find(mail=email)['result']
        if result:
            user_username = result[0]['uid'][0]
            return user_username,email
    except Exception as e:
        print(f"Пользователь с почтой '{email}' не был найден. Ошибка {e}.")

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
# @app.route('/')   
# def reset_password():
#     email = "ya.alexgr4@yandex.ru"
#     new_password = generate_password()
#     #print(f"Сгенерированный пароль: {new_password}")
#     send_email(email, new_password)
#     return f"Пароль отправлен на почту {email}"

# @app.route('/', methods=['GET'])   
# def reset_password():
#     email = request.args.get('email')
#     new_password = generate_password()
#     #print(f"Сгенерированный пароль: {new_password}")
#     send_email(email, new_password)
#     return f"Пароль отправлен на почту {email}"

# @app.route('/', methods=['POST'])   
# def reset_password():
#     data = request.get_json()
#     email = data.get('email')
#     #email = "ya.alexgr4@yandex.ru"
#     new_password = generate_password()
#     #print(f"Сгенерированный пароль: {new_password}")
#     send_email(email, new_password)
#     return f"Пароль отправлен на почту {email}"

@app.route('/reset_email_password', methods=['GET'])   
def reset_password():
    email = request.args.get('email')
    user_username, user_email = valid_user(email)
    new_password = generate_password()
    #print(f"Сгенерированный пароль: {new_password}")
    send_email(email, new_password)
    api.Command.user_mod(user_username, userpassword=new_password)
    return f"Пароль отправлен на почту {email}"

# @app.route('/check')   
# def check():
#     return 'ok'

        
if __name__ == "__main__":
    app.run(debug=True)