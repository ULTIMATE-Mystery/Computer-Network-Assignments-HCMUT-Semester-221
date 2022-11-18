from tkinter import * 
from tkinter.ttk import *
from PeerClass import Peer
from tkinter import filedialog
peer = None
flag = True
friendList = None
def RunServer():
    global flag
    global peer
    print("Starting Server")
    if (flag == False):
        return
    if (nameEntry.get() != "" and portEntry.get() != "" and flag):
        try:
            nameEntry.configure(state='readonly')
            portEntry.configure(state='readonly')
            peer = Peer(nameEntry.get(), int(portEntry.get()),text)
            print("Create Server")
            peer.startServer()
            print("Run Server")
            flag = False
        except Exception:
            print("Fail Server")
            return
def RunClient():
    global flag
    global peer
    print("Starting client")
    if (flag == True or peer == None):
        return
    if (friendPortEntry.get() != ""):
        try:
            peer.startClient(int(friendPortEntry.get()))
            print("Run client")
            friendPortEntry.delete(0,END)
        except Exception:
            print("Fail client")
            return
def SendMessage():
    global flag
    global peer
    print("Starting send")
    if (flag == True or peer == None):
        return
    if (chatBox.get().strip() != ""):
        try:
            peer.sendMessage(chatBox.get().strip())
            chatBox.delete(0,END)
            print("SendMessage")
        except Exception:
            print("Fail sending message")
            return
def OpenFile():
    filepath = filedialog.askopenfilename()
    fileBox.configure(state='normal')  
    fileBox.delete(0,END)
    fileBox.insert(0,filepath)
    fileBox.configure(state='readonly')
    pass
def SendFile():
    global peer
    if (peer == None):
        return
    try:
        if (fileBox.get() != ""):
            peer.sendFile(fileBox.get())
    except:
        return

def on_closing():
    global peer
    if (peer != None):
        peer.endSystem()
    master.destroy()
master = Tk()
master.title('The game')
master.geometry("500x500")
master.resizable(0, 0)


# Server
l1 = Label(master, text = "Name:",width=10)
l2 = Label(master, text = "Port:",width=10)
l1.place(x = 10, y = 10)
l2.place(x = 280, y = 10)
nameEntry = Entry(master,width=30)
portEntry = Entry(master,width=10)
nameEntry.place(x=60,y=10)
portEntry.place(x=320,y=10)
runServerButton = Button(master,text="Run",command=RunServer)
runServerButton.place(x=400,y = 10)


#chat area
l3 = Label(master, text = "Friend Port:",width=10)
l3.place(x = 10, y = 50)
friendPortEntry = Entry(master,width=30)
friendPortEntry.place(x=100,y=50)
addFriendButton = Button(master,text="Run",command=RunClient)
addFriendButton.place(x=400,y = 50)


chatArea = Frame(master,width = 100,height  = 300)
scroll=Scrollbar(chatArea)
text=Text(chatArea, font=("Georgia, 12"), yscrollcommand=scroll.set,width= 50, height=17)
chatArea.place(x=20,y = 100)
scroll.pack(side=RIGHT)
text.pack(side=LEFT)
text.configure(state='disable')

# send message
l3 = Label(master, text = "Message:",width=10)
l3.place(x = 20, y = 460)
chatBox = Entry(master,width=50)
chatBox.place(x=80,y=460)
addFriendButton = Button(master,text="Send",command=SendMessage)
addFriendButton.place(x=400,y = 460)

# send file
l4 = Label(master, text = "File:",width=10)
l4.place(x = 20, y = 420)
fileBox = Entry(master,width=35)
fileBox.place(x=80,y=420)
fileBox.configure(state='readonly')
addFileButton = Button(master,text="Browser",command=OpenFile)
addFileButton.place(x=300,y = 420)
sendFileButton = Button(master,text="Send",command=SendFile)
sendFileButton.place(x=400,y = 420)


master.protocol("WM_DELETE_WINDOW", on_closing)
mainloop()