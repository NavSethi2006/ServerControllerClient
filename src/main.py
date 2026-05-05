import sys
from PySide6.QtWidgets import QApplication
from gui.app import App

app = QApplication(sys.argv)

window = App()
window.show()

sys.exit(app.exec())