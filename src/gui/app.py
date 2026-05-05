from PySide6.QtWidgets import QWidget, QStackedLayout, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QHBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from gui.login import LoginPage
from gui.dashboard import Dashboard
from net.client import ClientThread


class App(QWidget):
    def __init__(self):
        super().__init__()
        
        # Modern window setup
        self.setWindowTitle("MC Control")
        self.resize(1000, 700)
        self.setContentsMargins(20, 20, 20, 20)
        
        # Main layout with modern styling
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Top bar
        self.top_bar = QWidget()
        self.top_bar.setObjectName("topBar")
        self.top_bar.setStyleSheet("background-color: #1a1d25; border-bottom: 1px solid #2a3040;")
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(20, 10, 20, 10)
        self.top_bar_layout.setSpacing(0)
        
        # Title Label
        self.title_label = QLabel("Server Controller")
        self.title_label.setObjectName("title")
        self.title_label.setStyleSheet("color: #e6e6e6; font-size: 24px; font-weight: bold;")
        
        # Add title to top bar
        self.top_bar_layout.addWidget(self.title_label)
        
        # Content area
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_area.setStyleSheet("background-color: #0f1117;")
        self.content_area.setLayout(QVBoxLayout())
        self.content_area.layout().setContentsMargins(20, 20, 20, 20)
        self.content_area.layout().setSpacing(20)
        
        # Status bar
        self.status_bar = QWidget()
        self.status_bar.setObjectName("status")
        self.status_bar.setStyleSheet("color: #888; font-size: 12px;")
        self.status_bar.setLayout(QHBoxLayout())
        self.status_bar.layout().setContentsMargins(0, 0, 0, 0)
        self.status_bar.layout().setSpacing(0)
        
        # Add all to main layout
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.content_area)
        self.main_layout.addWidget(self.status_bar)
        
        # Initialize UI components
        self.login_page = LoginPage()
        self.dashboard_page = Dashboard()
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.login_page)
        self.stacked_layout.addWidget(self.dashboard_page)
        self.content_area.layout().addLayout(self.stacked_layout)
        
        # Animation setup
        self.transition_animation = QPropertyAnimation(self.content_area, b"geometry")
        self.transition_animation.setDuration(300)
        self.transition_animation.setEasingCurve(QEasingCurve.OutCubic)

    def start_auth(self, password):
        self.client = ClientThread(password)
        
        self.client.auth_ok.connect(self.auth_success)
        self.client.auth_fail.connect(self.login_show_error)
        self.client.message.connect(self.dashboard_log_msg)
        
        self.client.start()
    
    def auth_success(self):
        self.transition_animation.setStartValue(self.content_area.geometry())
        self.transition_animation.setEndValue(self.content_area.geometry())
        self.transition_animation.start()
        self.stacked_layout.setCurrentWidget(self.dashboard_page)
    
    def login_show_error(self, message):
        self.login_page.show_error(message)
    
    def dashboard_log_msg(self, message):
        self.dashboard_page.log_msg(message)
    
    def send_command(self, cmd):
        if self.client:
            self.client.send(cmd)
    
    def styles(self):
        return """
        QWidget {
            background-color: #0f1117;
            color: #e6e6e6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        #topBar {
            background-color: #1a1d25;
            border-bottom: 1px solid #2a3040;
            padding: 0 20px;
        }

        #title {
            font-size: 24px;
            font-weight: bold;
            color: #e6e6e6;
        }

        #contentArea {
            background-color: #0f1117;
        }

        #status {
            color: #888;
            font-size: 12px;
        }

        QWidget#loginPage, QWidget#dashboardPage {
            background-color: #1a1d25;
            border-radius: 12px;
            padding: 20px;
        }

        QLineEdit {
            background-color: #1f2430;
            border: 1px solid #444;
            padding: 10px 12px;
            border-radius: 6px;
            font-size: 14px;
            color: #e6e6e6;
        }

        QLineEdit:focus {
            border-color: #888;
            outline: none;
        }

        QPushButton {
            background-color: #2a3040;
            border: 1px solid #444;
            padding: 10px 16px;
            border-radius: 6px;
            font-size: 14px;
            color: #e6e6e6;
            transition: background-color 0.2s ease-in-out;
        }

        QPushButton:hover {
            background-color: #3a4060;
        }

        QTextEdit {
            background-color: #0a0c10;
            border: 1px solid #444;
            padding: 10px;
            border-radius: 6px;
            font-size: 14px;
            color: #e6e6e6;
        }

        #error {
            color: red;
        }

        #flow {
            color: #888;
            font-size: 12px;
        }

        #card {
            background-color: #1a1d25;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        #card h2 {
            color: #e6e6e6;
            margin-bottom: 10px;
        }

        #card p {
            color: #888;
        }
        """