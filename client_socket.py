import socket
import sys

port = ''
if len(sys.argv)==1:
	print("No port specified,default is 12344")
	port=12344
else:
	port = int(sys.argv[1])
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
		data = input("Input message.. ")
		sock.send(data.encode())	#encode the user message so it can be send with sock.send()
		incoming = sock.recv(1024).decode()	#decode incoming message from server
		if incoming == "Connection closed":	#if server close connection,close socket on client too
			print("exit code detected,connection closed")
			sock.close()
			break
		print("server reply : ",incoming)	#print server message
	sys.exit(1)
