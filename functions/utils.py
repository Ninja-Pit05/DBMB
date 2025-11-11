"""
Utility class
"""

def is_hex(code: str):
    """checks if a piece of text is a valid hex code"""
    if len(code) != 7 or code[0] != "#":
        return False
    for charac in code[1:]:
        if charac not in "0123456789abcdef":
            return False
    return True



from PIL.Image import Image
def buffer(file: Image, file_name: str):
    """ Buffers PIL.Image.Image objects to
    discord.File objects without saving it to
    memory and yet they're ready to send.
    """
    from io import BytesIO
    from discord import File
    ##
    
    imgBytes = BytesIO()
    file.save(imgBytes, format="PNG")
    imgBytes.seek(0)
    return File(fp=imgBytes,filename=file_name)



import aiohttp
import json
async def leaderboard(raw: bool=False):
    #req
    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'}) as session:
        async with session.get(r"https://droneboi.io/api/Conquest/GetClaims") as response:
            info = json.loads(await response.text())
    #get info out
    owners={}
    for block in info:
        try:
            owners[block['ownerName']]+=1
        except:
            owners[block['ownerName']]=1
    #sort it
    owners = {owner:value for owner, value in sorted(owners.items(), key=lambda item: item[1], reverse=True)}
    #leave if want data raw
    if raw:
        return owners
    #returns a discord str surrounded by ```
    String="```\n"
    for faction in owners:
        String +=faction+" : owns "+str(owners[faction])+" station(s).\n"
    String+="```"
    return String



def _is_mentionable(string:str, leading:str, trailing: str):
    '''
    Internal function for "custom" mentionables.
    We don't repeat code and is_(mentionable) becomes 2 lines. How handy!
    '''
    string=string.strip()
    if " " in string:
        return False
    if not string.startswith(leading) or not string.endswith(trailing):
        return False
    try: int(string[len(leading):-len(trailing)])
    except: return False
    return True


def is_channel(string: str):
    return _is_mentionable(string, '<#', '>')
def is_user(string: str):
    return _is_mentionable(string, '<@', '>')
def is_role(string: str):
    return _is_mentionable(string, '<@&', '>')

def extract_id(string: str):
    """Extract ids from strings, remember to make sure those strings are from mentionables."""
    out=""
    for charac in string:
        if charac in "0123456789":
            out+=charac
    return int(out)
