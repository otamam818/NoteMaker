import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIntValidator, QKeyEvent, QRegularExpressionValidator
from PySide6.QtWidgets import (QApplication, QComboBox, QFileDialog, 
                               QGraphicsDropShadowEffect, QGridLayout, QGroupBox, QHBoxLayout, QLabel, 
                               QGridLayout, QLineEdit, QTextEdit, QVBoxLayout, QWidget, QPushButton,
                               QFileDialog)
from main import NoteMaker
from headers import DARK_THEME, DEF_SPLITTER

FONT_SIZE: str = "Font Size"
TITLE_SEPARATOR: str = "Title separator"
ITEMS: list = [
    FONT_SIZE,
    TITLE_SEPARATOR
]
ENTER_BUG: int = int(Qt.Key_Enter)-1

button_config = NoteMaker.config_button_SL

def main():
    init_app()

class NMCustomizer(QWidget):
    def __init__(self, NM: NoteMaker = None, parent = None) -> None:
        super().__init__(parent=parent)
        self.splitter = DEF_SPLITTER
        self.NoteMaker_connect = NM
        self.states = QComboBox()
        self.states.addItems(ITEMS)
        self.states.currentTextChanged.connect(self.print_current_text)

        self.add_preview_text(NM)

        self.confirm_button = QPushButton("&Confirm")
        button_config(self.confirm_button, self.confirm)
        self.confirm_label = QLabel("Confirmed!")
        self.confirm_label.hide()
        self.confirm_button.setStyleSheet("min-width: 240%; min-height: 22px")

        self.create_layout()
        self.setStyleSheet(DARK_THEME)
        self.resize(600, 200)
        self.setWindowTitle("Customizer")

    def create_layout(self):
        size = 34
        # Parameter configurator
        font = self.previewText.font()
        self.param_config = QLineEdit(f"{font.pointSize()}")
        self.param_config.setValidator(QIntValidator(0, 999))
        self.param_config.returnPressed.connect(self.confirm)
        self.param_config.textChanged.connect(self.change_preview_text)
        self.param_config.setMaximumSize(size*3, size)
        self.param_config.setAlignment(Qt.AlignCenter)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.states, stretch=1)
        top_layout.addWidget(self.confirm_label, alignment=Qt.AlignRight)
        top_layout.addWidget(self.param_config)
        header_group = QGroupBox("Parameter")
        header_group.setLayout(top_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(header_group)
        main_layout.addWidget(self.previewText)
        main_layout.addWidget(self.confirm_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)
        self.param_config.setFocus()

    def change_preview_text(self, text):
        self.confirm_label.hide()
        state = self.states.currentText()
        if state == FONT_SIZE:
            font = self.previewText.font()
            font.setFamily("Consolas")
            font.setPointSize(int(text))
            self.previewText.setFont(font)
        if state == TITLE_SEPARATOR:
            breaker = text*78
            title = breaker + '\n' + ' '*36 + "TITLE\n" + breaker
            self.previewText.setText(title)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        state = self.states.currentText()
        if state == FONT_SIZE:
            if event.key() == Qt.Key_Up:
                new_number = int(self.param_config.text()) + 1
                self.param_config.setText(f"{new_number}")
            elif event.key() == Qt.Key_Down:
                new_number = int(self.param_config.text()) - 1
                self.param_config.setText(f"{new_number}")

    def add_preview_text(self, NM: NoteMaker):
        self.previewText = QTextEdit()
        self.previewText.setDisabled(True)

        if NM != None:
            self.nmFont = NM.curr_font
        else:
            self.nmFont = self.previewText.font()

        self.previewText.setText("PREVIEW text.")
        self.nmFont.setFamily("Consolas")
        self.previewText.setStyleSheet("color: #888888")
        self.previewText.setFont(self.nmFont)

    def print_current_text(self):
        self.previewText.setText(self.states.currentText())
        state = self.states.currentText()
        if state == TITLE_SEPARATOR:
            splitter = self.splitter
            self.param_config.setValidator(QRegularExpressionValidator("."))
            self.param_config.setText(splitter)
            self.param_config.setAlignment(Qt.AlignCenter)
            self.change_preview_text(splitter)
        elif state == FONT_SIZE:
            font_size = str(self.param_config.font().pointSize())
            self.param_config.setValidator(QIntValidator(0, 999))
            self.param_config.setText(font_size)
            self.param_config.setAlignment(Qt.AlignCenter)
            self.change_preview_text(font_size)

    def confirm(self): 
        func = {
            FONT_SIZE : self.change_font_size,
            TITLE_SEPARATOR : self.change_title_separator
        }
        state = self.states.currentText()
        if self.NoteMaker_connect:
            func[state]()
        self.confirm_label.show()
    
    def change_font_size(self):
        size = int(self.param_config.text())
        self.nmFont.setPointSize(size)
        self.NoteMaker_connect.text_area.setFont(self.nmFont)
    
    def change_title_separator(self):
        char = self.param_config.text()
        self.NoteMaker_connect.change_linebreakerchar(char)


def init_app() -> None:
    app = QApplication(sys.argv)
    help_widget = NMCustomizer()
    help_widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
