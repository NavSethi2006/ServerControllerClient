import socket
import hashlib

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080



def server_AUTH(password):
    try :
        s = socket.socket()
        s.connect(SERVER_IP, SERVER_PORT)
        
        challange = s.recv(1024).decode().strip()

        if not challange.startswith("CHALLENGE"):
            return 1
        server_hash = challange.split(" ")[1]
        client_hash = hashlib.sha256(((password+server_hash).endcode()).hexdigest())
        
        s.sendall(f"AUTH {client_hash}\n".encode());
        result = s.recv(1024).decode().strip()

        if result != "OK":
            print("Authentication incorrect")
            return 2
    except Exception as e: 
        return 3
    
    return 0

def server_mainloop():
    return

