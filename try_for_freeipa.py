from ipalib import create_api, rpc
from ipalib import errors

# Создание нового экземпляра API
api = create_api()

# Инициализация API
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()

# Подключение к серверу через RPC клиент
client = rpc.jsonclient(api)
client.finalize()
client.connect()

# Проверка загруженных плагинов
try:
    print("Loaded plugins:", api.env.loaded_plugins)
except AttributeError:
    print("Could not access loaded plugins.")

# Проверка доступных команд
try:
    available_commands = api.Command.keys()
    print("Available commands:", available_commands)
except AttributeError:
    print("Could not access available commands.")

# Выполнение команды user_find, если она доступна
try:
    if 'user_find' in api.Command:
        result = api.Command['user_find']()
        print(result)
    else:
        print("The command 'user_find' is not available in the current API context.")
except errors.PublicError as e:
    print(f"An error occurred: {e}")
except KeyError:
    print("The command 'user_find' is not available in the current API context.")