from pypresence import Presence
import time

clientID = '1226317055356309504'
RPC = Presence(clientID)
RPC.connect()
curState = 'Running through VM'

print(RPC.update(details=curState, large_image='star'))

while True:
    RPC.update(details=curState, large_image='star')