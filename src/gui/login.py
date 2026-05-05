from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Secure Login")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(60, 60, 60, 60)

        # Title
        self.title_label = QLabel("Authentication")
        self.title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 30px;
        """)
        layout.addWidget(self.title_label)

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            padding: 15px;
            border-radius: 12px;
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        layout.addWidget(self.password_input)

        # Connect Button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("""
            padding: 15px;
            border-radius: 12px;
            background-color: #1e90ff;
            color: #ffffff;
            font-size: 16px;
            border: none;
            transition: background-color 0.3s;
        """)
        self.connect_button.setCursor(Qt.PointingHandCursor)
        self.connect_button.clicked.connect(self.on_connect_clicked)
        layout.addWidget(self.connect_button)

        self.setLayout(layout)

    def on_connect_clicked(self):
        password = self.password_input.text()
        self.password_input.clear()
        return password