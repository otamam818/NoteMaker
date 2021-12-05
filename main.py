# .##..##...####...######..######....##...##...####...##..##..######..#####..
# .###.##..##..##....##....##........###.###..##..##..##.##...##......##..##.
# .##.###..##..##....##....####......##.#.##..######..####....####....#####..
# .##..##..##..##....##....##........##...##..##..##..##.##...##......##..##.
# .##..##...####.....##....######....##...##..##..##..##..##..######..##..##.

from headers import *
import helpWidget
import confighandler
import utility

# TODO: Orthogonalize code

def main():
    # Get the screen resolution
    scres = utility.get_scres()
    # Initiate the app
    init_app(scres)

class NoteMaker(QWidget):
    def __init__(self, scres, parent= None):
        super().__init__(parent=parent)

        # Backend
        self.settings = confighandler.main()
        self.prev_text = EMPTY_STR
        x_res, y_res = self.settings["Window-Resolution"]
        self.lb_separator = self.settings["Separator"] # line-break separator
        self.initial_text = EMPTY_STR
        self.file_location = EMPTY_STR
        self.folder_location = self.settings["Folder-location"]

        self.header_ui = UI_header(parent=self, styleSheet=DARK_THEME)
        self.add_text_area()
        self.footer_ui = UI_footer(parent=self)

        # GUI Properties
        self.create_layout()
        self.setStyleSheet(DARK_THEME)
        self.resize(x_res, y_res)
        self.setWindowTitle("Note Maker")

    def add_text_area(self):
        self.text_area = QTextEdit()
        self.curr_font = self.text_area.font()
        self.curr_font.setFamily("Consolas")
        self.text_area.setFont(self.curr_font)

        blurRadius = 7
        x_offset = 0
        y_offset = 2
        shadow_effect = self.add_shadow(blurRadius, x_offset, y_offset)
        self.text_area.setGraphicsEffect(shadow_effect)

    def create_layout(self):
        layout_order = [
            self.header_ui, 
            self.text_area, 
            self.footer_ui
        ]
        # Create a main layout in the following order
        main_layout = QVBoxLayout()
        for widget in layout_order:
            main_layout.addWidget(widget)

        # Set up the created layout
        self.setLayout(main_layout)
        self.text_area.setFocus()

    def add_shadow(self, blurRadius=5, offX=1, offY=2):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setColor(Qt.black)
        shadow_effect.setBlurRadius(blurRadius)
        shadow_effect.setOffset(offX, offY)
        return shadow_effect

    def resizeEvent(self, event):
        size = self.size()
        size = [size.width(), size.height()]
        confighandler.update_settings("Window-Resolution", size)

    def keyReleaseEvent(self, QKeyEvent):
        # Make sure the current text is different from the previous 
        # and non-empty
        curr_text = self.text_area.toPlainText()
        valid_change = (curr_text != self.prev_text) and (len(curr_text) > 0)
        if valid_change:
            self.change_text()
        
        # A '*' character at the end signifies the file has been modified
        is_modified = self.initial_text != curr_text
        if is_modified and not(self.header_ui.title_ends_with('*')):
            self.header_ui.add_to_title('*')
        elif not(is_modified) and self.header_ui.title_ends_with('*'):
            self.header_ui.remove_title_ending_chars(1)

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
                    {
                        INP_TITLE : self.title_replace
                    }[feature_input](curr_cursor, prev_cursor_pos)

        # Fix the cursor position
        self.text_area.setTextCursor(curr_cursor)

    def basic_replace(self, curr_text, curr_cursor, prev_cursor_pos, feature):
        # set a map of basic replacables and their cursor index
        replacables = {
            INP_TO_DO : [ACTION_TO_DO, 3]
        }

        curr_text = curr_text.replace(feature, replacables[feature][0])
        self.text_area.setText(curr_text)
        self.text_area.setFont(self.curr_font)
        curr_cursor.setPosition(prev_cursor_pos + replacables[feature][1])

    def change_linebreakerchar(self, char):
        self.lb_separator = char
        confighandler.update_settings("Separator", char)

    def title_replace(self, curr_cursor, prev_cursor_pos):
        curr_text = self.text_area.toPlainText()
        full_param = re.findall(INP_TITLE + " .+;", curr_text)[0]
        reps = calc_repeats(self.text_area.font().pointSize())
        LINE_BREAKER = self.lb_separator * reps

        title = "".join(full_param.replace(INP_TITLE + " ", "").split(';')[:-1])

        hreps = reps//2 # half reps
        replace_text = LINE_BREAKER + '\n' + ' '*(hreps-len(title)//2)
        replace_text += title + ' '*(hreps-len(title)//2)
        replace_text += '\n' + LINE_BREAKER + '\n'

        curr_text = curr_text.replace(full_param, replace_text)
        self.text_area.setText(curr_text)
        self.text_area.setFont(self.curr_font)
        curr_cursor.setPosition(prev_cursor_pos-len(full_param)+len(replace_text))

    def save_text_as(self):
        location = QFileDialog.getSaveFileName(
            self, "Save file...", self.folder_location, 'Text files (*.txt)'
        )[0]
        if not(".txt" in location): location = location + '.txt'
        folder = path.join(path.split(location)[:-1][0])
        self.folder_location = folder
        confighandler.update_settings("Folder-location", folder)
        self.file_location = location
        self.save_text(location)

    def save_text(self, location: str = None):
        if location == None:
            if self.file_location == '':
                self.save_text_as()
            else:
                location = self.file_location

        try:
            with open(location, 'w') as my_file:
                text = self.text_area.toPlainText()
                my_file.write(text)
            title = path.split(location)[-1].replace(".txt", '').capitalize()
            self.title_label.setText(title)
            self.initial_text = self.text_area.toPlainText()

        except TypeError:
            pass

    def load_text(self):
        try:
            location = QFileDialog.getOpenFileName(
                self, "Load file...", self.folder_location,
                'Text files (*.txt)'
            )[0]
            with open(location, 'r') as myFile:
                text = myFile.read()
            title = path.split(location)[-1].replace(".txt", '').capitalize()
            self.file_location = location
            folder = path.join(path.split(location)[:-1][0])
            self.folder_location = folder
            confighandler.update_settings("Folder-location", folder)
            self.title_label.setText(title)
            self.text_area.setText(text)
            self.text_area.setFont(self.curr_font)
            self.initial_text = self.text_area.toPlainText()
            self.text_area.setFocus()
        except:
            pass

    def closeEvent(self, event: QCloseEvent) -> None:
        changes_made = self.text_area.toPlainText() != self.initial_text
        if changes_made:
            warning = QMessageBox()
            warning.setText("Changes were made.")
            warning.setInformativeText("Save changes?")
            warning.setStandardButtons(
                QMessageBox.Save    | 
                QMessageBox.Discard | 
                QMessageBox.Cancel
            )
            warning.setStyleSheet(DARK_THEME)
            choice = warning.exec()
            if choice == QMessageBox.Save: 
                self.save_text_as()
                event.accept()
            elif choice == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

def calc_repeats(x) -> int : 
    return int((x*x)+(-29*x)+260)

def init_app(scres) -> None:
    app = QApplication(sys.argv)
    note_maker = NoteMaker(scres)
    note_maker.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
