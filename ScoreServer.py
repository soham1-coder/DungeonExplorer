import socket
from save_system import save_high_score, load_high_scores

def message(message):# message = "SUBMIT,<name>,<class>,<steps>,<bosses defeated>,<status>"" || "GET"
    parts = message.split(",")

    if parts[0] == "SUBMIT":
        save_high_score("high_score.csv", parts[1], parts[2], int(parts[3]), int(parts[4]), parts[5])
        return "OK"
    
    elif parts[0] == "GET":
        scores = load_high_scores("high_score.csv")
        lines = []
        for i in scores:
            lines.append(i["Player Name"] + "," + i["Class"] + "," + i["Steps"] + "," + i["Bosses Defeated"] + "," + i["Status"])
        return "\n".join(lines)
    return "Error"

server = socket.socket()
server.bind(("127.0.0.1", 5050))
server.listen()
print("Server is running...")

while(True):
    conn, addr = server.accept()
    recMessage = conn.recv(1024).decode()
    reply = message(recMessage)
    conn.send(reply.encode())
    conn.close()