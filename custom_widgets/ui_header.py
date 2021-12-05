import helpWidget
import utility

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from nmcustomizer import NMCustomizer
from custom_widgets.square_button import SquareButton

class UI_header(QWidget):
    def __init__(self, parent=None, styleSheet = None):
        super(UI_header, self).__init__()
        self.setParent(parent)
        self.add_title_label() 
        self.add_buttons()
        self.set_layout()
        utility.set_stylesheet_if_exists(self, styleSheet)

    def add_title_label(self):
        self.title_label = QLabel("Enter text: ")
        TitleFont = QFont()
        TitleFont.setPointSizeF(11)
        self.title_label.setFont(TitleFont)

    def add_buttons(self):
        # Adds a button for the user to find keybindings
        self.help_button = SquareButton(
            label = '?', 
            tooltip = "Help", 
            shortcut = "CTRL+H", 
            parent = self.parentWidget(), 
            click_func = self.init_help
        )

        # Allows the user to edit NoteMaker settings
        self.edit_button = SquareButton(
            label = '*', 
            tooltip = "Edit", 
            shortcut = "CTRL+Q", 
            parent = self.parentWidget(), 
            click_func = self.init_customizer
        )

    def set_layout(self):
        layout = QHBoxLayout()
        header_widgets = [
            self.title_label, 
            self.edit_button,
            self.help_button 
        ]

        for i in header_widgets:
            layout.addWidget(i)
        self.setLayout(layout)

    def init_help(self):
        self.customizer = helpWidget.helpW(
            parent=None, 
            styleSheet=self.styleSheet()
        )
        self.customizer.show()

    def init_customizer(self):
        NM_widget = self.parentWidget()
        self.customizer = NMCustomizer(
            parent=None, 
            NM=NM_widget, 
            styleSheet=self.styleSheet()
        )
        self.customizer.show()

    def title_ends_with(self, string) -> bool:
        return self.title_label.text().endswith(string)

    def add_to_title(self, string):
        title_text = self.title_label.text()
        self.title_label.setText(f"{title_text} {string}")

    def remove_title_ending_chars(self, num_chars):
        """Removes characters ending with specified (positive) index"""
        if index <= 0 or type(index) != int: 
            raise TypeError("Use a negative string as the index")
        title_text = self.title_label.text()
        self.title_label.setText(title_text[:(num_chars*-1)])


