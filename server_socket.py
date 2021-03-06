import socket
import sys
import threading
from auth import Auth
#from crypt import AESCipher

print("Server Start")
host = 'localhost'
port = 12345


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host,port)) #bind the socket
sock.listen(1) #listen for incoming connection

thread_num = 0
thread_ID = 1
threads = []

while True :
	try :
	#count=threading.activeCount()-2
		conn, client = sock.accept()
		thread = Auth(thread_ID, client, conn)
		thread.start()
		threads.append(thread)
		thread_num+=1
		thread_ID+=1
	#print(threading.activeCount() , count)
	except KeyboardInterrupt :
		break

print ("\nExiting Server")
