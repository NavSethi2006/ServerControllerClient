import socket
import hashlib
import threading

SERVER_IP = ""
SERVER_PORT = 31159
MCSERVERIP = ""
MCSERVERPORT = 25565


class client:
        
    def server_AUTH(self, password):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((SERVER_IP, SERVER_PORT))

            challenge = ""
            while True:
                data = self.s.recv(1024).decode().strip()
                if not data:
                    break
                challenge = data
                if challenge.startswith("CHALLENGE"):
                    break
            if not challenge.startswith("CHALLENGE"):
                return 1

            server_hash = challenge.split(" ")[1]
            server_hash = server_hash.lstrip()
            client_hash = hashlib.sha256((password+server_hash).encode()).hexdigest()

            self.s.sendall(f"AUTH {client_hash}".encode())

            response = self.s.recv(1024).decode().strip()
            if response == "OK":
                return 0
            elif response == "FAIL":
                self.close_conn()
                return 2
            else:
                return 1
        except socket.error as e:
            print(f"Socket error: {e}")
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 3
         
    def send_start(self):
        self.s.sendall("START".encode())

    def send_stop(self):
        self.s.sendall("STOP".encode())
        result = self.s.recv(1).decode().strip()
        return result

    def check_online(self) -> bool:
        try:
            with socket.create_connection((MCSERVERIP, MCSERVERPORT)):
                return True
        except (OSError, socket.timeout):
            return False
    
    def close_conn(self):
        self.s.close()


