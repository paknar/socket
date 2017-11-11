import socket
import sys
import threading

class Auth (threading.Thread) :
    onlinelist = {}
    def __init__ (self,threadID,client,conn) :
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.client = client
        self.conn = conn
    
    def run(self):
        print ("Starting to connect : " + str(self.client) + " (" + self.name + ")")
        self.clientCall ()
        #print(threading.activeCount())
        print ("Exiting : " + str(self.client) + " (" + self.name + ")")
    
    def clientCall (self) :
        auth = 0
        username = 'kkalisjndjk'
        com=' '
        while True :
            if com[0] == 'LOGIN' and auth==0:
                if len(com) != 2 :
                    self.conn.send(b"-ERR Wrong Argument")
                else :
                    print("Try to login --> Username : " + com[1])
                    if len(com[1]) > 12 :
                        print(self.name + " --> Username melebihi 12 karakter!")
                        self.conn.send(b"-ERR Username melebihi 12 karakter!")
                    elif com[1] in self.onlinelist :
                        print(self.name + " --> Username sudah tersedia di server!")
                        self.conn.send(b"-ERR Username sudah tersedia di server!")
                    else :
                        self.onlinelist[com[1]]=self.conn
                        print(self.name + " Login success")
                        auth=1
                        username=com[1]
                        self.conn.send(b"+OK Login Success")
            
            elif com[0]=='SHOW':
                if len(com) == 1 :
                    if auth != 0 :
                        user=self.onlinelist.keys()
                        data="+OK\n" + '\n'.join(user)
                        self.conn.send(data.encode() + b"\n<--END OF USERLIST-->")
                        #self.conn.send(b"\n<--END OF USERLIST-->")
                    else :
                        self.conn.send(b"-ERR You Must Logged In")
                else :
                    self.conn.send(b"-ERR Wrong Argument")
                

            elif com[0]=='PRIV' and auth!=0:
                if len(com) ==3 and com[2].lstrip()!='' :
                    try :
                        target = self.onlinelist[com[1]]
                    except KeyError :
                        #print(com[2].lstrip())
                        self.conn.send(b"-ERR User Doesn't Exist")
                    else :
                        msg="Private :\nPesan dari " + username + " : " +  com[2]
                        target.send(msg.encode())
                        self.conn.send(b"+OK Sending Success")
                else :
                    self.conn.send(b"-ERR Wrong Argument")
            
            elif com[0]== 'PUB' and auth!=0:
                if len(com)==2 and com[1].lstrip()!='' :
                    for target in self.onlinelist.values() :
                        #print(target)
                        if target!=self.conn :
                            msg="Public :\nPesan dari " + username + " : " + com[1]
                            target.send(msg.encode())
                    self.conn.send(b"+OK Broadcast Success")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0]=='quit' :
                if len(com) == 1 :
                    if auth==1:
                        if username != 'kkalisjndjk' :
                            del self.onlinelist[username]
                            print("Logging out : " + username)
                        self.conn.send(b"Connection closed")
                        break
                    else :
                        self.conn.send(b"Connection closed")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com != ' ' :
                self.conn.send(b"-ERR Wrong Command")
          
            comm=self.conn.recv(2048).decode()
            com=comm.split(' ', 2)
            if com[0] != 'LOGIN' :
                print("Command : " + com[0] + " From " + username)

        self.conn.close





