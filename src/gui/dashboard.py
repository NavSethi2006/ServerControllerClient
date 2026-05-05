from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(60, 60, 60, 60)

        # Log Area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("""
            background-color: #1e1e2f;
            color: #ffffff;
            padding: 15px;
            border-radius: 12px;
            font-size: 14px;
            margin-bottom: 30px;
        """)
        layout.addWidget(self.log_area)

        # Command Input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command")
        self.command_input.setStyleSheet("""
            padding: 15px;
            border-radius: 12px;
            background-color: #2c2c2c;
            color: #ffffff;
            border: 1px solid #444;
            font-size: 16px;
            margin-bottom: 30px;
        """)
        layout.addWidget(self.command_input)

        # Send Button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            padding: 15px;
            border-radius: 12px;
            background-color: #1e90ff;
            color: #ffffff;
            font-size: 16px;
            border: none;
            transition: background-color 0.3s;
        """)
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.clicked.connect(self.on_send_clicked)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def on_send_clicked(self):
        command = self.command_input.text()
        self.command_input.clear()
        return command