import os
from dotenv import load_dotenv

class Config():
    load_dotenv()
    DOMAIN = os.environ.get('DOMAIN')
    AUTH_URL = f'https://{DOMAIN}/ipa/session/login_password'
    JSON_RPC_URL = f'https://{DOMAIN}/ipa/json'
    SENDER_POST = os.environ.get('SENDER_POST')
    REFERER_URL = f'https://{DOMAIN}/ipa/ui/'
    SMTP_PROVIDER = os.environ.get('SMTP_PROVIDER')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ADMIN_PASS = os.environ.get('ADMIN_PASS')
    VERIFY_SSL = os.environ.get('VERIFY_SSL', 'true').lower() in {"true", "1"}

config = Config()








