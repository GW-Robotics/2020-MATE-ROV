import socket, pickle
import sys
import pygame
import os

host = "fe80::d21a:f453:108b:8af6"
port = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client Socket Successfully created!")

pygame.init()
screen = pygame.display.set_mode((400, 300))

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

if len(joysticks) == 0:
    print("Joystick not detected")
    exit()

joystick = joysticks[0]
joystick.init()

clock = pygame.time.Clock()

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

while not done:
    for event in pygame.event.get():  # User did something.
        if event.type == pygame.QUIT:  # If user clicked close.
            done = True  # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            pass
            # print("Joystick button pressed.")
        elif event.type == pygame.JOYBUTTONUP:
            pass
            # print("Joystick button released.")

    ax0 = joystick.get_axis(0)
    ax1 = joystick.get_axis(1)
    ax2 = joystick.get_axis(2)
    ax3 = joystick.get_axis(3)
    ax4 = joystick.get_axis(4)
    bt4 = joystick.get_button(4)
    bt5 = joystick.get_button(5)

    d = [ax0, ax1, ax2, ax3, ax4, bt4, bt5, 1]

    d = [round(i * 100) + 100 for i in d]

    print(d)

    bytearr = bytearray(d)

    s.sendto(bytearr, (host, port))


