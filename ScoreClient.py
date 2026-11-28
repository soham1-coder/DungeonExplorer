import socket

def sendMessage(message):
    s = socket.socket()
    s.connect(("127.0.0.1", 5050))

    s.send(message.encode())
    reply = s.recv(4096).decode()
    
    s.close()
    return reply