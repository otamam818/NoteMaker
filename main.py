# .##..##...####...######..######....##...##...####...##..##..######..#####..
# .###.##..##..##....##....##........###.###..##..##..##.##...##......##..##.
# .##.###..##..##....##....####......##.#.##..######..####....####....#####..
# .##..##..##..##....##....##........##...##..##..##..##.##...##......##..##.
# .##..##...####.....##....######....##...##..##..##..##..##..######..##..##.

from headers import *
import helpWidget

# to avoid circular import ImportError
if __name__ == "__main__":
    from nmcustomizer import NMCustomizer

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
        self.def_linebreaker = LINE_BREAKER
        self.initial_text = ''

        # User-interface
        prompt_label = self.add_title_label()
        self.title_label = prompt_label

        self.add_help_button()
        self.add_edit_button()
        self.add_text_area()
        self.make_save_and_load()

        self.create_layout(prompt_label)
        self.setStyleSheet(DARK_THEME)
        self.resize(x_res, y_res)
        self.setWindowTitle("Note Maker")

    def add_help_button(self):
        self.help_button = QPushButton("?")
        self.help_button.setToolTip("Help") 
        self.help_button.setFixedSize(30, 30)
        self.help_button.clicked.connect(self.init_help)
        self.help_button.setGraphicsEffect(NoteMaker.add_shadow(self))

    def add_edit_button(self):
        self.edit_button = QPushButton("*")
        self.edit_button.setToolTip("Edit") 
        self.edit_button.setFixedSize(30, 30)
        self.edit_button.clicked.connect(self.init_customizer)
        self.edit_button.setGraphicsEffect(NoteMaker.add_shadow(self))

    def init_customizer(self):
        self.customizer = NMCustomizer(parent=None, NM=self)
        self.customizer.show()
    
    def init_help(self):
        self.customizer = helpWidget.helpW(parent=None)
        self.customizer.show()

    def add_text_area(self):
        self.text_area = QTextEdit()
        self.curr_font = self.text_area.font()
        self.curr_font.setFamily("Consolas")
        self.text_area.setFont(self.curr_font)
        self.text_area.setGraphicsEffect(self.add_shadow(self, 7, 0, 2))

    def make_save_and_load(self):
        self.save_button = QPushButton("&Save")
        self.config_button_SL(self.save_button, self.save_text)

        self.load_button = QPushButton("&Load")
        self.config_button_SL(self.load_button, self.load_text)

    @staticmethod
    def config_button_SL(button: QPushButton, connector_method):
        button.clicked.connect(connector_method)
        button.setMinimumHeight(22)
        button.setStyleSheet("max-width: 240%")
        button.setGraphicsEffect(NoteMaker.add_shadow(button))

    def create_layout(self, prompt_label):
        # Enum for header and footer
        HEADER = object()
        FOOTER = object()

        # Header and Footer widgets
        HF_WIDGETS: dict = {
            HEADER : [prompt_label, self.edit_button, self.help_button],
            FOOTER : [self.save_button, self.load_button]
        }

        # List of Header (index 0) and Footer (index 1)
        HF_list = []
        for index in HF_WIDGETS.keys():
            temp_layout = QHBoxLayout()
            for widget in HF_WIDGETS[index]:
                stretch = 0 if widget is not prompt_label else 1
                temp_layout.addWidget(widget, stretch=stretch)
            temp_group = QGroupBox()
            temp_group.setLayout(temp_layout)
            temp_group.setStyleSheet("border: none")
            HF_list.append(temp_group)
        header_group, footer_group = HF_list[0], HF_list[1]
        
        main_layout = QGridLayout()
        main_layout.addWidget(header_group)
        main_layout.addWidget(self.text_area,)
        main_layout.addWidget(footer_group)

        self.setLayout(main_layout)
        self.text_area.setFocus()

    def add_title_label(self):
        prompt_label = QLabel("Enter text: ")
        TitleFont = QFont()
        TitleFont.setPointSizeF(11)
        prompt_label.setFont(TitleFont)
        return prompt_label

    @staticmethod
    def add_shadow(widget, blurRadius=5, offX=1, offY=2):
        shadow_effect = QGraphicsDropShadowEffect(widget)
        shadow_effect.setColor(Qt.black)
        shadow_effect.setBlurRadius(blurRadius)
        shadow_effect.setOffset(offX, offY)
        return shadow_effect

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
        self.text_area.setText(curr_text)
        self.text_area.setFont(self.curr_font)
        curr_cursor.setPosition(prev_cursor_pos + replacables[feature][1])

    def param_replace(self, feature, curr_cursor, prev_cursor_pos): 
        {
            INP_TITLE : self.title_replace
        }[feature](curr_cursor, prev_cursor_pos)

    def change_linebreakerchar(self, char):
        self.def_linebreaker = char*78
    
    def title_replace(self, curr_cursor, prev_cursor_pos):
        curr_text = self.text_area.toPlainText()
        full_param = re.findall(INP_TITLE + " .+;", curr_text)[0]
        LINE_BREAKER = self.def_linebreaker
        
        title = "".join(full_param.replace(INP_TITLE + " ", "").split(';')[:-1])
        
        replace_text = LINE_BREAKER + '\n'
        replace_text += ' '*(40-len(title)//2) + title + ' '*(40-len(title)//2)
        replace_text += '\n' + LINE_BREAKER + '\n'
        
        curr_text = curr_text.replace(full_param, replace_text)
        self.text_area.setText(curr_text)
        self.text_area.setFont(self.curr_font)
        curr_cursor.setPosition(prev_cursor_pos-len(full_param)+len(replace_text))
    
    def save_text(self):
        location = QFileDialog.getSaveFileName(self, "Save file...", '',
                                               'Text files (*.txt)')[0]
        if not(".txt" in location): location = location + '.txt'
        with open(location, 'w') as my_file:
            text = self.text_area.toPlainText()
            my_file.write(text)
        title = path.split(location)[-1].replace(".txt", '').capitalize()
        self.title_label.setText(title)

    def load_text(self):
        location = QFileDialog.getOpenFileName(self, "Load file...", '',
                                               'Text files (*.txt)')
        with open(location[0], 'r') as myFile:
            text = myFile.read()
        title = path.split(location[0])[-1].replace(".txt", '').capitalize()
        self.title_label.setText(title)
        self.text_area.setText(text)
        self.text_area.setFont(self.curr_font)
        self.initial_text = text
        self.text_area.setFocus()

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
            choice = warning.exec()
            if choice == QMessageBox.Save: 
                self.save_text()
                event.accept()
            elif choice == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

def get_scres():
    """ Get the screen resolution """
    if name != 'nt':
        scres = check_output("xrandr  | grep \* | cut -d' ' -f4", shell=True)
        scres = [int(i) for i in re.findall("\d+", scres.decode('utf-8'))]
    else: 
        # NOT_IMPLEMENTED (properly, at least)
        scres = check_output("wmic desktopmonitor get screenheight, screenwidth", 
                shell=True)
        scres = re.findall("\d+", scres.decode('utf-8'))
        scres[0], scres[1] = int(scres[1]), int(scres[0])
    return scres

def init_app(scres) -> None:
    app = QApplication(sys.argv)
    note_maker = NoteMaker(scres)
    note_maker.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
