import socket, pickle
import time
# import serial
# from gpiozero import Servo
# from smbus import SMBus
# bus = SMBus(1)
addr = 9
host = '127.0.0.1'
port = 1234
n_motors = 8

# motor1 = Servo(1,initial_value = None)
# motor1.min()
#motor2 = Servo(2,initial_value = -1)
#motor3 = Servo(3,initial_value = -1)
#motor4 = Servo(4,initial_value = -1)
#motor5 = Servo(5,initial_value = -1)
#motor6 = Servo(6,initial_value = -1)
#motor7 = Servo(7,initial_value = -1)
#motor8 = Servo(8,initial_value = -1)


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
print("Server Socket was created and bound!")
s.listen(5)

conn, addr=s.accept()
print("Conn: ",conn," Address: ",addr)

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

# motors = [motor1,motor2,motor3,motor4,motor5,motor6,motor7,motor8]
# motors = [motor1]

motorInputs = [
	{	
		"inputs": [ax0,ax1,ax4], 
		"mults":[-1,-1,1]
	},
	{	
		"inputs": [ax0,ax1,ax4], 
		"mults":[1,-1,1]
	},
	{	
		"inputs": [ax0,ax1], 
		"mults":[-1,1]
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
	d = list(conn.recv(8))
	d = [(x-100)/100 for x in d]
	motorSend = []
	for i in range(n_motors):
		motorSum = 0
		activeInputs = 0
		for j in range(0,len(motorInputs[i]["inputs"])):
			currentInput = d[motorInputs[i]["inputs"][j]]
			# print(currentInput, end=" ")
			if abs(currentInput) > .05:
				motorSum +=  currentInput * motorInputs[i]["mults"][j]
				activeInputs += 1
		if (activeInputs != 0):
			motorSum = motorSum / activeInputs
			# print("Motor " + str(i+1) + ": " + str(motorSum))
		motorSend.append(motorSum)
		
	final_send = []
	for value in motorSend:
		if value < 0:
			final_send.append(0)
		else:
			final_send.append(value*180)
	
	print(final_send)
	conn.sendall(bytes(1))
	#bus.write_i2c_block_data(addr, 0x00, motorSend) # switch it on
	# print()
