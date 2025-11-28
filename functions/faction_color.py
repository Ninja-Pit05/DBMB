"""
Functions related to //faction_color command.
"""


import json
from functions import utils


def get_faction(owner: str):
    with open("database/Allowed_Faction_Owners.txt") as fil:
        file = json.loads(fil.read())
        print(file)
        for faction in file:
            if owner in file[faction]:
                return faction


def edit_color(faction: str,color: str):
    faction=faction.lower()
    faction = faction.strip()
    
    with open("database/custom_faction_colors.txt") as fil:
        file = json.loads(fil.read())
        if utils.is_hex(color):
            file[faction] = color
            with open("database/custom_faction_colors.txt","w") as output:
                output.write(json.dumps(file, indent=4))
            return
        else:
            raise Exception("Invalid HEX Code")


def get_factions():
    with open("database/custom_faction_colors.txt") as file:
        file = json.loads(file.read())
        return file.keys()


def rm_faction(faction: str):
    with open("database/custom_faction_colors.txt") as fil:
        file = json.loads(fil.read())
        file.pop(faction)
    with open("database/custom_faction_colors.txt","w") as output:
        output.write(json.dumps(file, indent=4))