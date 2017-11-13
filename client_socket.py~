import socket
import sys

port = 12346
host = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:	#try to connect to server
	sock.connect((host,port))
except socket.error as msg:	#if we got error,close the socket and exit
	sock.close()
	print("Cannot connect to server")
	sys.exit(1)
if sock is not None:
	while True:
		data = input()
		#print('a', data.lstrip(), 'a', '\r', 'a')
		if data.lstrip() != '' :
			sock.send(data.encode())	#encode the user message so it can be send with sock.send()
			incoming = sock.recv(2048).decode()	#decode incoming message from server
			if incoming == "Connection closed":	#if server close connection,close socket on client too
				print("Exit Code Detected, Connection Closed")
				sock.close()
				break
			print(incoming)	#print server message
	sys.exit(1)
