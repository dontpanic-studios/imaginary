from pypresence import Presence
from main import Main
from PyQt6.QtWidgets import QApplication
import sys
from tkinter import messagebox
from pypresence import DiscordNotFound
from dotenv import load_dotenv
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
    messagebox.showwarning(title='Discord를 찾을수 없음', message='디스코드를 찾을수 없어 관련된 기능이 꺼진채로 실행이 됩니다.\n관련된 기능이 비활성화 될수도 있음을 확인합니다.')
    app = QApplication(sys.argv[0:]) # yeah i shouldn't doing this for presence but, no option!
    win = Main()
    win.setupWidget()
    win.show()
    app.exec()