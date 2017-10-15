import socket
import sys
import threading
#from fu import *

class myThread (threading.Thread):
	def __init__(self, threadID, name, conn):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.conn = conn
	def run(self):
		print ("Starting " + self.name)
		client_call(self.conn)
		print ("Exiting " + self.name)

def client_call (conn) :
	while True:
		data = conn.recv(1024)
		if not data:		#if no data recieved,break the loop
			break
		input = data.decode()
		print("client input : ",input)
		if input == "quit":	#if client sent "quit" stop the server
			conn.send(b'Connection closed') #send the closing notice to client
			print("exit code detected")
			break
		else:
			conn.send(input.encode())

	conn.close	#close the connection


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

thread_num = 0
thread_ID = 1
threads = []
while True :
	conn, client = sock.accept()
	thread = myThread(thread_ID, client, conn)
	thread.start()
	threads.append(thread)
	thread_num+=1
	thread_ID+=1
	if threading.activeCount() == 2:
		break
	
for t in threads:
	t.join()


print ("Exiting Server")
