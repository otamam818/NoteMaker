from custom_widgets.shadow_button import ShadowButton

class SquareButton(ShadowButton):
    def __init__(self, label, tooltip, shortcut=None, parent=None,
                 click_func=None, length=30):
        super(SquareButton, self).__init__(
            label, 
            tooltip, 
            shortcut, 
            parent, 
            click_func
        )
        self.setFixedSize(length, length)

