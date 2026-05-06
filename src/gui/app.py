from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QStackedLayout, QFrame
)
from PySide6.QtCore import Qt
from net.client import server_AUTH

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MC Control")
        self.resize(400, 500)

        self.stack = QStackedLayout()

        self.login_page = self.build_login()
        self.dashboard = self.build_dashboard()

        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.dashboard)

        self.setLayout(self.stack)
        self.setStyleSheet(self.styles())

    # 🔐 LOGIN UI
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

    # 🎮 DASHBOARD UI
    def build_dashboard(self):
        container = QWidget()
        layout = QVBoxLayout()

        self.status = QLabel("● CONNECTED")
        self.status.setObjectName("status")

        self.log = QTextEdit()
        self.log.setReadOnly(True)

        start = QPushButton("START")
        stop = QPushButton("STOP")
        wol = QPushButton("WAKE")

        start.clicked.connect(lambda: self.send("START"))
        stop.clicked.connect(lambda: self.send("STOP"))
        wol.clicked.connect(lambda: self.send("WOL"))

        layout.addWidget(self.status)
        layout.addWidget(start)
        layout.addWidget(stop)
        layout.addWidget(wol)
        layout.addWidget(self.log)

        container.setLayout(layout)
        return container

    # 🔐 LOGIN LOGIC
    def do_login(self):
        pwd = self.password.text()

        if not pwd:
            self.error.setText("Enter password")
            return

        self.error.setText("Connecting...")

        result = server_AUTH(pwd)

        if result == 0:
            self.error.setText("Successful Connection")
        if result == 1:
            self.error.setText("Error with the server, try again later")
            return
        if result == 2:
            self.error.setText("Wrong password, try again in 30 seconds")
            return
        if result == 3:
            self.error.setText("Error with server, restart the program and try again")
            return

        self.stack.setCurrentWidget(self.dashboard)

    # 🎨 STYLE
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