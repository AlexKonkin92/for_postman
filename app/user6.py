#проверка по почте

import smtplib
from email.mime.text import MIMEText
from ipalib import api

if not api.isdone('bootstrap'):
    api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
    api.finalize()
    api.Backend.rpcclient.connect()

def generate_password():
    return "new_password"

def valid_user(email):
    try:
        api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
        api.finalize()
        api.Backend.rpcclient.connect()
        result = api.Command.user_find(mail=email)['result']
        if result:
            user_username = result[0]['uid'][0]
            return user_username,email
    except Exception as e:
        return False, str(e)
    
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
        
def reset_password(email):
    #email = "ya.alexgr4@yandex.ru"
    user_username, user_email = valid_user(email)
    new_password = generate_password()
    send_email(user_email, new_password)
    api.Command.user_mod(user_username, userpassword=new_password)
    try:
        return True, "Пароль успешно изменен и отправлен на электронную почту."
    except Exception as e:
        return False, str(e)