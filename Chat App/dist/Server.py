import socket
import json

PORT = 8000
address = socket.gethostname()
jsonDatas = ""
ports = []
def sendListUser():
    global jsonDatas
    global ports
    global PORT
    global address
    #data =  '{ "name":"Rey", "type":"chat", "message":"alo alo alo"}'
    data = '{ "name":"Rey", "type":"central", "listFriend":"'+jsonDatas+'"}'
    print(data)
    for port in ports:
        clientSocket = socket.socket()
        clientSocket.connect((address, int(port)))
        clientSocket.send(data.encode('utf8'))
        print("Send success")
        
serverSocket = socket.socket()
serverSocket.bind((address,PORT))
serverSocket.listen()
print('Server is running...')
while (True):
    sendListUser()
    conn,addr = serverSocket.accept()
    if (conn):
        print("Have an user connnected")
        try:
            data = conn.recv(1024).decode('utf-8')
            jsonData = json.loads(data)
            ports.append(jsonData["port"])
            rawData = jsonData["name"] + ":" + jsonData["port"]
            jsonDatas+= rawData
            jsonDatas+=";"
        except:
            continue
    