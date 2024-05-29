from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

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
# @app.route('/')   
# def reset_password():
#     email = "ya.alexgr4@yandex.ru"
#     new_password = generate_password()
#     #print(f"Сгенерированный пароль: {new_password}")
#     send_email(email, new_password)
#     return f"Пароль отправлен на почту {email}"

@app.route('/', methods=['GET'])   
def reset_password():
    email = request.args.get('email')
    new_password = generate_password()
    #print(f"Сгенерированный пароль: {new_password}")
    send_email(email, new_password)
    return f"Пароль отправлен на почту {email}"

# @app.route('/', methods=['POST'])   
# def reset_password():
#     data = request.get_json()
#     email = data.get('email')
#     #email = "ya.alexgr4@yandex.ru"
#     new_password = generate_password()
#     #print(f"Сгенерированный пароль: {new_password}")
#     send_email(email, new_password)
#     return f"Пароль отправлен на почту {email}"

        
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)