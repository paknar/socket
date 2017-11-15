import socket
import sys
import threading

class Receive(threading.Thread) :
    def __init__ (self,sock) :
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        print ("Starting recv function")
        self.fuc ()
        #print(threading.activeCount())
        print ("Exiting recv function")
        print ("Connection Closed")

    def fuc (self) :
        while True :
            incoming = self.sock.recv(2048).decode()	#decode incoming message from server
            if incoming == "Connection closed":	#if server close connection,close socket on client too
                self.sock.close()
                break
            print(incoming)	#print server message

class Sending(threading.Thread) :
    def __init__ (self,sock) :
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        print ("Starting send function")
        self.fuc2 ()
        #print(threading.activeCount())
        print ("Exiting send function")
    
    def fuc2 (self) :
        while True :
            data = input()
            #print('a', data.lstrip(), 'a', '\r', 'a')
            if data.lstrip() != '' :
                self.sock.send(data.encode())	#encode the user message so it can be send with sock.send()
            if data == "QUIT":	#if server close connection,close socket on client too
                print("Exit Code Detected")
                self.sock.close()
                break





