from pypresence import Presence
from main import Main
from PyQt6.QtWidgets import QApplication
import sys
from src.language.lang import LanguageList
from pypresence import DiscordNotFound
from dotenv import load_dotenv
from src.notification.wrapper import Notifiaction
load_dotenv('./data/setting.env')

print('load discord')
try:
    clientID = '1226317055356309504'
    RPC = Presence(clientID)
    RPC.connect()
    curState = 'Debugging through VM'

    print(RPC.update(details=curState, large_image='star'))
    app = QApplication(sys.argv[0:]) # yeah i shouldn't doing this for presence but, no option!
    win = Main()
    win.setupWidget()
    win.show()
    app.exec()
    print('done')
    while True:
        RPC.update(details=curState, large_image='star')
except DiscordNotFound:
    Notifiaction.showWarn(LanguageList.MSG_DISCORD_NOT_FOUND_TITLE, LanguageList.MSG_DISCORD_NOT_FOUND_DESC, 1500, True)
    app = QApplication(sys.argv[0:]) # yeah i shouldn't doing this for presence but, no option!
    win = Main()
    win.setupWidget()
    win.show()
    app.exec()