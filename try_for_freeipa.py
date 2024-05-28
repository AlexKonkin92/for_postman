from ipalib import create_api, rpc
api = create_api()
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.finalize()
client = rpc.jsonclient(api)
client.finalize()
client.connect()

try:
    print("Loaded plugins:", api.env.loaded_plugins)
except AttributeError:
    print("нет плагинов")
try:
    available_commands = api.Command.keys()
    print("команды:", available_commands)
except AttributeError:
    print("нет команд.")
try:
    if 'user_find' in api.Command:
        result = api.Command['user_find']()
        print(result)
    else:
        print("'user_find' не доступна.")
except Exception as e:
    print(f"An error occurred: {e}")