from ipalib import create_api

# Создание и инициализация API объекта
api = create_api(mode=None)
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()

# Подключение к серверу
api.Backend.rpcclient.connect()

# Выполнение команды
result = api.Command.user_find()
print(result)