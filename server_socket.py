import socket
import sys
#from fu import *

host = 'localhost'
port = ''

if len(sys.argv)==1:
	print("no port specified.default is 12344")
	port = 12344
else:
	port = int(sys.argv[1])

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port)) #bind the socket
sock.listen(1) #listen for incoming connection

conn, client = sock.accept()
print ("New Connection from",client)

while True:
	data = conn.recv(1024)
	if not data:		#if no data recieved,break the loop
		break
	input = data.decode()
	print("client input : ",input)
	if input == "quit":	#if client sent "quit" stop the server
		conn.send(b'Connection closed') #send the closing notice to client
		print("exit code detected.closing server")
		break
	else:
		conn.send(input.encode())

conn.close	#close the connection
