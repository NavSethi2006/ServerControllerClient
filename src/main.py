import sys
from PySide6.QtWidgets import QApplication
from gui.app import App

app = QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec())