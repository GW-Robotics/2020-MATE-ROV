import socket, pickle
import time
from gpiozero import Servo
from smbus2 import SMBus
from time import sleep
bus = SMBus(1)
addr = 9
host = "::"
port = 5005
n_motors = 8
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind((host,port))
print("Server Socket was created and bound!")

#Manual controls -> Keyboard numbers
#Up -> R trigger (A:5678)
#Down -> L trigger (D:5678)
#Lateral movement -> L stick
	#Forward -> (A:12 D:34)
	#Backward -> (A:34 D:12)
	#Left -> (A:13 D:24)
	#Right -> (A:24 D:13)
#Tilt(U,D) and Turn(L,R) - R stick
	#Up -> (A:56 D:78)
	#Down -> (A:56 D:78)
	#Left -> (A:1 D:234)
	#Right -> (A:2 D:134)

# Arm left right: D-pad L/R
# Arm up down: D-pad U/D
# Arm spin clockwise -> R bumper(A:56 D:78)
# Arm spin counterclockwise -> L bumper (A:78 D:56)
# Open: A
# Close: B

ax0 = 0
ax1 = 1
ax2 = 2
ax3 = 3
ax4 = 4
bt4 = 5
bt5 = 6

motorInputs = [
	{	
		"inputs": [ax0,ax1,ax3], 
		"mults":[1,1,1]
	},
	{	
		"inputs": [ax0,ax1,ax3], 
		"mults":[-1,1,-1]
	},
	{	
		"inputs": [ax0,ax1,ax3], 
		"mults":[1,-1,-1]
	},
	{	
		"inputs": [ax0,ax1,ax3], 
		"mults":[-1,-1,1]
	},
	{	
		"inputs": [ax2,ax4], 
		"mults":[1,1]
	},
	{	
		"inputs": [ax2,ax4], 
		"mults":[1,1]
	},
	{	
		"inputs": [ax2,ax4], 
		"mults":[1,-1]
	},
	{	
		"inputs": [ax2,ax4], 
		"mults":[1,-1]
	}
]

while True:
	data = s.recvfrom(1024)
	data = data[0]
	data = [((int(d))-100)/100 for d in data]
	
	motorSend = []
	for i in range(n_motors):
		motorSum = 0
		motorAvg = 0
		activeInputs = 0
		for j in range(0,len(motorInputs[i]["inputs"])):
			currentInput = data[motorInputs[i]["inputs"][j]]
			if abs(currentInput) > .05:
				motorSum +=  currentInput * motorInputs[i]["mults"][j]
				activeInputs += 1
		if (activeInputs != 0):
			motorAvg = motorSum / activeInputs
		motorSend.append(int(max(motorAvg*180,0)))
	
	bus.write_i2c_block_data(addr, 0x00, motorSend) # switch it on
	
	sleep(.2)
