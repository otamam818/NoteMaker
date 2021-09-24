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
