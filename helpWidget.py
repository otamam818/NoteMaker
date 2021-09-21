import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QFileDialog, QFrame, QGridLayout, 
                               QHBoxLayout, QLabel,QGridLayout, QTextEdit, 
                               QWidget, QPushButton, QFileDialog)

def main(): 
    init_app()

class helpW(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        self.window_width  = 400
        # Add a bunch of labels
        self.all_help_objects = dict()
        
        self.create_help_object("What to type", "Insert", "Outputs")
        self.create_help_object("To-do", ";;[]", "[   ] ", 
            "Creates a new todo bullet")
        self.create_help_object(
            "Title", 
            ";;'tt TITLE_NAME;", 
            "#"*35 + '\n' + ' '*35 + "TITLE_NAME" + '\n' + "#"*35,
            "Replaces TITLE_NAME"
        )
        self.window_height = 100 * HelpObjects.num_obj
        self.setFixedSize(self.window_width, self.window_height)

        layout = QGridLayout()

        for key in self.all_help_objects.keys():
            HelpObject = self.all_help_objects[key]
            row = HelpObjects.get_row_num()
            layout.addWidget(HelpObject.label, row, 0, 1, 2, 
                            alignment=Qt.AlignLeft)
            layout.addWidget(HelpObject.syntax, row+1, 0, 
                            alignment=Qt.AlignHCenter)
            layout.addWidget(HelpObject.output, row+1, 1,
                            alignment=Qt.AlignRight)

        self.setLayout(layout)
        with open("dark_theme.qss", 'r') as myTheme:
            self.setStyleSheet(myTheme.read())
        self.setWindowTitle("Help")
    
    def create_help_object(self, label, syntax, output, tooltip=None):
        key = f"{label}>>{syntax}"
        
        label = QLabel(label)
        label.setFrameShadow(QLabel.Raised)

        Font = QFont("Consolas", 8)

        syntax = QLabel(syntax)
        if tooltip != None:
            syntax.setToolTip(tooltip)
        syntax.setFixedWidth(self.window_width*0.3)
        syntax.setFont(Font)
        syntax.setDisabled(True)

        output = QLabel(output)
        output.setFont(Font)
        output.setToolTip("Creates a new todo bullet")
        output.setFixedWidth(self.window_width*0.7)
        output.setDisabled(True)

        self.all_help_objects[key] = HelpObjects(key, label, syntax, output)


class HelpObjects:
    row_num = 0
    num_obj = 0
    def __init__(self, id, label, syntax, output) -> None:
        self.label = label
        self.syntax = syntax
        self.output = output
        self.num_obj += 1
    
    @staticmethod
    def get_row_num():
        HelpObjects.row_num += 2
        return HelpObjects.row_num-2

def init_app() -> None:
    if __name__ == "__main__":
        app = QApplication(sys.argv)

    help_widget = helpW()
    help_widget.show()

    if __name__ == "__main__":
        sys.exit(app.exec())
    else: 
        raise SystemError("Please stop")

if __name__ == "__main__":
    main()