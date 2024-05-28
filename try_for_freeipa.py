from ipalib import create_api, rpc
#from ipaclient.plugins.user import user_show


api = create_api(mode=None)
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
#api.add_plugin(user_show)

#api.load_plugins

api.finalize()
client = rpc.jsonclient(api)
client.finalize()
client.connect()

try:
    # Пример команды: получение информации о пользователе
    user_info = api.Command.user_show(uid='admin')
    print(f"Информация о пользователе: {user_info['result']}")

    # Ваш код для работы с API

except Exception as e:
    print(f"Ошибка при выполнении команды: {e}")

try:
    print("Loaded plugins:", api.env.loaded_plugins)
except AttributeError:
    print("нет плагинов")
try:
    available_commands = api.Command.keys()
    print("команды:", available_commands)
except AttributeError:
    print("нет команд.")
if 'user_show' in api.Command:
    result = api.Command['user_show']()
    user_show = api.Command.user_show('alex')['result']
    print(user_show)
    print(result)
else:
    print("'user_show' не доступна.")
