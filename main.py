# .##..##...####...######..######....##...##...####...##..##..######..#####..
# .###.##..##..##....##....##........###.###..##..##..##.##...##......##..##.
# .##.###..##..##....##....####......##.#.##..######..####....####....#####..
# .##..##..##..##....##....##........##...##..##..##..##.##...##......##..##.
# .##..##...####.....##....######....##...##..##..##..##..##..######..##..##.

from os import replace
from headers import *

def main():
    # Get the screen resolution
    scres = get_scres()
    # Initiate the app
    init_app(scres)

class NoteMaker(QWidget):
    def __init__(self, scres, parent= None):
        super().__init__(parent=parent)

        # Backend
        self.prev_text = ""
        x_res, y_res = scres[0]*X_FACTOR, scres[1]*Y_FACTOR

        # User-interface
        prompt_label = QLabel("Enter text: ")

        self.text_area = QTextEdit()
        self.text_area.setFontFamily("Consolas")

        self.save_button = QPushButton("&Save")
        self.save_button.clicked.connect(self.save_text)

        self.load_button = QPushButton("&Load")
        self.load_button.clicked.connect(self.load_text)

        main_layout = QGridLayout()
        main_layout.addWidget(prompt_label, 0, 0)
        main_layout.addWidget(self.text_area, 1, 0, 1, 2)
        main_layout.addWidget(self.save_button, 2, 0)
        main_layout.addWidget(self.load_button, 2, 1)

        self.setLayout(main_layout)
        self.resize(x_res, y_res)
        self.setWindowTitle("Note Maker")

    def keyReleaseEvent(self, QKeyEvent):
        # Make sure the current text is different from the previous 
        # and non-empty
        curr_text = self.text_area.toPlainText()
        valid_change = (curr_text != self.prev_text) and (len(curr_text) > 0)
        if valid_change:
            self.change_text()

    def change_text(self):
        basic_inputs = [INP_TO_DO]
        param_inputs = [INP_TITLE]
        all_feature_inputs = basic_inputs + param_inputs

        # Note down the cursor position and text
        curr_widget = self.text_area
        curr_text = curr_widget.toPlainText()
        curr_cursor = curr_widget.textCursor()

        prev_cursor_pos = curr_cursor.position()

        # Find if there is anything to replace
        for feature_input in all_feature_inputs:
            if feature_input in curr_text:
                if feature_input in basic_inputs:
                    self.basic_replace(curr_text, curr_cursor, 
                                       prev_cursor_pos, feature_input
                    )
                elif bool(re.search(feature_input + " .+;", curr_text)):
                    self.param_replace(feature_input, curr_cursor, 
                                       prev_cursor_pos)

        # Fix the cursor position
        self.text_area.setTextCursor(curr_cursor)

    def basic_replace(self, curr_text, curr_cursor, prev_cursor_pos, feature):
        # set a map of basic replacables and their cursor index
        replacables = {
            INP_TO_DO : [ACTION_TO_DO, 3]
        }

        curr_text = curr_text.replace(feature, replacables[feature][0])
        self.text_area.setFontFamily("Consolas")
        self.text_area.setText(curr_text)
        curr_cursor.setPosition(prev_cursor_pos + replacables[feature][1])

    def param_replace(self, feature, curr_cursor, prev_cursor_pos): 
        {
            INP_TITLE : self.title_replace
        }[feature](curr_cursor, prev_cursor_pos)
    
    def title_replace(self, curr_cursor, prev_cursor_pos):
        curr_text = self.text_area.toPlainText()
        full_param = re.findall(INP_TITLE + " .+;", curr_text)[0]
        
        title = "".join(full_param.replace(INP_TITLE + " ", "").split(';')[:-1])
        
        replace_text = LINE_BREAKER + '\n'
        replace_text += ' '*(40-len(title)//2) + title + ' '*(40-len(title)//2)
        replace_text += '\n' + LINE_BREAKER + '\n'
        
        # print(full_param in curr_text)
        curr_text = curr_text.replace(full_param, replace_text)
        self.text_area.setFontFamily("Consolas")
        self.text_area.setText(curr_text)
        curr_cursor.setPosition(prev_cursor_pos-len(full_param)+len(replace_text))
    
    def save_text(self):
        location = QFileDialog.getSaveFileName(self, "Save file...", '',
                                               'Text files (*.txt)')[0]
        print(location)
        if not(".txt" in location): location = location + '.txt'
        with open(location, 'w') as my_file:
            text = self.text_area.toPlainText()
            my_file.write(text)

    def load_text(self):
        location = QFileDialog.getOpenFileName(self, "Save file...", '',
                                               'Text files (*.txt)')
        with open(location[0], 'r') as myFile:
            text = myFile.read()
        self.text_area.setFontFamily("Consolas")
        self.text_area.setText(text)

def get_scres():
    """ Get the screen resolution """
    scres = check_output("xrandr  | grep \* | cut -d' ' -f4", shell=True)
    scres = [int(i) for i in re.findall("\d+", scres.decode('utf-8'))]
    return scres

def init_app(scres) -> None:
    app = QApplication(sys.argv)
    note_maker = NoteMaker(scres)
    note_maker.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()