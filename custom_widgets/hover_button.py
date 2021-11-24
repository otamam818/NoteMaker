
import sys
from PySide6.QtWidgets import QApplication, QPushButton
sys.path.append('.')
from headers import DARK_THEME

class HoverButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Hi")
        self.setStyleSheet(DARK_THEME)
        self.setMinimumSize(30, 30)
        

if __name__ == "__main__":
    app = QApplication()
    hbuttn = HoverButton()
    hbuttn.show()
    sys.exit(app.exec())