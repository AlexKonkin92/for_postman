from ipalib import create_api
from ipalib.rpc import jsonclient

# Создание нового экземпляра API
api = create_api()

# Инициализация API
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()

# Подключение API через RPC клиент
client = jsonclient(api)
client.finalize()
client.connect()

# Пробный вызов команды user_find
try:
    email = 'ya.alexgr4@yandex.ru'
    result = api.Command['user_find'](mail=email)
    print(f"Результат поиска: {result}")
except Exception as e:
    print(f"Ошибка выполнения команды 'user_find': {e}")