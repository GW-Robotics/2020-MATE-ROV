import socket, pickle
import sys
from inputs import KEYS_AND_BUTTONS as codes
from inputs import get_gamepad
import os

host = "fe80::d21a:f453:108b:8af6"
port = 5005
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
print("Client Socket Successfully created!")

ax0 = 0
ax1 = 0
ax3 = 0
tl = 0
tr = 0
ax4 = 0
bt4 = 0
bt5 = 0

done = False

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

    bytearr = bytearray(d)
    s.sendto(bytearr, (host, port))


