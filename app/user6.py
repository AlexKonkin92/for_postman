#проверка по почте

import smtplib
from email.mime.text import MIMEText
import logging #
import threading #
from ipalib import api #
#from  sendmail_project.ipa_api import bootstrap_ipa_api

# logging.basicConfig(level=logging.WARNING)
# logging.warning(f"before initialization_lock: {threading.current_thread()}")
# initialization_lock = threading.Lock() #
# logging.warning(f"after initialization_lock: {threading.current_thread()}")

# with initialization_lock:
#     if 'finalize' in api._API__done:
#         logging.warning('IPA API is already bootstrapped.')
#     else:
#         logging.warning(threading.current_thread())
#         logging.warning('Bootstrapping IPA API.')
#         api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works' , in_server=True)
#         api.finalize()
#         if api.env.in_server:
#             api.Backend.ldap2.connect()
#         else:
#             api.Backend.rpcclient.connect()
# logging.warning(f"after with initialization_lock: {threading.current_thread()}")
#IPA_API = bootstrap_ipa_api()
#logging.warning(f'without func: {IPA_API._API__done}')

api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()
api.Backend.rpcclient.connect()

def generate_password():
    return "new_password"
    
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
        
def reset_password():
    email = "ya.alexgr4@yandex.ru"
    user_username = "alex"
    #user_username, user_email = valid_user(email)
    new_password = generate_password()
    send_email(email, new_password)
    api.Command.user_mod(user_username, userpassword=new_password)
    try:
        logging.warning('password sent.')
        return True, "Пароль успешно изменен и отправлен на электронную почту."
    except Exception as e:
        logging.warning('error sending password.')
        return False, str(e)