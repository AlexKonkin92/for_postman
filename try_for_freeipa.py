from ipalib import create_api, rpc

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
print("Loaded plugins:", api._plugins.keys())

# Проверка доступных команд
print("Available commands:", api.Command.keys())

# Выполнение команды user_find, если она доступна
if 'user_find' in api.Command:
    result = api.Command['user_find']()
    print(result)
else:
    print("The command 'user_find' is not available in the current API context.")