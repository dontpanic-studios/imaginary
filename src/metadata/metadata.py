import json, os

class MetaData():
    def __init__(self):
        super().__init__()

    def readMetaData(path):
        metadata = json.load(path)
        return metadata

    def reload():
        sub_folders = [name for name in os.listdir('./src/vm/') if os.path.isdir(os.path.join('./src/vm/', name))]
        return sub_folders        
    
    def createMetadata(path, core, maxmem, isoloc, diskloc):
        f = open(path + 'metadata.json', 'w')
        f.close()

        data = {}
        data['sys_core'] = core
        data['max_mem'] = maxmem
        data['iso_loc'] = isoloc
        data['disk_loc'] = diskloc