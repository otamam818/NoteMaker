import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, 
                               QGridLayout, QTextEdit, QWidget)

def main():
    # Initiate the app
    init_app()

class NoteMaker(QWidget):
    def __init__(self, parent= None):
        super().__init__(parent=parent)

        # User-interface
        prompt_label = QLabel("Enter text: ")
        self.text_area = QTextEdit()
        self.text_area.setFontFamily("Consolas")

        main_layout = QGridLayout()
        main_layout.addWidget(prompt_label, 0, 0)
        main_layout.addWidget(self.text_area, 1, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Note Maker")

def init_app() -> None:
    # Create the QMainWindow class as an application 
    app = QApplication(sys.argv)
    note_maker = NoteMaker()
    note_maker.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()