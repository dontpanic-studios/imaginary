from dotenv import load_dotenv

class Load():
    def __init__(self):
        super.__init__()

    def loadEnv(self, path):
        load_dotenv(path)    