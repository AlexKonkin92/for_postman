from ipalib import create_api
from ipalib import errors
from ipalib.backend import Executioner
from ipalib.plugable import Registry

# Создание API объекта
api = create_api(mode=None)

# Инициализация API
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')

# Загрузка плагинов и команд
api.finalize()

# Подключение к серверу
api.Backend.rpcclient.connect()

# Явная загрузка команд
executioner = Executioner(api)
api.Command = Registry(api, 'command', api.env.context)

# Выполнение команды
try:
    result = api.Command['user_find']()
    print(result)
except errors.PublicError as e:
    print(f"An error occurred: {e}")