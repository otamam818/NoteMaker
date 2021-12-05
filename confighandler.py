# ..####....####...##..##..######..######...####..
# .##..##..##..##..###.##..##........##....##.....
# .##......##..##..##.###..####......##....##.###.
# .##..##..##..##..##..##..##........##....##..##.
# ..####....####...##..##..##......######...####..

import os
import json
from typing import List, Final
from utility import get_scres

FLDR_CONFIG:  Final[str]   = ".notemaker"
FILE_CONFIG:  Final[str]   = os.path.join(FLDR_CONFIG, "settings.json")

OG_SETTINGS:  Final[dict]  = {
    "Window-Resolution" : get_scres(),
    "Font-size" : 10,
    "Separator": "―",
    "Theme" : None,
    "Folder-location" : ""
}

def main() -> dict:
    """Creates a dictionary from ./.notemaker/settings.json"""
    create_config_if_not_exists()
    settings: dict = json.load(open(FILE_CONFIG))
    return settings

def create_config_if_not_exists():
    if not(os.path.exists(FLDR_CONFIG)):
        os.mkdir(FLDR_CONFIG)

    if not(os.path.exists(FILE_CONFIG)):
        with open(FILE_CONFIG, 'w') as my_file:
            my_file.write("{}")
        settings = OG_SETTINGS
        export_settings(settings)

def update_settings(key, value):
    settings: dict = json.load(open(FILE_CONFIG))
    settings.update({key : value})
    export_settings(settings)

def export_settings(settings):
    with open(FILE_CONFIG, 'w') as my_file:
        json.dump(settings, my_file, indent=4)

if __name__ =="__main__":
    main()

