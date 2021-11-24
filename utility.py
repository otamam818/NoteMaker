import os
import re
from subprocess import check_output
from typing import List, Final

X_FACTOR: Final[float] = 5/16
Y_FACTOR: Final[float] = 5/12

def get_scres() -> List[int]:
    """ Get the screen resolution """
    # Check if the operating system is Windows-based or UNIX-based
    if os.name != 'nt':
        scres = check_output("xrandr  | grep \* | cut -d' ' -f4", shell=True)
        scres = [int(i) for i in re.findall("\d+", scres.decode('utf-8'))]
    else: 
        # NOT_IMPLEMENTED (properly, at least)
        scres = check_output("wmic desktopmonitor get screenheight, screenwidth", 
                shell=True)
        scres = re.findall("\d+", scres.decode('utf-8'))
        scres[0], scres[1] = int(scres[1]), int(scres[0])
    return [scres[0]*X_FACTOR, scres[1]*Y_FACTOR]

def set_stylesheet_if_exists(self, styleSheet):
    styleSheet_exists = bool(styleSheet)
    if styleSheet_exists:
        self.setStyleSheet(styleSheet)


