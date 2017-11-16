import socket
import sys
import threading

class Auth (threading.Thread) :
    onlinelist = {}
    multilist = {}	
    def __init__ (self,threadID,client,conn) :
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.client = client
        self.conn = conn
    
    def run(self):
        print ("Starting to connect : " + str(self.client) + " (" + self.name + ")")
        print(self.conn)
        self.clientCall ()
        #print(threading.activeCount())
        print ("Exiting : " + str(self.client) + " (" + self.name + ")")
    
    def clientCall (self) :
        auth = 0
        username = ''
        com=' '
        multi=' '
        while True :

            comm=self.conn.recv(2048).decode()
            #comm=AESCipher.decrypt(msg)
            com=comm.split(' ')
            if com[0] == 'MULTI' or com[0] == 'PUB' :
                com=comm.split(' ', 1)
            else :
                com=comm.split(' ', 2)
            if com[0] != 'LOGIN' :
                print("Command : " + com[0] + " From " + username + " (" + str(self.client) + ")")

            if com[0] == 'LOGIN': #fungsi login
                if auth != 0 :
                    self.conn.send(b"-ERR You Already Logged In") #jika sudah login
                elif len(com) != 2 :
                    self.conn.send(b"-ERR Wrong Argument") #jika argumen login salah
                else :
                    print("Try to login --> Username : " + com[1])
                    if len(com[1]) > 12 : #cek panjang username
                        print(self.name + " --> Username melebihi 12 karakter!")
                        self.conn.send(b"-ERR Username melebihi 12 karakter!")
                    elif com[1] in self.onlinelist : #cek ketersediaan username
                        print(self.name + " --> Username sudah tersedia di server!")
                        self.conn.send(b"-ERR Username sudah tersedia di server!")
                    else :
                        self.onlinelist[com[1]]=self.conn #login
                        print(self.name + " Login success")
                        auth=1
                        username=com[1]
                        self.conn.send(b"+OK Login Success")
            
            elif com[0]=='SHOW' and auth !=0: #fungsi menampilkan user online
                if len(com) == 1 : #cek command
                        user=self.onlinelist.keys()   
                        data="+OK\n" + '\n'.join(user)
                        self.conn.send(data.encode() + b"\n<--END OF USER LIST-->")
                        #self.conn.send(b"\n<--END OF USERLIST-->")
                else :
                    self.conn.send(b"-ERR Wrong Argument")
                

            elif com[0]=='PRIV' and auth!=0: #private chat
                if len(com) ==3 and com[2].lstrip()!='' : #cek argument
                    if len(com[2]) < 256 :
                        try :
                            target = self.onlinelist[com[1]] #cek user target online
                        except KeyError :
                            #print(com[2].lstrip())
                            self.conn.send(b"-ERR User Doesn't Exist")
                        else : 
                            msg="Private :\nPesan dari " + username + " : " +  com[2]
                            target.send(msg.encode())
                            self.conn.send(b"+OK Sending Success")
                    else :
                        self.conn.send(b"-ERR Message Too Long")
                else :
                    self.conn.send(b"-ERR Wrong Argument")
            
            elif com[0]== 'PUB' and auth!=0 : #fungsi broadcast
                if len(self.onlinelist) < 2 : #cek user lain yang online
                    self.conn.send(b"-ERR No Other User Online")
                elif len(com)==2 and com[1].lstrip()!='' : #cek command
                    if len(com[1]) < 256 :
                        for target in self.onlinelist.values() :
                            #print(target)
                            if target!=self.conn :
                                msg="Public :\nPesan dari " + username + " : " + com[1]
                                
                                target.send(msg.encode())
                        self.conn.send(b"+OK Broadcast Success")
                    else :
                        self.conn.send(b"-ERR Message Too Long")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0] == 'CREATE_MULTI' and auth!=0 :
                if len(com) == 2 :
                    if multi == ' ' :
                        if com[1].lstrip not in self.multilist :
                            self.multilist.setdefault(com[1].lstrip(), [])
                            self.multilist[com[1]].append(self.conn)
                            multi = com[1]
                            #print(self.multilist.keys)
                            self.conn.send(b"+OK Multichat Created")
                        else :
                            self.conn.send(b"-ERR Multichat Already Exist")
                    else :
                        self.conn.send(b"-ERR You Already Joined Multichat")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0] == 'SHOW_MULTI'and auth!=0 :
                if len(com) == 1 :
                    if len(self.multilist) > 0 :
                        key=self.multilist.keys()   
                        data="+OK\n" + '\n'.join(key)
                        self.conn.send(data.encode() + b"\n<--END OF MULTICHAT LIST-->")
                    else :
                        self.conn.send(b"-ERR No Multichat Exist")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0] == 'JOIN_MULTI' and auth != 0 :
                if len(com) == 2 :
                    if multi == ' ' :
                        if com[1] not in self.multilist.keys() :
                            self.conn.send(b"-ERR Multichat Doesn't Exist")
                        else :
                            if len(self.multilist[com[1]]) < 3 :
                                self.multilist[com[1]].append(self.conn)
                                multi = com[1]
                                self.conn.send(b"+OK Join Success")
                            else :
                                self.conn.send(b"-ERR Multichat Full")
                    else :
                        self.conn.send(b"-ERR You Already Joined Multichat")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0] == 'MULTI' and auth!=0 :
                if len(com) == 2 :
                    if multi != ' ' :
                        if len(self.multilist[multi]) > 1 :
                            if len(com[1]) < 256 :
                                for target in self.multilist[multi] :
                                    if target!=self.conn :
                                        msg="@" + username + ' ' + com[1]
                                        target.send(msg.encode())
                                self.conn.send(b"+OK Sending Multichat Success")
                            else :
                                self.conn.send(b"Message Too Long")
                        else : 
                            self.conn.send(b"-ERR No Other User In " + multi.encode())
                    else :
                        self.conn.send(b"-ERR You're Not Joined Multichat")
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0] == 'OUT_MULTI' and auth != 0:
                if len(com) == 1 :
                    if multi != ' ' :
                        self.multilist[multi].remove(self.conn)
                        if len(self.multilist[multi]) == 0 :
                            print ("No User in " + multi + ",\nDeleting " + multi)
                            del self.multilist[multi]
                        else :
                            msg="+Server --> Leaving Multichat : " + username
                            for target in self.multilist[multi] :
                                target.send(msg.encode())
                        multi=' '
                        self.conn.send(b"+OK Leaving Multichat Success")
                    else :
                        self.conn.send(b"-ERR You're Not Joined Multichat")
                else :
                    self.conn.send(b"-ERR Wrong Argument")


            elif com[0]=='QUIT' : #fungsi disconnect
                if len(com) == 1 : #cek command
                    if auth!=0 and username != '': #cek autentifikasi
                        del self.onlinelist[username]
                        print("Logging out : " + username)
                        self.conn.send(b"Connection closed")
                        if multi != ' ' :
                            self.multilist[multi].remove(self.conn)
                            if len(self.multilist[multi]) == 0 :
                                print ("No User in " + multi + ",\nDeleting " + multi)
                                del self.multilist[multi]
                            else :
                                msg="+Server --> Leaving Multichat : " + username + "\n"
                                for target in self.multilist[multi] :
                                    target.send(msg.encode())
                            multi=' '
                        msg="+Server --> Logging Out : " + username
                        for target in self.onlinelist.values() :
                            target.send(msg.encode())
                        break
                    else :
                        self.conn.send(b"Connection closed")
                        break
                else :
                    self.conn.send(b"-ERR Wrong Argument")

            elif com[0]=='LOGOUT' and auth !=0 : #fungsi logout
                if len(com) == 1 :
                    del self.onlinelist[username]
                    auth = 0
                    self.conn.send(b"+OK Logging Out")
                    print("Logging out : " + username)
                    msg="+Server --> Logging Out : " + username
                    for target in self.onlinelist.values() :
                        target.send(msg.encode())
                else :
                    self.conn.send(b"-ERR Wrong Argument")


            else : #fungsi jika command salah
                if auth == 0 :
                    self.conn.send(b"-ERR You're not Logged In")
                else :
                    self.conn.send(b"-ERR Wrong Command")
          

        self.conn.close




    
