from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QStackedLayout, QFrame
)
from PySide6.QtCore import QTimer, Qt, QObject, Signal
from net.client import client
import threading


class StatusWorker(QObject):
    finished = Signal(bool)

    def __init__(self, client_obj):
        super().__init__()
        self.client = client_obj

    def run(self):
        try:
            result = self.client.check_online()
            self.finished.emit(result)
        except Exception:
            self.finished.emit(False)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MC Control")
        self.resize(400, 500)

        self.current_result = None
        self.client = client()

        self.stack = QStackedLayout()
        self.login_page = self.build_login()
        self.dashboard = self.build_dashboard()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.dashboard)

        self.setLayout(self.stack)
        self.setStyleSheet(self.styles())

        # status timer
        self.status_timer = QTimer(self)
        self.status_timer.setInterval(1000)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start()

        self.timer = QTimer(self)
        self.timer.setInterval(1000)

    def build_login(self):
        container = QWidget()
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout()

        title = QLabel("MC CONTROL")
        title.setObjectName("title")

        subtitle = QLabel("AUTHENTICATE TO CONTINUE")
        subtitle.setObjectName("subtitle")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("enter server password")

        self.error = QLabel("")
        self.error.setObjectName("error")

        btn = QPushButton("AUTHENTICATE")
        btn.clicked.connect(self.do_login)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.password)
        layout.addWidget(btn)
        layout.addWidget(self.error)

        card.setLayout(layout)
        outer.addWidget(card)

        container.setLayout(outer)
        return container

    def build_dashboard(self):
        container = QWidget()
        layout = QVBoxLayout()

        self.status = QLabel("")
        self.status.setObjectName("status")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        start = QPushButton("START")
        stop = QPushButton("STOP")

        start.clicked.connect(self.on_start)
        stop.clicked.connect(self.on_stop)

        layout.addWidget(self.status)
        layout.addWidget(start)
        layout.addWidget(stop)
        layout.addWidget(self.log)

        container.setLayout(layout)
        return container

    def on_start(self):
        self.log.append("Starting server...")
        try:
            self.client.send_start()
            self.log.append(f"Server attempting to start started. Check the top left of the screen to see if its on in the next 30 seconds. If not then contact Navin")
        except Exception as e:
            self.log.append(f"Error starting server: {str(e)}")

    def on_stop(self):
        self.log.append("Stopping server...")
        try:
            result = self.client.send_stop()
            if(result == "0"):
                self.log.append(f"Server stopped successfully: {result}")
            else:
                self.log.append(f"Server failed to stop probably cuz its already offline: {result}")
        except Exception as e:
            self.log.append(f"Error stopping server: {str(e)}")
    def do_login(self):
        pwd = self.password.text()

        if not pwd:
            self.error.setText("Enter password")
            return

        self.error.setText("Connecting...")
        self.current_result = None

        def thread_target():
            result = self.client.server_AUTH(pwd)
            self.current_result = result

        threading.Thread(target=thread_target, daemon=True).start()

        self.timer.timeout.connect(self.check_result)
        self.timer.start(1000)

    def check_result(self):
        if self.current_result is None:
            return

        self.timer.stop()

        if self.current_result == 0:
            self.error.setText("Successful Connection")
            self.stack.setCurrentWidget(self.dashboard)

        elif self.current_result == 1:
            self.error.setText("Error with the server, it is highly likely someone else is connected. Try again later")

        elif self.current_result == 2:
            self.error.setText("Wrong password, try again in 30 seconds")

        elif self.current_result == 3:
            self.error.setText("Error with server, it is highly likely someone else is connected. Restart the program and try again")

    def update_status(self):
        worker = StatusWorker(self.client)

        def run():
            worker.run()

        worker.finished.connect(self.on_status_result)

        threading.Thread(target=run, daemon=True).start()

    def on_status_result(self, is_online):
        if is_online:
            self.status.setText("● CONNECTED")
            self.status.setStyleSheet("color: #4caf50; font-weight: bold;")
        else:
            self.status.setText("● DISCONNECTED")
            self.status.setStyleSheet("color: red; font-weight: bold;")

    def styles(self):
        return """
        QWidget {
            background-color: #0f1117;
            color: #e6e6e6;
            font-family: Consolas;
        }

        #card {
            background-color: #1a1d25;
            padding: 20px;
            border-radius: 10px;
        }

        #title {
            font-size: 20px;
            font-weight: bold;
        }

        #subtitle {
            color: #888;
            margin-bottom: 10px;
        }

        QLineEdit {
            background-color: #1f2430;
            border: 1px solid #444;
            padding: 6px;
        }

        QPushButton {
            background-color: #2a3040;
            border: 1px solid #444;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #3a4060;
        }

        QTextEdit {
            background-color: #0a0c10;
            border: 1px solid #444;
        }

        #status {
            font-weight: bold;
            color: #4caf50;
        }

        #error {
            color: red;
        }
        """