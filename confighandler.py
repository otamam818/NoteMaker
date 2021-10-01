# ..####....####...##..##..######..######...####..
# .##..##..##..##..###.##..##........##....##.....
# .##......##..##..##.###..####......##....##.###.
# .##..##..##..##..##..##..##........##....##..##.
# ..####....####...##..##..##......######...####..

import os
import json
import re
from subprocess import check_output
from typing import List, Final

X_FACTOR:     Final[float] = 5/16
Y_FACTOR:     Final[float] = 5/12
FLDR_CONFIG:  Final[str]   = ".notemaker"
FILE_CONFIG:  Final[str]   = os.path.join(FLDR_CONFIG, "settings.json")

def main() -> dict:
    create_config_if_not_exists()
    settings: dict = json.load(open(FILE_CONFIG))
    return settings

def create_config_if_not_exists():
    if not(os.path.exists(FLDR_CONFIG)):
        os.mkdir(FLDR_CONFIG)

    if not(os.path.exists(FILE_CONFIG)):
        with open(FILE_CONFIG, 'w') as my_file:
            my_file.write("{}")
        settings = initialize_settings()
        export_settings(settings)

def initialize_settings():
    settings: dict = json.load(open(FILE_CONFIG))
    # Initialize Window resolution
    settings.update({"Window-Resolution" : get_scres()})
    # Initialize Font size
    settings.update({"Font-size" : 10})
    # Initialize Default separator character
    settings.update({"Separator" : '#'})
    # Initialize default theme
    settings.update({"Theme" : None})
    # Initialize default file location
    settings.update({"Folder-location" : ''})
    return settings

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

def update_settings(key, value):
    settings: dict = json.load(open(FILE_CONFIG))
    settings.update({key : value})
    export_settings(settings)

def export_settings(settings):
    with open(FILE_CONFIG, 'w') as my_file:
        json.dump(settings, my_file, indent=4)

if __name__ =="__main__":
    main()