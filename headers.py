# .######..##   ##..#####....####...#####...######...####..
# ...##....### ###..##  ##..##  ##..##  ##....##....##   ..
# ...##....##.#.##..#####...##  ##..#####.....##.....####..
# ...##....##   ##..##......##  ##..##..##....##.....   ##.
# .######..##   ##..##.......####...##..##....##.....####..

import sys
import re
from subprocess import check_output
from typing import Final
from os import replace, name, path

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QCloseEvent, QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication, QFileDialog, 
    QGraphicsDropShadowEffect, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, 
    QGridLayout, QMessageBox, QTextEdit, QWidget, QPushButton,
    QFileDialog
)

from custom_widgets.ui_header import UI_header
from custom_widgets.ui_footer import UI_footer

# ..####....####...##..##...####...######...####...##..##..######...####..
# .##..##..##..##..###.##..##........##....##..##..###.##....##....##.....
# .##......##..##..##.###...####.....##....######..##.###....##.....####..
# .##..##..##..##..##..##......##....##....##..##..##..##....##........##.
# ..####....####...##..##...####.....##....##..##..##..##....##.....####..


LINE_WIDTH_FACTOR: Final[int] = 78/6000
INP_TO_DO:         Final[str] = ";;[]"
ACTION_TO_DO:      Final[str] = "\n[   ] "
EMPTY_STR:         Final[str] = ""

INP_CUST_TITLE:    Final[str] = ";;t. .+;"
INP_TITLE:         Final[str] = ";;t"
DARK_THEME:        Final[str] = """
    QWidget {
        background-color: "#111111";
        opacity: 225;
        color: "#FFFFFF";
    }

    QPushButton {
        background-color: "#212121";
        border-style: none;
        border-radius: 5px;
    }

    QPushButton::hover {
        background-color: "#242424";
        border: 1px solid "#2A2A2A";
    }

    QPushButton::pressed {
        background-color: "#191919";
    }

    QTextEdit {
        background-color: "#0A0A0A";
        border-style: none;
        border-radius: 5px;
        padding: 5px;
    }

    QScrollBar:vertical {
        border: none;
        background: "#121212";
        width: 15px;
        margin: 22px 0 22px 0;
    }
    QScrollBar::handle:vertical {
        background: "#212121";
        min-height: 20px;
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: "#191919";
        height: 20px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::sub-line:vertical {
        border: none;
        background: "#191919";
        height: 20px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        border: 2px solid "#212121";
        width: 3px;
        height: 3px;
        background: "#212121";
    }

    QLineEdit {
        background-color: "#0A0A0A";
        border-style: none;
        border-radius: 5px;
        margin-bottom: 5px;
        padding: 5px;
    }
    
    QMessageBox QPushButton{
        background-color: "#252525";
        border-style: none;
        border-radius: 5px;
        margin-bottom: 5px;
        height: 25px;
        padding: 3px;
    }
"""
