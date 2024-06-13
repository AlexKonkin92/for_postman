import os
from dotenv import load_dotenv

class Config():
    load_dotenv()
    AUTH_URL = os.environ.get('AUTH_URL')
    JSON_RPC_URL = os.environ.get('JSON_RPC_URL')
    SENDER_POST = os.environ.get('SENDER_POST')
    REFERER = os.environ.get('REFERER')
    SMTP_PROVIDER = os.environ.get('SMTP_PROVIDER')
    SMTP_PORT = os.environ.get('SMTP_PORT')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ADMIN_PASS = os.environ.get('ADMIN_PASS')
    VERIFY_SSL = os.environ.get('VERIFY_SSL').lower() in {"true", "1"}

config = Config()








