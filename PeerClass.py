from threading import Thread
from threadwithreturn import ThreadWithReturn as RetThread
import tkinter as tk
import socket
import json
import os

class Peer:
    listSocket = []
    address = socket.gethostname()
    allThreads = []
    endAllThread = False
    filename = ""
    ports = []
    centralServerPort = 8000
    listFriend = ""
    def __init__(self,name,port,text):
        self.port = port
        self.name = name
        self.text = text
    def recv_input_stream(self,connection, address):
        print("Connectiom from: " + str(address))
        while True:
            if (self.endAllThread == True):
                break
            try:
                data = connection.recv(1024).decode("utf-8")
                if (not(data)):
                    return -1
                jsonMessage = json.loads(data)
                print(jsonMessage)
                if (jsonMessage["type"] == "chat"):
                    self.text.configure(state='normal')  
                    self.text.insert(tk.END,"<"+jsonMessage["name"]+ "> : " + jsonMessage["message"] +"\n")
                    self.text.configure(state='disable')
                elif(jsonMessage["type"] == "file"):
                    self.filename = jsonMessage["filename"]
                    self.text.configure(state='normal')
                    self.text.insert(tk.END,"<"+jsonMessage["name"]+ "> : send you " + self.filename +" check your folder\n")
                    self.text.configure(state='disable')
                elif(jsonMessage["type"] == "central"):
                    self.listFriend = jsonMessage["listFriend"]
                else:
                    continue
            except:
                continue
    def handleReceiveFile(self,connection):
        while True:
            try:
                try: 
                    os.mkdir(self.name) 
                except: 
                    pass
                f = open(self.name+"/"+self.filename,'wb')
                print('Start Receiving')
                while (True):
                    print("Receiving...")
                    l = connection.recv(1024)
                    if (not(l)):
                        break
                    f.write(l)
                f.close()
                print("Done Receiving") 
                self.filename = ""
            except:
                continue
    def accept_connection(self,connection, address):
        while True:
            if (self.endAllThread == True):
                break
            input_stream = RetThread(target=self.recv_input_stream, args=(connection,address))
            receiveFileStream = RetThread(target=self.handleReceiveFile, args=(connection,))
            receiveFileStream.start()
            input_stream.start()
            self.allThreads.append(input_stream)
            self.allThreads.append(receiveFileStream)
            val2 = receiveFileStream.join()
            val1 = input_stream.join()
            if (val2 == -1):
                return
            if (val1 == -1):
                return
    def registerPort(self,address,port):
        serverSocket = socket.socket()
        serverSocket.bind((address,port))
        serverSocket.listen()
        centralSocket = socket.socket()
        centralSocket.connect((self.address,self.centralServerPort))
        data =  '{"name":"'+self.name+'", "port":"'+str(self.port)+'"}'
        centralSocket.send(data.encode('utf-8'))
        while (True):
            if (self.endAllThread == True):
                break
            conn, addr = serverSocket.accept()  # accept new connection
            acceptThread = Thread(target=self.accept_connection,args=(conn,addr))
            self.allThreads.append(acceptThread)
            acceptThread.start()
    
    def sendMessage(self,message):
        if (message.lower() == "showfriends"):
            print(self.listFriend)
            friends = self.listFriend.split(";")
            self.text.configure(state='normal') 
            self.text.insert(tk.END,"From Server send the online user list:\n")
            self.text.configure(state='disable')
            for i in range(0,len(friends) - 1):
                print(friends[i])
                friend = friends[i].split(":")
                self.text.configure(state='normal')
                self.text.insert(tk.END,"\t"+friend[0]+ " : " + friend[1] +"\n")
                self.text.configure(state='disable')
            return
        self.text.configure(state='normal')  
        self.text.insert(tk.END,"<"+self.name+ "> : " + message +"\n")
        self.text.configure(state='disable')
        data =  '{ "name":"'+self.name+'", "type":"chat", "message":"'+message+'"}'
        for client in self.listSocket:
            client.send(data.encode('utf-8'))
    def sendFile(self,filePath):
        filename = filePath.split('/')[-1];
        self.text.configure(state='normal')  
        self.text.insert(tk.END,"<You> : send an " + filename +" to your friend\n")
        self.text.configure(state='disable')
        data =  '{ "name":"'+self.name+'", "type":"file", "filename":"'+filename+'"}'
        for client in self.listSocket:
            client.send(data.encode('utf-8'))
            f = open(filePath,'rb')
            print("Start sending file")
            while (True):
                l = f.read(1024)
                if (not(l)):
                    break
                client.send(l)
                print('Sending...')
            f.close()
            print("Done Sending")
            client.shutdown(socket.SHUT_WR)
        self.listSocket = []
        for port in self.ports:
            sender = Thread(target=self.setUpSendMessage,args=(self.address,port))
            self.allThreads.append(sender)
            sender.start()
    def setUpSendMessage(self,address,port):
        clientSocket = socket.socket()
        clientSocket.connect((address, int(port)))
        self.listSocket.append(clientSocket)
        print("Connect to " + str(port))
    def startServer(self):
        binder = Thread(target=self.registerPort, args=(self.address, self.port))
        self.allThreads.append(binder)
        binder.start()
    def startClient(self,port):
        sender = Thread(target=self.setUpSendMessage,args=(self.address,port))
        self.ports.append(port)
        self.allThreads.append(sender)
        sender.start()
    def endSystem(self):
        print("End system call")
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        self.endAllThread = True