from ipalib import create_api, rpc
from ipaclient.plugins.user import user_show


api = create_api()
api.bootstrap(context='cli', domain='ks.works', server='freeipa-dev.ks.works')
api.add_plugin(user_show)

#api.load_plugins

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
    if 'user_show' in api.Command:
        result = api.Command['user_show']()
        user_show = api.Command.user_show('alex')['result']
        print(user_show)
        print(result)
    else:
        print("'user_show' не доступна.")
except Exception as e:
    print(f"An error occurred: {e}")