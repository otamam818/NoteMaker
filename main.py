# .##..##...####...######..######....##...##...####...##..##..######..#####..
# .###.##..##..##....##....##........###.###..##..##..##.##...##......##..##.
# .##.###..##..##....##....####......##.#.##..######..####....####....#####..
# .##..##..##..##....##....##........##...##..##..##..##.##...##......##..##.
# .##..##...####.....##....######....##...##..##..##..##..##..######..##..##.

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

        main_layout = QGridLayout()
        main_layout.addWidget(prompt_label, 0, 0)
        main_layout.addWidget(self.text_area, 1, 0)

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
                elif feature_input in param_inputs:
                    pass

        # Fix the cursor position
        self.text_area.setTextCursor(curr_cursor)

    def basic_replace(self, curr_text, curr_cursor, prev_cursor_pos, feature):
        # set a map of basic replacables and their cursor index
        replacables = {
            INP_TO_DO : [ACTION_TO_DO, 3]
        }

        curr_text = curr_text.replace(feature, replacables[feature][0])
        self.text_area.setText(curr_text)
        curr_cursor.setPosition(prev_cursor_pos + replacables[feature][1])

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