from pypresence import Presence
from main import Main
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys, time, os
from pypresence import DiscordNotFound
from dotenv import load_dotenv
load_dotenv('./data/setting.env')

app = QApplication(sys.argv[0:])
win = Main()
win.setupWidget()
win.show()
app.exec()

if(os.environ.get('DiscordSupport') == 'True'):
    print('load discord')
    try:
        clientID = '1226317055356309504'
        RPC = Presence(clientID)
        RPC.connect()
        curState = 'Running through VM(s)'

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
        msgBox = QMessageBox()
        msgBox.setWindowTitle('디스코드 확인되지 않음')
        msgBox.setText('디스코드가 설치되지 않았거나, 실행되지 않았습니다.\n다만, 이 기능을 data/setting.env 파일에서 끌수 있습니다.')
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes)
        if(msgBox == QMessageBox.StandardButton.Yes):
            exit(1)
else:
    print('DiscordSupport disabled, returning non.')