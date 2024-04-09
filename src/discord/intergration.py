from pypresence import Presence
from main import Main
from PyQt6.QtWidgets import QApplication
import sys

clientID = '1226317055356309504'
RPC = Presence(clientID)
RPC.connect()
curState = 'Running through VM'

print(RPC.update(details=curState, large_image='star'))
app = QApplication(sys.argv[0:])
win = Main()
win.setupWidget()
win.show()
app.exec()

while True:
    RPC.update(details=curState, large_image='star')