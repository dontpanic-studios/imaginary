import json, os, importlib
from traceback import format_exc

class NoPluginFound(Exception):
    pass

class InvaildPluginData(Exception):
    pass

loadedPlugins = []

def loadPlugin():
        sub_folders = [name for name in os.listdir('src/plugins/') if os.path.isdir(os.path.join('src/plugins/', name))]
        try:
            for i in sub_folders:
                if(len(sub_folders) > 0):
                    f = open(f'src\\plugins\\{i}\\metadata.json', encoding='utf-8')
                    data = json.load(f)
                    isIgnore = data['ignoreThisPlugin']
                    if(isIgnore == False):
                        print(f"IUPL: Trying to load plugin -> {data['data']['name']}")
                        print(f"IUPL: Metadata:\nIUPL: Name -> {data['data']['name']}\nIUPL: Description -> {data['data']['desc']}\nIUPL: Author -> {data['author']}\nIUPL: Sources/Main -> {data['sources']['main']}\nIUPL: Sources/Class -> {data['sources']['class']}")
                        print("IUPL: Trying to inject code..")
                        try:
                            module = importlib.import_module(f"src.plugins.{i}.{data['sources']['main']}")
                            print("IUPL: Success! Returing Module.")
                        except ImportError:
                            raise NoPluginFound
                        print("IUPL: Injecting Class from plugin")
                        cls = getattr(module, data['sources']['class']) 
                        cls.Main()
                        print("IUPL: Appending")
                        loadedPlugins.append(data['data']['name'])
                    else:
                         print(f"IUPL: Ignoring plugin {data['data']['name']}.")
                else:
                    print("IUPL: No Plugins Found.")    
        except PermissionError:
            print("IUPL: Permission Error!!")
            print(format_exc())
            raise InvaildPluginData
        
        print(f"IUPL: Injection Done, Loaded Plugin Count: {len(loadedPlugins)}")

def getData(plname: str):
        try:
            f = open(f'src\\plugins\\{plname}\\metadata.json', encoding='utf-8')
            data = json.load(f)
            return data
        except (FileNotFoundError, PermissionError):
            raise InvaildPluginData