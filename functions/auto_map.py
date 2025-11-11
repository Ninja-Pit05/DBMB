"""
Functions Related to //auto map command.
"""

import json


def set_channel(guild_id: int, channel_id: int):
    """Updates Guild's auto map channel"""
    guild_id = str(guild_id)
    with open("database/autoUpdatesChannels.txt") as fil:
        file = json.loads(fil.read())
    file[guild_id] = channel_id
    with open("database/autoUpdatesChannels.txt","w") as fil:
        fil.write(json.dumps(file,indent=4))
            
            
def get_channel(guild_id: int):
    """Gets guild's auto map channel"""
    guild_id = str(guild_id)
    with open("database/autoUpdatesChannels.txt") as fil:
        file = json.loads(fil.read())
        return file.get(guild_id)
           

def get_all_channels():
    """Returns ALL guild's auto map channel"""
    with open("database/autoUpdatesChannels.txt") as fil:
        file = json.loads(fil.read())
        return file