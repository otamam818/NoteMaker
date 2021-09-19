# .######..##...##..#####....####...#####...######...####..
# ...##....###.###..##..##..##..##..##..##....##....##.....
# ...##....##.#.##..#####...##..##..#####.....##.....####..
# ...##....##...##..##......##..##..##..##....##........##.
# .######..##...##..##.......####...##..##....##.....####..

import sys
import re
from subprocess import check_output
from typing import Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, 
                               QGridLayout, QTextEdit, QWidget)

# ..####....####...##..##...####...######...####...##..##..######...####..
# .##..##..##..##..###.##..##........##....##..##..###.##....##....##.....
# .##......##..##..##.###...####.....##....######..##.###....##.....####..
# .##..##..##..##..##..##......##....##....##..##..##..##....##........##.
# ..####....####...##..##...####.....##....##..##..##..##....##.....####..

X_FACTOR: Final[float] = 5/16
Y_FACTOR: Final[float] = (10/27)

INP_TO_DO: Final[str] = ";;[]"
ACTION_TO_DO: Final[str] = "\n[   ] "

INP_TITLE: Final[str] = ";;title: ;"
LINE_BREAKER: Final[str] = "#"*78
