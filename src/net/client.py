import socket
import hashlib
import threading
from PySide6.QtCore import Qt, QTimer

SERVER_IP = "10.82.81.56"
SERVER_PORT = 31159

def server_AUTH(password):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)  # Set a timeout to avoid hanging

        s.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server")

        # Step 1: Receive the challenge
        challenge = ""
        while True:
            data = s.recv(1024).decode().strip()
            if not data:
                break
            challenge = data
            print(f"Received challenge: {challenge}")
            if challenge.startswith("CHALLENGE"):
                break

        if not challenge.startswith("CHALLENGE"):
            print("Invalid challenge received")
            return 1  # Invalid challenge

        # Step 2: Compute hash of password + challenge
        server_hash = challenge.split(" ")[1]
        server_hash = server_hash.lstrip()
        print(f"hashing {password+server_hash}")
        client_hash = hashlib.sha256((password+server_hash).encode()).hexdigest()

        # Step 3: Send the computed hash

        s.sendall(f"AUTH {client_hash}".encode())
        print(f"Sent computed hash {client_hash}")

        # Step 4: Wait for server response
        response = s.recv(1024).decode().strip()
        print(f"Authentication response: {response}")

        if response == "OK":
            print("Authentication successful")
            return 0  # Authentication successful
        elif response == "FAIL":
            print("Authentication failed")
            return 2  # Wrong password
        else:
            print(f"Unexpected server response: {response}")
            return 1  # Unexpected response

    except socket.error as e:
        print(f"Socket error: {e}")
        return 1  # Socket error
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 3  # General error