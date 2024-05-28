from ipalib import create_api, rpc

# Создание нового экземпляра API
api = create_api()

# Инициализация API
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()

# Подключение API через RPC клиент
client = rpc.jsonclient(api)
client.finalize()
client.connect()

# Выполнение команды user_find
result = api.Command['user_find']()
print(result)