import socket, pickle
import sys
from inputs import get_gamepad
import os
from time import sleep


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
btnA = 0
btnB = 0
bl = 0
br = 0
dPadUD = 0
dPadLR = 0

done = False

while not done:

    for event in get_gamepad():  # User did something.
        code = event.code
        value = event.state
        if code == "ABS_X":
            ax0 = (value / 32768) * 100
        elif code == "ABS_Y":
            ax1 = (value / 32768) * 100
        elif code == "ABS_RX":
            ax3 = (value / 32768) * 100
        elif code == "ABS_RY":
            ax4 = (value / 32768) * 100
        elif code == "ABS_Z":
            tl = value
        elif code == "ABS_RZ":
            tr = value / 255 * 100
        elif code == "BTN_SOUTH":
            btnA = value
        elif code == "BTN_EAST":
            btnB = value
        elif code == "ABS_HAT0Y":
            dPadUD = value
        elif code == "ABS_HAT0X":
            dPadLR = value
        elif code == "BTN_TL":
            bl = value
        elif code == "BTN_TR":
            br = value
        elif code == "BTN_SELECT":
            exit()

    d = [
        ax0,
        ax1,
        tr,
        ax3,
        ax4,
        btnA * 100,
        btnB * 100,
        dPadUD * -100,
        dPadLR * 100,
        bl * 100,
        br * 100
    ]

    d = [round(x) + 100 for x in d]

    bytearr = bytearray(d)
    s.sendto(bytearr, (host, port))

    sleep(0.3)
