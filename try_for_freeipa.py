from ipalib import create_api
from ipalib import rpc

# Создание API объекта
api = create_api(mode=None)

# Инициализация API
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')

# Загрузка плагинов
api.finalize()

# Подключение к серверу
client = rpc.jsonclient(api)
client.finalize()
client.connect()

# Загрузка команд
api.Command = api.Command

# Выполнение команды
result = api.Command['user_find']()
print(result)