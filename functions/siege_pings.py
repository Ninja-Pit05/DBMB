"""
Functions related to `//siege ping`.
Gets, deletes and adds siege ping ids and faction names between some other things related to `//siege ping`
"""


import json


# -----> Channel
# This is the entrance of any guild to the db
def set_channel(guild_id: int,channel_id: int):
    """ Set's the channel to receive siege pings"""
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        file[guild_id] = {"channel":channel_id,"factions":[],"ids":[]}
    else:
        file[guild_id]["channel"]=channel_id
    with open(file_path,"w") as fil:
        fil.write(json.dumps(file,indent=4))

def get_channel(guild_id: int):
    """ Returns channel configured to receive siege pings """
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        return None
    else:
        return file[guild_id]["channel"]


# -----> Faction Names
def add_faction(guild_id: int, faction: str):
    """ Adds a faction name to the db """
    guild_id=str(guild_id)
    faction=faction.lower()
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        raise Exception("Guild inexistent")
    if faction in file[guild_id]["factions"]:
        raise Exception("Faction already added")
    else:
        file[guild_id]["factions"]+=[faction]
        with open(file_path,"w") as fil:
            fil.write(json.dumps(file,indent=4))


def del_faction(guild_id: int, faction: str):
    """ Dels a faction name from the db """
    guild_id=str(guild_id)
    faction=faction.lower()
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        raise Exception("Guild inexistent")
    if faction not in file[guild_id]["factions"]:
        raise Exception("Faction inexistent")
    else:
        file[guild_id]["factions"].remove(faction)
        with open(file_path,"w") as fil:
            fil.write(json.dumps(file,indent=4))

#get faction names for siege pings
def get_factions(guild_id: int):
    """ Returns list of factions configured to trigger siege pings """
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        return None
    else:
        return file[guild_id]["factions"]



# -----> IDS
def add_id(guild_id: int, id: str):
    """ Adds a id to the db """
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        raise Exception("Guild inexistent")
    if id in file[guild_id]["ids"]:
        raise Exception("ID already added")
    else:
        file[guild_id]["ids"]+=[id]
        with open(file_path,"w") as fil:
            fil.write(json.dumps(file,indent=4))


def del_id(guild_id: int, id: str):
    """ Dels a id from the db """
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        raise Exception("Guild inexistent")
    if id not in file[guild_id]["ids"]:
        raise Exception("ID inexistent")
    else:
        file[guild_id]["ids"].remove(id)
        with open(file_path,"w") as fil:
            fil.write(json.dumps(file,indent=4))


def get_ids(guild_id: int):
    """ Returns list of ids configured to ping"""
    guild_id=str(guild_id)
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    if file.get(guild_id) is None:
        return None
    else:
        return file[guild_id]["ids"]


# -----> Triggers.
def check_triggers(trigger: str):
    """ Returns dictionary of guilds triggered.
    The dict format is like:
    --> Dict{channel_id:[ids to ping]}
    Altho we check for which guilds were triggered
    we directly return their configured channel as
    dict keys so their use is straight forward.
    """
    trigger=trigger.lower()
    file_path="database/siegePingList.txt"
    with open(file_path) as fil:
        file = json.loads(fil.read())
    
    output={}
    for guild in file:
        if trigger in guild['factions']:
            output[int(guild['channel'])] = [id for id in guild['ids']]
    return output