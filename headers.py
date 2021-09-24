# .######..##...##..#####....####...#####...######...####..
# ...##....###.###..##..##..##..##..##..##....##....##.....
# ...##....##.#.##..#####...##..##..#####.....##.....####..
# ...##....##...##..##......##..##..##..##....##........##.
# .######..##...##..##.......####...##..##....##.....####..

import sys
import re
from subprocess import check_output
from typing import Final
from os import replace, name

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QFileDialog, 
                               QGraphicsDropShadowEffect, QGridLayout, QLabel, 
                               QGridLayout, QTextEdit, QWidget, QPushButton,
                               QFileDialog)

# ..####....####...##..##...####...######...####...##..##..######...####..
# .##..##..##..##..###.##..##........##....##..##..###.##....##....##.....
# .##......##..##..##.###...####.....##....######..##.###....##.....####..
# .##..##..##..##..##..##......##....##....##..##..##..##....##........##.
# ..####....####...##..##...####.....##....##..##..##..##....##.....####..

X_FACTOR: Final[float] = 5/16
Y_FACTOR: Final[float] = (10/27)

INP_TO_DO: Final[str] = ";;[]"
ACTION_TO_DO: Final[str] = "\n[   ] "

INP_TITLE: Final[str] = ";;'tt"
LINE_BREAKER: Final[str] = "#"*78
DARK_THEME: Final[str] = """
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
        margin-bottom: 5px;
        padding: 5px;
    }
"""
