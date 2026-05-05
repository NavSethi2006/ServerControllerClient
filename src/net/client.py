import socket
import hashlib
from PySide6.QtCore import QThread, Signal

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080


class ClientThread(QThread):
    auth_ok = Signal()
    auth_fail = Signal(str)
    message = Signal(str)

    def __init__(self, password):
        super().__init__()
        self.password = password
        self.sock = None
        self.running = True

    def auth(self, password):

        data = self.sock.recv(1024).decode().strip()

        if not data.startswith("CHALLENGE"):
            self.auth_fail.emit("Invalid server response")
            return

        challenge = data.split(" ")[1]
        hashed = hashlib.sha256((self.password + challenge).encode()).hexdigest()

        self.sock.sendall(f"AUTH {hashed}\n".encode())

        result = self.sock.recv(1024).decode().strip()

        if result != "OK":
            self.auth_fail.emit("Wrong password")
            return

        self.auth_ok.emit()

        while self.running:
            data = self.sock.recv(1024)
            if not data:
                break
            self.message.emit(data.decode())

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((SERVER_IP, SERVER_PORT))
        except Exception as e:
            self.auth_fail.emit(str(e))

    def send(self, cmd):
        if self.sock:
            self.sock.sendall((cmd + "\n").encode())