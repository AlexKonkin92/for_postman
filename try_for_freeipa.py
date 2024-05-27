#проверка по почте

import smtplib
from email.mime.text import MIMEText

# from ipalib import api

# api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
# api.finalize()
# api.Backend.rpcclient.connect()

#from ipalib import create_api, rpc


# api = create_api(mode=None)
# api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
# client = rpc.jsonclient(api)
# client.finalize()
# client.connect()

from ipalib import Command, create_api, rpc, parameters, Str, Flag
from ipalib.plugable import Registry
from ipalib.frontend import Local


# Определяем кастомную команду как пример
class my_command(Command):
    __doc__ = 'Example command'

    takes_params = (
        Str('example_param', cli_name='example_param', label='Example Param'),
    )

    has_output = (
        Str('result', label='Result'),
    )

    def execute(self, *args, **kwargs):
        return dict(result="Example result")


api = create_api(None)
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')

# Регистрация кастомных команд
registry = Registry()
registry.register(api, my_command)

api.finalize()

client = rpc.jsonclient(api)
client.finalize()
client.connect()


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
        
def reset_password():
    email = "ya.alexgr4@yandex.ru"
    user_username, user_email = valid_user(email)
    new_password = generate_password()
    print(f"Сгенерированный пароль: {new_password}")
    send_email(user_email, new_password)
    print("Пароль отправлен на почту.")

    try:
        api.Command.user_mod(user_username, userpassword=new_password)  # , krbpasswordexpiration='2025-12-31T23:59:59Z')
        print(f"Пароль для пользователя '{user_username}' был изменен.")
    except Exception as e:
        print(f"Возникла ошибка с '{user_username}': {e}")
        
if __name__ == "__main__":
    reset_password()