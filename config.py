import os

class Config():
    AUTH_URL = os.environ.get('AUTH_URL')

    JSON_RPC_URL = os.environ.get('JSON_RPC_URL')
    MY_POST = os.environ.get('MY_POST')
    REFERER = os.environ.get('REFERER')
    SMTP_PROVIDER = os.environ.get('SMTP_PROVIDER')
    SESSION_CACHE = os.environ.get('SESSION_CACHE')
    ADMIN_USER = os.environ.get('ADMIN_USER')
    ADMIN_PASS = os.environ.get('ADMIN_PASS')
    VERIFY_SSL = os.environ.get('VERIFY_SSL')







