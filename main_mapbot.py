# Version 2.1


# ---------- Initializing ----------
# Python imports
from PIL import Image
from discord.ext import commands
import discord
import signal
import os
import random
from time import strftime, localtime
import asyncio
import traceback
import numpy as np
import re
import json
from datetime import datetime
# Our imports
import functions
from functions import utils
from functions import Report
from assets import strings
from assets import static
from assets import change_logs



# Discord Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['//','>'], intents=intents, help_command=None)
BOT_OWNER_IDS = [
    982591657130213406,
    1195827600925405245,
]
CHANGE_COLOR = [
    796536076751339560,
    982591657130213406,
    1195827600925405245,
]

# DataBase initialization
def _db_init(path: str):
    with open(path,'a') as file:
        if file.tell() != 0:
            return
    with open(path,'w') as fille:
        fille.write(json.dumps({},indent=4))

for file in [
    "database/autoUpdatesChannels.txt",
    "database/Allowed_Faction_Owners.txt",
    "database/custom_faction_colors.txt",
    "database/siegePingList.txt",
    ]:
        _db_init(file)



# Functions to get requests key-info
def get_info(ctx):
    info = " (server:{}/channel:{}/user:{}/cmd:{}/time:'{}')".format(ctx.guild.name, ctx.channel.name, ctx.message.author.name, ctx.command, strftime("%H:%M:%S", localtime()))
    return info






# ---------- Bot client ----------

# executes on connection
@bot.event
async def on_ready():
    print(f'\033[90mSuccessfully logged in as \033[94m{bot.user}!\033[0m')
    await bot.tree.sync()
    print("\033[1;96mInitialized commands phase\033[0m")
    # on wake up, map update
    await functions.map.gen_claimsMap() if False else 0
    print("-->Auto map update. '{}'".format(strftime("%H:%M:%S", localtime())))



# triggers on every message
@bot.event
async def on_message(message):
    # checks for commands and execute them.
    await bot.process_commands(message)
    
    
    # automatically updates faction claims map. 
    # Channel hard coded cause yes.
    if message.content in ['A siege was completed', 'A siege was defended'] and message.channel.id == (1326217953326141521):
        await message.channel.send('Updating map...')
        print("--> Conquest Log got an update")
        await functions.map.gen_claimsMap()
        print("<-- Map updated {} (auto)".format(strftime("%H:%M:%S", localtime())))
        await message.channel.send('Map updated.')
    
    
    # from //auto_map sends auto map updates
    # Channel hard coded cause yes
    if message.content in ['A siege was completed'] and message.channel.id == (1326217953326141521):
         # Get servers and channels to update
        channels_to_update = functions.auto_map.get_all_channels()
        tries=3
        while tries > 0:
            for channel_id in channels_to_update:
                try:
                    # checks for channel existence.
                    channel = bot.get_channel(channel_id)
                except Exception as e:
                    print("\033[31mERROR\033[0m while trying to get channel {}\n - {}".fornat(channel_id,e))
                    continue
                try:
                    # fetches siege data.
                    target_message= await message.channel.fetch_message(message.id)
                    embed = target_message.embeds
                    await channel.send("**{}** successfully sieged **{}** taking the station from **{}**".format(
                        embed[0].fields[3].value, embed[0].fields[1].value, embed[0].fields[2].value),
                        file=discord.File('output/claimsMap.png'))
                    channels_to_update.remove(channel_id)
                except Exception as e:
                    print("\033[31mERROR\033[0m while trying to send auto map updates! {} - {}".format(channel_id,e))
            # Keeps trying but quits after 3 tries.
            if len(channels_to_update) == 0:
                print("<-- Auto map updates were delivered successfully")
                break
            else:
                tries -= 1
                print('--> Trying again to send updates of auto map...')
            if tries == 0:
                print("\033[31m<-- It wasn't possible to send all auto map updates. {} were left... \033[0m ".format(len(channels_to_update)))
                break
        del [channels_to_update, tries]


    # from //siege_ping sends pings.
    # Channel hard coded cause yes
    if message.content.startswith("A new siege will start in 10 minutes") and message.channel.id == (
            1326217953326141521):
        target_message = await message.channel.fetch_message(message.id)
        embed = target_message.embeds
        #Emoji for different latencies
        sentTime = embed[0].timestamp
        receivedTime = target_message.created_at
        latencyTime = receivedTime - sentTime
        diffSec = int(latencyTime.total_seconds())
        if diffSec < 60:
            Emo = "⭐"
        elif diffSec < 150:
            Emo = "🔥"
        elif diffSec < 300:
            Emo = "😀"
        elif diffSec < 420:
            Emo = "👍"
        elif diffSec < 780:
            Emo = "😐"
        elif diffSec < 960:
            Emo = "👎"
        elif diffSec < 1200:
            Emo = "😮‍💨"
        elif diffSec < 2400:
            Emo = "😭"
        else:
            Emo = "💀"
        # Emoji for different latencies
        triggered_dict = functions.siege_pings.check_triggers(embed[0].fields[2].value.lower())
        for key in triggered_dict.keys():
            try:
                pchannel = bot.get_channel(int(key))
                pingsLine = ""
                for id in triggered_dict[key]:
                    pingsLine += "{}".format(id)
                    if triggered_dict[key].index(id) != len(triggered_dict) - 1: pingsLine += ", "
                await pchannel.send("**{}** will get attacked in 10 minutes by **{}** at **{}**!!\n{}\n-# Latency: {} {}".format(
                            embed[0].fields[2].value,
                            embed[0].fields[3].value,
                            embed[0].fields[1].value,
                            pingsLine,
                            latencyTime,
                            Emo))
            except Exception as e:
                print("\033[91mError on siege pings '{}' on id {}\033[0m".format(e, key))
        print("<-- Siege pings sent")




@bot.before_invoke
async def report_it(ctx):
    info=get_info(ctx)
    Report.write('[info] {}'.format(info))
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,discord.ext.commands.errors.CommandNotFound):
        await ctx.send(error)
        return
    info=get_info(ctx)
    err = ''.join(traceback.format_exception(error))
    Report.write('[ERROR] {} {}'.format(info,err))
    raise error







# ---------- Bot Commands ----------

# ping-pong command
@bot.hybrid_command("ping")
async def ping_pong(ctx):
    await ctx.send("Pong! :v")
    print("-->Ping received!" + get_info(ctx))



# map command
@bot.hybrid_command('map')
async def map_cmd(ctx, args=None):
    await ctx.typing()
    if args is not None and 'update' in args:
        await functions.map.gen_claimsMap()
        await ctx.send('Map was updated successfuly!')
        print("<-- Map was updated {} (manual)".format(strftime("%H:%M:%S", localtime())))
    else:
        await ctx.send('Actual Droneboi Map:',file=discord.File('output/claimsMap.png'))



#map and leaderboard fusion.
@bot.hybrid_command('maplb')
async def maplb(ctx):
    await map_cmd(ctx)
    await leaderboard(ctx)



# help command
@bot.hybrid_command('help')
async def help(ctx):
    await ctx.send(strings.help)



# new command
@bot.hybrid_command('new')
async def new(ctx):
    await ctx.send(strings.new)



# >>> Faction color command tree.
@bot.hybrid_group('faction',invoke_without_command=True)
async def faction(ctx):
    await ctx.send(strings.faction_color_help)

@faction.group('color',invoke_without_command=True)
async def faction_color(ctx):
    await ctx.send(strings.faction_color_help)

@faction_color.command('get')
async def faction_color_get(ctx):
    #returns list of configured factions.
    with open("database/custom_faction_colors.txt") as fil:
        file=json.loads(fil.read())
        if not file:
            await ctx.send("Smh I'm empty. No faction, no colors, no nothing.")
            return
        String = "```\n"
        for faction in file:
            String += faction + "\n" + file[faction] + "\n"
        String += "```"
    await ctx.send(String)
    del String

@faction_color.command('set')
async def faction_color_set(ctx, color=None):
    if color is None:
        await ctx.send('### Missing "Color" Argument.\n - You must send a valid HEX color code.\n - Example: `#ffaaff` `#ab6381` `#00aa00`')
        return
    if not utils.is_hex(color):
        await ctx.send("### Invalid HEX code.\n - HEX code format should be `#rrggbb`\n - Example: `//faction color set #310bff`")
        return
    #checks if is on the whitelist
    if functions.faction_color.get_faction(ctx.message.author.name) is None:
        await ctx.send("You're not allowed to change the colors for any faction. To be added to the whitelist, ask your faction leader to contact Ninja")
    else:
        #try to change color.
        try:
            functions.faction_color.edit_color(functions.faction_color.get_faction(ctx.message.author.name),color)
            await ctx.send(f"Faction ***{faction_color.get_faction(ctx.message.author)}*** color changed to `{color}`")
        except Exception as e:
            await ctx.send(f"ERROR: {e}")
            print("\033[31m ERROR! Exception at 'faction color set' : {}".format(e), "\033[0m" )
            raise



# just print my name.
@bot.command('owner')
async def owner(ctx):
    await ctx.send("Made by Ninja.")



# feedback command
@bot.hybrid_command('feedback')
async def feedback(ctx, *,message=None):
    if message==None:
        await ctx.send(
            "## Feedback Commad.\nFound an issue, got an ideia, or want to make a suggestion? Give us feedback through this command. Use '`//feedback (your message)`' and it will be sent directly to our development server.")
    else:
        await ctx.send("Thanks for your feedback.")
        #feedback channel hard-coded cause yes
        feedbackChannel = bot.get_channel(1380939646560895056)
        await feedbackChannel.send(message+"\n-# "+get_info(ctx))



# leaderboard command
@bot.hybrid_command('leaderboard',aliases=['lb','leaders'])
async def leaderboard(ctx):
    await ctx.typing()
    await ctx.send("Here is the leaderboard:"+ await utils.leaderboard())



# crystals command
@bot.hybrid_command('crystal',aliases=['crystals','crystall','cry'])
async def crystals(ctx):
    await ctx.typing()
    file = utils.buffer(functions.map.crystals_map(),"CrystalsLocationMap.png")
    await ctx.send('Here is where you can find and buy rift crystals:',file=file)



#Joke command DUCK!!
@bot.command('duck')
async def duck(ctx):
    fileNumber = random.randint(1, 3)
    if fileNumber == 2:
        await ctx.send(file=discord.File('duck/duck' + str(fileNumber) + '.gif'))
    else:
        await ctx.send(file=discord.File('duck/duck' + str(fileNumber) + '.png'))



#>>>> Market Command Tree
@bot.hybrid_group('market',invoke_without_command=True)
async def market(ctx):
    await ctx.send('## Market Command Tree.\n - //market map - \n -# Shows a map locating all Market Tables.\n - //market get {item name} - \n -# Shows a map showing where to buy and sell the item specified. "//market get" for more info.\n - //market info {market name} - \n -# Shows an item list for the Market Table specified. "//market info" for more info')

#cmd: market map
@market.command('map')
async def market_map(ctx):
    file = utils.buffer(functions.map.markets_type_map(),'MarketTypes.png')
    await ctx.send('Market Table map:',file=file)
    


#cmd: market get {item}
@market.command('get')
async def market_get(ctx, item: str=None):
    if item == None:
        await ctx.send('## Market Get command.\n Use this command to get a map showing which stars buys and sells a specified item.\n### Syntax: "//market get {item name}"\n - Use `//market get minerals` to get stars that buy Rock, Iron, Gold and Titanium.\n - Use `//market get Rift Crystal` or the shortcut `//crystal` to get stars that sell Rift Crystals.')
        return
    await ctx.typing()
    result = functions.map.market_get_item(item)
    if result is None:
        await ctx.send('Item could not be found.')
    else:
        file = utils.buffer(result,'marketGet.png')
        if item == "minerals":
            await ctx.send("Minerals can be found:", file=file)
        else:
            await ctx.send("Item can be found:", file=file)
            


#cmd: market info {market type}
@market.command("info")
async def market_info(ctx,market: str=None):
    if market is None:
        stringa="## Market Info command.\nUse this to get a list of items in a specified Market Table.\n### Current Market Tables:\n"
        for key in static.allMarkets:
            stringa += '`//market info {}`\n'.format(key[:-6])
        await ctx.send(stringa)
        return
    result = functions.map.market_table(market.lower())
    if result is None:
        await ctx.send('### Invalid "Market Table" Argument.\n - Make sure you\'re using the right syntax: `//market info {market name}`.\n - Have u tried `tourism` or `tech`?\n - Ex: `//market info millitary`')
    else:
        await ctx.send(market+ ":\n" + result)



#>>> Auto Map Updates tree.
@bot.hybrid_group('auto',invoke_without_command=True)
async def auto(ctx):
    await ctx.send(strings.help_update)

@auto.group('map',invoke_without_command=True)
async def auto_map(ctx):
    await ctx.send(strings.help_update)

#cmd: //auto map set
@auto_map.command('set')
async def auto_map_set(ctx, channel: str=None):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain":
        if channel == None:
            functions.auto_map.set_channel(ctx.guild.id,ctx.channel.id)
            await ctx.send(f"Auto map updates will be sent to {ctx.channel.mention}")
        elif utils.is_channel(channel):
            id = utils.extract_id(channel)
            functions.auto_map.set_channel(ctx.guild.id,id)
            await ctx.send(f"Auto map updates will be sent to {channel}")
        else:
            await ctx.send("### Invalid Channel.\nRemember, you just need to `#mention` the desired channel. Or leave the `channel` argument empty to use the current channel.")
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to set a channel for auto updates.")

#cmd: //auto map get
@auto_map.command('get')
async def auto_map_get(ctx):
    channel = functions.auto_map.get_channel(ctx.guild.id)
    if channel is None:
        await ctx.send("There's no Channel defined to get auto updates on this server.")
    else:
        await ctx.send("The https://discord.com/channels/{}/{} channel will receive auto map updates!".format(ctx.guild.id,channel))

#cmd: //auto map test
@auto_map.command('test')
async def auto_map_test(ctx, *, arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and arg[0] == 'n':
        channel = functions.auto_map.get_channel(ctx.guild.id)
        if channel is None:
            await ctx.send("There's no Channel defined to get auto updates on this server.")
        else:
            channel = (bot.get_channel(int(channel)) or bot.fetch_channel(int(channel)))
            await channel.send(f"{ctx.author.mention} ***~~Attacker Faction~~*** successfully sieged ***~~Sector (Star)~~*** taking the station from ***~~Sieged Faction~~***",file=discord.File('output/claimsMap.png'))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")



# change logs cmd
@bot.command('change-log')
async def change_log(ctx, *arg):
    if not arg:
        await ctx.send("## Change Log Command.\nUsed to see all past changes and updates.\n- Syntax: `//change-log {arg}`\n- - -# Where *arg* is a single integer, a list of them, or 'all'\n- Ex: '`//change-log 0`', '`//change-log 2 3 4 7`'.\n- - -# By passing 'all' as *arg* you gather every change-log. Be aware that it will return *all* of them.")
    #Print all if arg == 'all'
    elif arg[0] == "all":
        for log in change_logs.change_list:
            await ctx.send(log)
            await asyncio.sleep(0.7)
    #checks if valid and handles each output
    else:
        await ctx.send("Change Log:")
        for i in arg:
            try:
                int(i)
                if int(i) <= len(change_logs.change_list)-1:
                    try: await ctx.send(change_logs.change_list[int(i)])
                    except Exception as Exp:
                        await ctx.send("Error. Probably invalid argument `{}`".format(i))
                        print("\033[91mError on //change-log:",Exp,"\033[0m")
                else:
                    await ctx.send("Argument is too big. Max is `{}`".format(len(change_logs.change_list)-1))
            except Exception as Exp:
                    await ctx.send("Invalid argument `{}`".format(i))
                    raise
#maybe add a better way to this? Think later :)



#>>> Siege Pings Command Tree
@bot.hybrid_group('siegeping', invoke_without_command=True)
async def siege_pings(ctx):
    await ctx.send(strings.siege_ping)

"""@siege.hybrid_group('ping', invoke_without_command=True)
async def siege_pings(ctx):
    await ctx.send(strings.siege_ping)
"""
#cmd: //siege ping test
@siege_pings.command("test")
async def siege_test(ctx, args):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        channel = functions.siege_pings.get_channel(ctx.guild.id)
        if channel is None:
            await ctx.send("### Guild Inexistent Error.\n Use '`//siegeping set channel`' first.")
            return
            #Quit early if guild inexistent.
        channel = bot.get_channel(int(channel))
        pings_str=""
        for id in functions.siege_pings.get_ids(ctx.guild.id):
             pings_str += "<@{}>, ".format(id)
        await channel.send("**{}** will get attacked in 10 minutes by **{}** at **{}**!!\n{}".format("~~*Defending Faction*~~", "~~*Attacking Faction*~~", "~~*Star & Sector*~~", pings_str))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")

#!!!
# --- 'set' Branch
@siege_pings.group('set', invoke_without_command=True)
async def siege_set(ctx):
    await ctx.send("### Siegepings *SET* Branch.\n - `//siegeping set channel`")

@siege_set.command('channel')
async def siege_set_channel(ctx, channel: str):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not utils.is_channel(channel):
            await ctx.send("### Invalid Channel.\nRemember, you just need to `#mention` the desired channel.")
            return
        functions.siege_pings.set_channel(ctx.guild.id, utils.extract_id(channel))
        await ctx.send(f"Channel {channel} was set to receive siegepings.")
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")


# --- 'get' Branch
@siege_pings.group('get', invoke_without_command=True)
async def siege_get(ctx):
    await ctx.send("### Siegepings *GET* Branch.\n - `//siegeping get channel`\n - `//siegeping get ids`\n - `//siegeping get factions`")

@siege_get.command('channel')
async def siege_get_channel(ctx):
    await ctx.send(
        "Siege pings will be sent to https://discord.com/channels/{}/{}\n-# if the link is broken, try assigning a channel again.".format(
            ctx.guild.id,
            functions.siege_pings.get_channel(ctx.guild.id)))

@siege_get.command('factions')
async def siege_get_factions(ctx):
    textin = ""
    for fac in functions.siege_pings.get_factions(ctx.guild.id):
        textin += fac + "\n"
    await ctx.send("These faction names will trigger pings: ```{}```".format(textin))

@siege_get.command('ids')
async def siege_get_factions(ctx):
    textin = ""
    for id in functions.siege_pings.get_ids(ctx.guild.id):
        id_=utils.extract_id(id)
        try:
            name = await bot.fetch_user(id_)
            textin += "{} <user:{}>\n".format(id, name.name)
        except:
            try:
                name = ctx.guild.get_role(int(id_))
                textin += "{} <role:{}>\n ".format(id, name.name)
            except:
                textin += "{} <uknown>\n".format(id_)
    await ctx.send("These ids will be pinged:\n```{}```".format(textin))


# -- 'add'' Branch
@siege_pings.group('add', invoke_without_command=True)
async def siege_add(ctx):
    await ctx.send("### Siegepings *ADD* Branch.\n - `//siegeping add id`\n - `//siegeping add faction`")

@siege_add.command('id')
async def siege_add_id(ctx, mentionable: str):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if mentionable is None:
            await ctx.send("### Siegeping Add Id Command\nAdd an ID to ping on sieges by mentioning either a user or a role.\nSyntax: `//siegeping add id {@mention}`\n - Ex:\n - - `//siegeping add id @VicTheCloned`\n - - `//siegeping add id @Anti-Siege-Team`\n - - `//siegeping add id @Siege_Pings_Role`")
            return
        elif utils.is_user(mentionable) or utils.is_role(mentionable):
            pass
        else:
            await ctx.send("### Invalid ID.\nRemember, you just need to `@mention` the desired user or role")
            return
        try:
            functions.siege_pings.add_id(ctx.guild.id, mentionable)
        except Exception as e:
            await ctx.send('### Error {}'.format(e))
            raise
        await ctx.send("Successfully added the id {}".format(mentionable))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")

@siege_add.command('faction')
async def siege_add_faction(ctx, *, faction: str=None):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if faction is None:
            await ctx.send("### Siegeping Add Faction Command\nAdd factions to trigger siegepings. For your faction, allies, enemies etc.\nSyntax: `//siegeping add faction {faction name}`\n - Faction names must be exactly equal as in-game and fully written.\n - No 'MMM' or 'FROG' per instance.\n - Be aware of spaces and special characters\n - Ex:\n - - `//siegeping add faction Star`\n - - `//siege ping add faction Massive Man Machinery`\n - - `//siegeping add faction Rabbits`")
            return
        functions.siege_pings.add_faction(ctx.guild.id, faction.strip())
        await ctx.send("Faction '`{}`' added.".format(faction))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")


# -- 'del' Branch
@siege_pings.group('del', invoke_without_command=True)
async def siege_del(ctx):
    await ctx.send("### Siege Pings *DEL* Branch.\n - `//siegeping del id`\n - `//siegeping del faction`")

@siege_del.command('id')
async def siege_del_id(ctx, mentionable: str):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if mentionable is None:
            await ctx.send("### Siegeping Del Id Command\nDelete IDs by mentioning either a user or a role.\nSyntax: `//siegeping del id {@mention}`\n - Ex:\n - - `//siegeping del id @Polarina`\n - - `//siegeping del id @Pro-Siege-Team`\n - - `//siegeping del id &27173828103`")
            return
        elif utils.is_user(mentionable) or utils.is_role(mentionable):
            pass
        else:
            await ctx.send("### Invalid ID.\nRemember, you just need to `@mention` the desired user or role")
            return
        try:
            functions.siege_pings.del_id(ctx.guild.id, mentionable)
        except Exception as e:
            await ctx.send('### Error {}'.format(e))
            raise
        await ctx.send("Successfully deleted the id {}".format(mentionable))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")

@siege_del.command('faction')
async def siege_del_faction(ctx, *, faction: str):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if faction is None:
            await ctx.send("### Siegeping Del Faction Command\nDeletes factions.\nSyntax: `//siegeping del faction {faction name}`\n - Faction names must be exactly equal in memory. To get a list of them use `//siegeping get factions`\n - Be aware of spaces and special characters\n - Ex:\n - - `//siegeping del faction void`\n - - `//siegeping del faction ice cube`\n - - `//siegeping del faction ahoy`")
            return
        functions.siege_pings.del_faction(ctx.guild.id, faction.strip())
        await ctx.send("Faction '`{}`' deleted.".format(faction))
    else:
        await ctx.send("### Permission Error\nYou must be an ADMIN to use this command")




# image generation by @a_person_that_exists1 (KaasKroket)
@bot.group("image", aliases=["im"],invoke_without_command=True)
async def image(ctx):
    return

@image.command("help")
async def send_help_message_image(ctx, arg: str = ""):
    if arg == "": (
        await ctx.send(
            "# Command tree 'image'\nTwo really cool functions by **@KaasKroket** (aka Warden), one applies an image (**//image help apply**), and the other generates an image (**//image help generate**). \n(**//image help ratio**)) is used for getting the ratio of an image automatically."
        )
    )
    elif arg == "apply": (
        await ctx.send(
            "```'//image apply (drone width) (drone height)'```**IMPORTANT** To use the command you need to attach an image and a .dbv file.\n\nTo get a processed drone in game, you should copy the folder that the bot outputs into your local drone folder. \nFor android users this folder should be at: ```Android/Data/com.rizenplanet.droneboiconquest/files/Vehicles```\nFor PC users (Windows) this folder should be located at: ```C:\\Users\\(your user)\\AppData\\LocalLow\\Rizen Planet Studios\\Droneboi_ Conquest\\Vehicles```\n You can do this by downloading it directly from the bot, it is formatted correctly so it should automatically work."
        )
    )
    elif arg == "generate": (
        await ctx.send(
            "```'//image generate (drone width) (drone height) (drone name) (boolean LED mode) '```**IMPORTANT** To use the command you need to attach an image.\n\nTo get a processed drone in game, you should copy the folder that the bot outputs into your local drone folder. \nFor android users this folder should be at: ```Android/Data/com.rizenplanet.droneboiconquest/files/Vehicles```\nFor PC users (Windows) this folder should be located at: ```C:\\Users\\(your user)\\AppData\\LocalLow\\Rizen Planet Studios\\Droneboi_ Conquest\\Vehicles```\n You can do this by downloading it directly from the bot, it is formatted correctly so it should automatically work."
        )
    )
    elif arg == "ratio": (
        await ctx.send(
            "```'//image ratio (desired width or height by typing w10 or h10)'```**IMPORTANT** To use the command you need to attach an image.\n\nThis outputs the image size, ratio, and the matching image width or height with the input."
        )
    )
@image.command("apply")
async def img_apply_to_existing(ctx, droneW: int = 9, droneH: int = 13):
    attachments = ctx.message.attachments
    if len(attachments) < 2:
        await ctx.send("Please attach both an image and a .dbv file.")
        return

    image_attachment = next((a for a in attachments if a.filename.lower().endswith((".png", ".jpg", ".jpeg"))), None)
    dbv_attachment = next((a for a in attachments if a.filename.lower().endswith(".dbv")), None)

    if not image_attachment or not dbv_attachment:
        await ctx.send("Missing required image or .dbv file.")
        return

    await ctx.channel.typing()

    image_path = "output/temp_image.png"
    dbv_path = "output/input.dbv"
    output_path = "output/updated_blocks.dbv"

    await image_attachment.save(image_path)
    await dbv_attachment.save(dbv_path)

    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img)
    img_height, img_width = pixels.shape[:2]

    with open(dbv_path, "r") as f:
        dbv_data = json.load(f)

    color_lines = re.findall(r"([\w\s]+), (\d+), (\d+), (\d+), ([\w\s]+),", imageData.data)
    palette_by_type = {"Armor Block": [], "Other": []}

    for block_type, r, g, b, name in color_lines:
        color_entry = {
            "type": block_type.strip(),
            "name": name.strip(),
            "rgb": (int(r), int(g), int(b))
        }
        if block_type.strip() == "Armor Block":
            palette_by_type["Armor Block"].append(color_entry)
        else:
            palette_by_type["Other"].append(color_entry)


    virtualW = droneW * 2 + 0.5
    virtualH = droneH * 2 + 0.5
    step_x = img_width / virtualW
    step_y = img_height / virtualH
    for block in dbv_data["b"]:
        px, py = block["p"]
        grid_x = int((px + droneW / 2) * 2)
        grid_y = int((-py + droneH / 2) * 2)

        if 0 <= grid_x < virtualW and 0 <= grid_y < virtualH:
            pixel_x = int(grid_x * step_x)
            pixel_y = int(grid_y * step_y)
            rgb = tuple(pixels[pixel_y, pixel_x])

            palette = (
                palette_by_type["Armor Block"]
                if block["n"] == "Armor Block"
                else palette_by_type["Other"]
            )

            if palette:
                closest = min(palette, key=lambda c: compare_colors(rgb, c["rgb"]))
                block["s"] = closest["name"]

    with open(output_path, "w") as f:
        json.dump(dbv_data, f, separators=(",", ":"))

    await ctx.send("Applied image onto your drone:", file=discord.File(output_path, filename="Applied drone.dbv"))

@image.command("generate")
async def img_generate(ctx, droneW: int, droneH: int, droneName: str, hasLeds: bool = False):

    image_path = "output/temp_file_404.png"
    dbv_path = "output/output_blocks.dbv"
    attachment = None

    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
    elif ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if replied_message.attachments:
            attachment = replied_message.attachments[0]

    if not attachment:
        await ctx.send("You didn't provide any image.")
        return

    await ctx.channel.typing()
    await attachment.save(image_path)

    img = Image.open(image_path).convert("RGBA")
    img_resized = img.resize((droneW, droneH), resample=Image.BILINEAR)
    pixels = np.array(img_resized)

    color_lines = re.findall(r"([\w\s]+), (\d+), (\d+), (\d+), ([\w\s]+),", imageData.data)
    color_palette = [{
        "type": block_type.strip(),
        "name": name.strip(),
        "rgb": (int(r), int(g), int(b))
    } for block_type, r, g, b, name in color_lines]

    blocks = []
    nc_connections = []

    if hasLeds:
        visible_pixels = pixels[pixels[:, :, 3] > 0]
        if len(visible_pixels) > 0:
            avg_rgb = tuple(np.mean(visible_pixels[:, :3], axis=0).astype(int))
            closest_color = min(color_palette, key=lambda c: compare_colors(avg_rgb, c["rgb"]))
            signal_color = closest_color["name"]
        else:
            signal_color = "White"

        blocks.append({
            "n": "Constant On Signal",
            "p": [0.0, 0.0],
            "s": signal_color,
            "ni": [0]
        })

        led_index = 1
        iteration_counter = 0

        offset_x = 0.25 if droneW % 2 != 0 else 0.0
        offset_y = 0.25 if droneH % 2 != 0 else 0.0

        for j in range(droneH):
            for i in range(droneW):
                iteration_counter += 1
                if iteration_counter % 500 == 0:
                    await asyncio.sleep(0)

                r, g, b, a = pixels[j, i]
                if a == 0:
                    continue

                px = (i - droneW / 2) * 0.5 + offset_x
                py = (j - droneH / 2) * -0.5 - offset_y
                if px == 0.0 and py == 0.0:
                    continue
                rgb = (r, g, b)
                closest_color = min(color_palette, key=lambda c: compare_colors(rgb, c["rgb"]))

                blocks.append({
                    "n": "LED",
                    "p": [float(px), float(py)],
                    "s": closest_color["name"],
                    "ni": [led_index]
                })

                nc_connections.append({
                    "Item1": led_index,
                    "Item2": 0
                })

                led_index += 1

    else:
        iteration_counter = 0

        for j in range(droneH):
            for i in range(droneW):
                iteration_counter += 1
                if iteration_counter % 10000 == 0:
                    await asyncio.sleep(0)

                r, g, b, a = pixels[j, i]
                if a == 0:
                    continue

                px = i - droneW // 2
                py = j - droneH // 2
                rgb = (r, g, b)
                closest_color = min(color_palette, key=lambda c: compare_colors(rgb, c["rgb"]))

                block_name = "Core" if (px == 0 and py == 0) else closest_color["type"]
                blocks.append({
                    "n": block_name,
                    "p": [float(px), float(py) * -1],
                    "s": closest_color["name"],
                    "ni": []
                })

    ls_value = 0 if ctx.author.id in BOT_OWNER_IDS else 2
    full_output = {
        "n": droneName,
        "gv": "1.5.8",
        "dt": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        "ls": ls_value,
        "b": blocks,
        "nc": nc_connections,
        "ci": []
    }

    with open(dbv_path, "w") as f:
        json.dump(full_output, f, separators=(",", ":"))

    await ctx.send(
        f"Converted image to {'LED drone' if hasLeds else 'drone'}:",
        file=discord.File(dbv_path, filename=f"{droneName}.dbv")
    )


@image.command("ratio")
async def image_ratio(ctx, dimension: str = None):
    import discord
    from PIL import Image
    from math import gcd

    image_path = "output/temp_ratio_check.png"

    attachment = None
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]
    elif ctx.message.reference:
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if replied_message.attachments:
            attachment = replied_message.attachments[0]

    if not attachment:
        await ctx.send("You didn't provide any image.")
        return

    await ctx.channel.typing()
    await attachment.save(image_path)

    img = Image.open(image_path)
    width, height = img.size
    divisor = gcd(width, height)
    simple_width = width // divisor
    simple_height = height // divisor

    response = f"Image size: `{width}x{height}`\nAspect ratio: `{simple_width}:{simple_height}`"

    if dimension:
        try:
            if dimension.lower().startswith("w"):
                target_width = float(dimension[1:])
                calc_height = round((target_width * height) / width, 2)
                response += f"\nIf the drone width = `{target_width}`, the drone height should be `{calc_height}`"
            elif dimension.lower().startswith("h"):
                target_height = float(dimension[1:])
                calc_width = round((target_height * width) / height, 2)
                response += f"\nIf the drone height = `{target_height}`, the drone width should be `{calc_width}`"
            else:
                response += "\nInvalid format. Use `w<number>` or `h<number>`."
        except ValueError:
            response += "\nInvalid number format. Use something like `w10` or `h25`."

    await ctx.send(response)




# >>> Siege Analysis Group Tree
@bot.hybrid_group('analysis',invoke_without_command=True)
async def analysis(ctx):
    await ctx.send("## Siege Analysis Command Tree.\n- //analysis board {n} \n-# Returns a board containing data from the last *n* sieges.\n- //analysis heatmap {n} {sensibility}` - Returns  siege hot map from the last *n* sieges.")

@analysis.command('board')
async def analyBoard(ctx,amount=20,type='overview'):
    #cancel amount too high
    if not ctx.author.id in BOT_OWNER_IDS:
        await ctx.send("### Too High!\nLimited at *200* messages.")
        return
    
    await ctx.send("*Trying to gather info from the last **{}** sieges...*".format(amount))
    
    #get messages
    databaseChannel = 1226483892391903283
    messages = [msg async for msg in bot.get_channel(databaseChannel).history(limit=amount*3)]
    #let ~~terminal~~ and users know
    await ctx.send("Found data for **{}** sieges.".format(int(len(messages)/3)))
    
    #finish by sending full list.
    await ctx.send(functions.claimAnalysis.analysisBoard(claimAnalysis.analysisToDic(messages))[:1999])

#cmd heatmap
@analysis.command('heatmap')
async def analyHot(ctx,amount=30,sensibility=1.0):
    #+++
    kaksnd
    if amount>100 and ctx.author.id!=1195827600925405245:
        await ctx.send("Too High! Max of ***200***")
        return
    if sensibility>10:
        await ctx.send("Sensibility Too High! Max of ***10***")
        return
    if sensibility>10 and ctx.author.id!=1195827600925405245:
        await ctx.send("Too High! Max of ***20***")
        return
    await ctx.send("*Producing heatmap for the last **{}** sieges...*  \n-# *Sensibility {}*".format(amount, sensibility))
    print("--> HeatMap",get_info(ctx))
    #get messages
    databaseChannel = 1226483892391903283
    messages = [msg async for msg in bot.get_channel(databaseChannel).history(limit=amount*3)]
    file = utils.buffer(functions.claimAnalysis.heatmap(messages, sensibility))
    await ctx.send("HeatMap:",file=file)



#for admins
@bot.hybrid_group('cl')
async def color_adm(ctx):
    if ctx.author.id not in CHANGE_COLOR:
        await ctx.send("Prohibited.")
        return

@color_adm.command('set')
async def cladm_set(ctx, faction: str, color: str):
    if ctx.author.id not in CHANGE_COLOR:
        await ctx.send("Prohibited.")
        return
    if not utils.is_hex(color.lower()):
        await ctx.send("Invalid hex")
        return
    functions.faction_color.edit_color(faction,color)
    await ctx.send(f"Eddited `{faction}` color to `{color}`")


@color_adm.command('remove')
async def cladm_rm(ctx, faction: str):
    if ctx.author.id not in CHANGE_COLOR:
        await ctx.send("Prohibited.")
        return
    if faction.lower() in functions.faction_color.get_factions():
        functions.faction_color.rm_faction(faction)
        await ctx.send('Removed `{}`'.format(faction))
    else:
        await ctx.send("Faction not found.")

#shut down bot.
@bot.command('shutdown')
async def shutdown(ctx):
    if ctx.author.id==1195827600925405245:
        await ctx.send('Shutting down...')
        print(' !! SHUTTING DOWN !!')
        print(get_info(ctx))
        await bot.close()







#----- Shutdown and Bot.Run ----

# Signal handling for graceful shutdown
async def shutdown_signal():
    print("Signal received, shutting down...")
    await bot.close()
def handle_signal():
    asyncio.create_task(shutdown_signal())
# Register signal handlers
signal.signal(signal.SIGINT, lambda *_: handle_signal())
signal.signal(signal.SIGTERM, lambda *_: handle_signal())

bot.run(os.getenv('DISCORD_BOT_TOKEN'))  # Make sure to set the token in the environment variable DISCORD_TOKEN