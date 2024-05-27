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
    # Проверяем доступные команды
    available_commands = api.Command.keys()
    print(f"Доступные команды: {list(available_commands)}")
    
    # Попытка вызова другой команды, например, 'env'
    result = api.Command['env']()
    print(f"Результат выполнения команды 'env': {result}")

except KeyError as e:
    print(f"Команда не найдена: {e}")
except Exception as e:
    print(f"Ошибка выполнения команды: {e}")