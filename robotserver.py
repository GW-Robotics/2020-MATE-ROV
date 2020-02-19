import socket, pickle
import time
from gpiozero import Servo
from smbus import SMBus
bus = SMBus(1)
addr = 9
host = "::"
port = 5005
n_motors = 1

s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind((host,port))
print("Server Socket was created and bound!")

#Manual controls -> Keyboard numbers
#Up -> R trigger (A:5678)
#Down -> L trigger (D:5678)
#Roll right -> R bumper(A:56 D:78)
#Roll left -> L bumper (A:78 D:56)
#Lateral movement -> L stick
	#Forward -> (A:12 D:34)
	#Backward -> (A:34 D:12)
	#Left -> (A:13 D:24)
	#Right -> (A:24 D:13)
#Tilt(U,D) and Turn(L,R) - R stick
	#Up -> (A:68 D:57)
	#Down -> (A:57 D:68)
	#Left -> (A:1 D:234)
	#Right -> (A:2 D:134)

ax0 = 0
ax1 = 1
ax2 = 2
ax3 = 3
ax4 = 4
bt4 = 5
bt5 = 6

motorInputs = [
	{	
		"inputs": [ax0,ax1,ax4], 
		"mults":[1,1,1]
	},
	{	
		"inputs": [ax0,ax1,ax4], 
		"mults":[1,1,1]
	},
	{	
		"inputs": [ax0,ax1], 
		"mults":[1,1]
	},
	{	
		"inputs": [ax0,ax1], 
		"mults":[1,1]
	},
	{	
		"inputs": [ax2,ax3,bt4, bt5], 
		"mults":[1,1,1,1]
	},
	{	
		"inputs": [ax2,ax3,bt4, bt5], 
		"mults":[1,1,1,1]
	},
	{	
		"inputs": [ax2,ax3,bt4, bt5], 
		"mults":[1,1,1,1]
	},
	{	
		"inputs": [ax2,ax3,bt4, bt5], 
		"mults":[1,1,1,1]
	}
]

while True:
	data = s.recvfrom(1024)
	d = data[0]
	print(d)
	motorSend = []
	for i in range(n_motors):
		motorSum = 0
		activeInputs = 0
		for j in range(0,len(motorInputs[i]["inputs"])):
			currentInput = d[motorInputs[i]["inputs"][j]]
			if abs(currentInput) > .05:
				motorSum +=  currentInput * d[motorInputs[i]["mults"][j]]
				activeInputs += 1
		if (activeInputs != 0):
			motorSum = motorSum / activeInputs
			print("Motor " + str(i+1) + ": " + str(motorSum))
		motorSend.append(motorSum)
	if int(d[3]) > 180:
		toSend = 90
	else:
		toSend = int(d[3]/2)
	print(toSend)
	bus.write_i2c_block_data(addr, 0x00, [toSend]*8) # switch it on
