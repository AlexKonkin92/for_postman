from ipalib import api, create_api
from ipalib.rpc import jsonclient

# Создание нового экземпляра API
api = create_api()

# Логирование инициализации API
print("Инициализация API")

try:
    # Инициализация API
    api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
    print("Bootstrap завершен")
    
    # Принудительная регистрация всех плагинов
    api.load_plugins()
    print("Плагины загружены")
    
    api.finalize()
    print("Finalize завершен")

except Exception as e:
    print(f"Ошибка инициализации API: {e}")

# Подключение API через RPC клиент
print("Подключение к RPC клиенту")

try:
    client = jsonclient(api)
    client.finalize()
    print("RPC клиент финализирован")
    
    client.connect()
    print("RPC клиент подключен")

except Exception as e:
    print(f"Ошибка подключения RPC клиента: {e}")

# Проверка доступных команд
try:
    # Проверяем доступные команды
    available_commands = api.Command.keys()
    print(f"Доступные команды: {list(available_commands)}")

    # Попытка вызова другой команды, например, 'env'
    if 'env' in available_commands:
        result = api.Command['env']()
        print(f"Результат выполнения команды 'env': {result}")
    else:
        print("Команда 'env' недоступна")

except KeyError as e:
    print(f"Команда не найдена: {e}")
except Exception as e:
    print(f"Ошибка выполнения команды: {e}")