import socket, pickle
import sys
from inputs import KEYS_AND_BUTTONS as codes
from inputs import get_gamepad
import os

host = "127.0.0.1"
port = 1234

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client Socket Successfully created!")
#s.connect((host, port))
done = False
# Manual controls -> Keyboard numbers
# Up -> R trigger (A:5678)
# Down -> L trigger (D:5678)
# Roll right -> R bumper(A:56 D:78)
# Roll left -> L bumper (A:78 D:56)
# Lateral movement -> L stick
# Forward -> (A:12 D:34)
# Backward -> (A:34 D:12)
# Left -> (A:13 D:24)
# Right -> (A:24 D:13)
# Tilt(U,D) and Turn(L,R) - R stick
# Up -> (A:68 D:57)
# Down -> (A:57 D:68)
# Left -> (A:1 D:234)
# Right -> (A:2 D:134)

motorInputs = []
ax0 = 0
ax1 = 0
ax3 = 0
tl = 0
tr = 0
ax4 = 0
bt4 = 0
bt5 = 0
while not done:

    for event in get_gamepad():  # User did something.
        code = event.code
        value = event.state
        if(code == "ABS_X"):
            ax0 = (value/32768)*100
        elif(code == "ABS_Y"):
            ax1 = (value/32768)*100
        elif(code == "ABS_RX"):
            ax3 = (value/32768)*100
        elif(code == "ABS_RY"):
            ax4 = (value/32768)*100
        elif(code == "BTN_TL"):
            bt4 = value
        elif(code == "BTN_TR"):
            bt5 = value
        elif(code == "ABS_Z"):
            tl = value
        elif(code == "ABS_RZ"):
            tr = value
    

        




    d = [ax0, ax1, tl,tr,ax3,ax4, bt4, bt5]

    d[0] = round(d[0])+100
    d[1] = round(d[1])+100
    d[4] = round(d[4])+100
    d[5] = round(d[5])+100


    print(d)

    #bytearr = bytearray(d)

    # data = pickle.dumps(d)
    #s.sendall(bytearr)
    #s.recv(1)


