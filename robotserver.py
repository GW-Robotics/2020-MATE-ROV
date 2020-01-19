import socket, pickle
import time
from gpiozero import Servo

host = '169.254.159.7'
port = 1234
motor0 = Servo(0,initial_value = None)
motor1 = Servo(1,initial_value = None)

def readInput(data):
	x_axis = data[0]
	return x_axis


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
print("Server Socket was created and bound!")
s.listen(1)

conn, addr=s.accept()
print("Conn: ",conn," Address: ",addr)

x_axis = -1
init = false
while True:
	data = pickle.loads(conn.recv(1024))
	d = readInput(data)
	if d is not 0
		if not init:
			motor0.value = -1
			motor1.value = -1
		else:
			motor0.value = d
			motor1.value = d
	
	send = ("Recieved: " + str(d))
	print(send)
