import socket, pickle
import sys
import pygame
import os

host = '169.254.159.7'
port = 1234

def makeInput():
	global x_axis
	output = [0]
	output[0] = round(x_axis,2)
	return output

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("CLient Socket Successfully created!")
s.connect((host,port))

pygame.init()
screen = pygame.display.set_mode((400, 300))

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

if len(joysticks) == 0:
	print('Joystick not detected')
	exit()

joystick = joysticks[0]
joystick.init()

clock = pygame.time.Clock()

done = False

while not done:
	for event in pygame.event.get(): # User did something.
		if event.type == pygame.QUIT: # If user clicked close.
                	done = True # Flag that we are done so we exit this loop.

	x_axis = abs(joystick.get_axis(1) * 180)

	d = makeInput()
	data = pickle.dumps(d)
	s.send(data)


