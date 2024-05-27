from ipalib import create_api
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

# Проверка конфигурации окружения и домена
try:
    env = api.Command['env']()
    print(f"Конфигурация окружения: {env}")

    domain = api.Command['whoami']()
    print(f"Информация о домене: {domain}")

except KeyError as e:
    print(f"Команда не найдена: {e}")
except Exception as e:
    print(f"Ошибка выполнения команды: {e}")