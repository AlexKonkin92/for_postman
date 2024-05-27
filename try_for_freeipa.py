from ipalib import api
from ipalib.rpc import jsonclient

# Создание и инициализация API
api.bootstrap_with_global_options(context='cli', debug=True, verbose=True)
api.finalize()

# Подключение к RPC клиенту
client = jsonclient(api)
client.finalize()
client.connect()

# Проверка доступных команд
try:
    # Проверяем доступные команды
    available_commands = list(api.Command)
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