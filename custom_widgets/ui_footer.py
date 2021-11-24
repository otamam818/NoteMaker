from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from custom_widgets.shadow_button import ShadowButton

class UI_footer(QWidget):
    def __init__(self, parent = None):
        super(UI_footer, self).__init__()
        self.save_button = ShadowButton(
            label = "&Save",
            tooltip = "Save",
            shortcut = "CTRL+S",
            parent = self,
            click_func = parent.save_text_as
        )

        self.load_button = ShadowButton(
            label = "&Load",
            tooltip = "Load",
            shortcut = "CTRL+L",
            parent = self,
            click_func = parent.load_text
        )

        self.all_buttons = (self.save_button, self.load_button)
        self.modify_buttons()
        self.setup_layout()

    def setup_layout(self):
        layout = QHBoxLayout()
        for i in self.all_buttons:
            layout.addWidget(i)
        self.setLayout(layout)

    def modify_buttons(self):
        fixed_height = 22
        width_adjust = "max-width: 240%"
        for button in self.all_buttons:
            button.setMinimumHeight(fixed_height)
            button.setStyleSheet(width_adjust)

