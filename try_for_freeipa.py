from ipalib import create_api
from ipalib.rpc import jsonclient

# Создание нового экземпляра API
api = create_api()

# Логирование инициализации API
print("Инициализация API")

try:
    # Печатаем конфигурацию API перед bootstrap
    config = api.env
    print(f"Конфигурация перед bootstrap: {config}")
    
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

# Подробное логирование доступных плагинов
try:
    plugins = list(api.loaded_plugins)
    print(f"Загруженные плагины: {plugins}")

    available_commands = list(api.Command.keys())
    print(f"Доступные команды: {available_commands}")

    # Попытка вызова команды 'user_find' если она существует
    if 'user_find' in available_commands:
        email = 'ya.alexgr4@yandex.ru'
        result = api.Command['user_find'](mail=email)
        print(f"Результат выполнения команды 'user_find': {result}")
    else:
        print("Команда 'user_find' недоступна")

except KeyError as e:
    print(f"Команда не найдена: {e}")
except Exception as e:
    print(f"Ошибка выполнения команды: {e}")