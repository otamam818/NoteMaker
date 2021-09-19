# .##..##...####...######..######....##...##...####...##..##..######..#####..
# .###.##..##..##....##....##........###.###..##..##..##.##...##......##..##.
# .##.###..##..##....##....####......##.#.##..######..####....####....#####..
# .##..##..##..##....##....##........##...##..##..##..##.##...##......##..##.
# .##..##...####.....##....######....##...##..##..##..##..##..######..##..##.

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

        # Backend
        self.prev_text = ""

        # User-interface
        prompt_label = QLabel("Enter text: ")
        self.text_area = QTextEdit()
        self.text_area.setFontFamily("Consolas")

        main_layout = QGridLayout()
        main_layout.addWidget(prompt_label, 0, 0)
        main_layout.addWidget(self.text_area, 1, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Note Maker")

    def keyReleaseEvent(self, QKeyEvent):
        # Make sure the current text is different from the previous 
        # and non-empty
        curr_text = self.text_area.toPlainText()
        valid_change = (curr_text != self.prev_text) and (len(curr_text) > 0)
        if valid_change:
            self.change_text()

    def change_text(self):
        # set a map of replacables and their cursor index
        replacables = {
            "||[]" : ["\n[   ]"+ " "*74 + "|", 3]
        }

        # Note down the cursor position and text
        curr_widget = self.text_area
        curr_text = curr_widget.toPlainText()
        curr_cursor = curr_widget.textCursor()

        prev_cursor_pos = curr_cursor.position()

        # Find if there is anything to replace
        for i in replacables.keys():
            if i in curr_text:
                curr_text = curr_text.replace(i, replacables[i][0])
                self.text_area.setText(curr_text)
                curr_cursor.setPosition(prev_cursor_pos + 
                                        replacables[i][1])

        # Fix the cursor position
        self.text_area.setTextCursor(curr_cursor)

def init_app() -> None:
    # Create the QMainWindow class as an application 
    app = QApplication(sys.argv)
    note_maker = NoteMaker()
    note_maker.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()