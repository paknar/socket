import socket
import sys
import threading
from funcrecv import Receive, Sending


port = 14000
host = 'localhost'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:	#try to connect to server
	sock.connect((host,port))
except socket.error as msg:	#if we got error,close the socket and exit
	sock.close()
	print("Cannot connect to server")
	sys.exit(1)
if sock is not None:
	recv=Receive(sock)
	send=Sending(sock)
	recv.start()
	send.start()
	print(sock)
sys.exit(1)
