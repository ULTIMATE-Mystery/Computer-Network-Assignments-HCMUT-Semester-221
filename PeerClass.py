from threading import Thread
from threadwithreturn import ThreadWithReturn as RetThread
import tkinter as tk
import socket
class Peer:
    listSocket = []
    address = socket.gethostname()
    allThreads = []
    endAllThread = False
    def __init__(self,name,port,text):
        self.port = port
        self.name = name
        self.text = text
    def recv_input_stream(self,connection, address):
        print("Connectiom from: " + str(address))
        while True:
            if (self.endAllThread == True):
                break
            data = connection.recv(1024).decode("utf-8")
            if (not(data)):
                return -1
            data = data.split(' ')
            print("<"+data[0]+ "> : " + str(' '.join(data[1:])))
            self.text.configure(state='normal')  
            self.text.insert(tk.END,"<"+data[0]+ "> : " + str(' '.join(data[1:])) +"\n")
            self.text.configure(state='disabled')
        
    def accept_connection(self,connection, address):
        while True:
            if (self.endAllThread == True):
                break
            input_stream = RetThread(target=self.recv_input_stream, args=(connection,address))
            input_stream.start()
            self.allThreads.append(input_stream)
            val = input_stream.join()
            if (val == -1):
                return

    def registerPort(self,address,port):
        serverSocket = socket.socket()
        serverSocket.bind((address,port))
        serverSocket.listen()
        while (True):
            if (self.endAllThread == True):
                break
            conn, addr = serverSocket.accept()  # accept new connection
            acceptThread = Thread(target=self.accept_connection,args=(conn,addr))
            self.allThreads.append(acceptThread)
            acceptThread.start()
    def sendMessage(self,message):
            for client in self.listSocket:
                client.send((self.name+" "+message).encode())
                self.text.configure(state='normal')  
                self.text.insert(tk.END,"<"+self.name+ "> : " + message +"\n")
                self.text.configure(state='disabled')
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
        self.allThreads.append(sender)
        sender.start()
    def endSystem(self):
        print("End system call")
        self.endAllThread = True