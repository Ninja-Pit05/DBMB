# version 2.0 "last changed mai 15"
from PIL import Image
# Python imports
from discord.ext import commands
import discord
import random
from time import strftime, localtime
import asyncio
import numpy as np
import re
import json
from datetime import datetime
# Python imports

# Our imports
from assets import strings
from database import preliminaryData
from database import changeLog
from database import imageData
from functions import mapCommand
from functions import faction_color
from functions import god_action
from functions import Functions
from functions.Functions import getUpdatesChannels, triggeredSiegePings
from functions.compareColors import compare_colors
from functions.mapCommand import gen_claimsMap
# Our imports


# first bot sets
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='//', intents=intents, help_command=None)


BOT_OWNER_IDS = [
    982591657130213406,
    1195827600925405245,
]


# function to get context info
def get_info(ctx):
    info = " (server:{}/channel:{}/user:{}/time:'{}')".format(ctx.guild.name, ctx.channel.name, ctx.message.author.name,
                                                              strftime("%H:%M:%S", localtime()))
    return info


sosCallsChID = 0


# start phase
@bot.event
async def on_ready():
    print(f'\033[90mSuccessfully logged in as \033[94m{bot.user}!\033[0m')
    print("\033[1;96mInitialized commands phase\033[0m")

    # on wake up map update
    gen_claimsMap() if False else 0
    print("-->Auto map update. '{}'".format(strftime("%H:%M:%S", localtime())))


# trigger for every message
@bot.event
async def on_message(message):
    # checks for commands and execute them.
    await bot.process_commands(message)

    # updade map (server sided)
    if message.content in ['A siege was completed', 'A siege was defended'] and message.channel.id == (
            1326217953326141521):
        await message.channel.send('Updating map...')
        print("-->Conquest Log got an update")
        mapCommand.gen_claimsMap()
        print("<--Map updated {} (auto)".format(strftime("%H:%M:%S", localtime())))
        await message.channel.send('Map updated.')

    # from the command "set-update". Sends auto updates to servers.
    if message.content in ['A siege was completed'] and message.channel.id == (1326217953326141521):
        # Get servers and channels to update maps
        toUpdateChannelList = getUpdatesChannels()
        # here i handle problems with auto maps.
        toUpdateTries = 3
        while True:
            for channel_id in toUpdateChannelList:
                try:
                    # checks for channel existence.
                    channel = bot.get_channel(channel_id)
                except:
                    print("\033[31mERROR\033[0m while trying to get allowed channels IDs")
                    break
                try:
                    # fetchs the message and message embeds.
                    fetchedMes = await message.channel.fetch_message(message.id)
                    embed = fetchedMes.embeds
                    await channel.send("**{}** successfully sieged **{}** taking the station from **{}**".format(
                        embed[0].fields[3].value, embed[0].fields[1].value, embed[0].fields[2].value),
                        file=discord.File('DBmap.png'))
                    # one less item on the list.
                    toUpdateChannelList.pop(toUpdateChannelList.index(channel_id))
                except:
                    print("\033[31mERROR\033[0m while trying to send auto map updates!")
            # tries again, and warns if it wasn't possible to send everything.
            if len(toUpdateChannelList) == 0:
                print("<-- Auto map updates were delivered successfully")
                break
            else:
                toUpdateTries -= 1
                print('-->Trying again...')
            if toUpdateTries == 0:
                print("\033[31m<-- It wasn't possible to send all auto map updates. {} were left... \033[0m ".format(
                    len(toUpdateChannelList)))
                break
        del [toUpdateChannelList, toUpdateTries]

    # siege pings
    if message.content.startswith("A new siege will start in 10 minutes") and message.channel.id == (
            1326217953326141521):
        fetchedMes = await message.channel.fetch_message(message.id)
        embed = fetchedMes.embeds

        # testing
        sentTime = embed[0].timestamp
        receivedTime = fetchedMes.created_at
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
        # testing

        PINGSdict = triggeredSiegePings(embed[0].fields[2].value.lower())
        for key in PINGSdict.keys():
            try:
                pchannel = bot.get_channel(int(key))
                pingsLine = ""
                for id in PINGSdict[key]:
                    pingsLine += "<@{}>".format(id)
                    if PINGSdict[key].index(id) != len(PINGSdict) - 1: pingsLine += ", "
                await pchannel.send(
                    "**{}** will get attacked in 10 minutes by **{}** at **{}**!!\n{}\n-# Latency: {} {}".format(
                        embed[0].fields[2].value, embed[0].fields[3].value, embed[0].fields[1].value, pingsLine,
                        latencyTime, Emo))
            except Exception as exc:
                print("\033[91mError on siege pings '{}' on id {}\033[0m".format(exc, key))
        print("<--Siege pings sent")

    # Coding for SOScalls
    if sosCallsChID != 0:
        if message.channel.id == sosCallsChID and not message.content.startswith("_ _"):
            channel = bot.get_channel(1357771433580953951)
            await channel.send("_ _ {}: {}".format(message.author, message.content))
        if message.channel.id == 1357771433580953951 and not message.content.startswith(
                "_ _") and not message.content.startswith("//attend"):
            channel = bot.get_channel(sosCallsChID)
            await channel.send("_ _ {}".format(message.content))


# ping-pong command
@bot.hybrid_command("ping")
async def ping_pong(ctx):
    await ctx.send("Pong!")
    print("-->Ping received!" + get_info(ctx))


# map command
@bot.command('map')
async def map(ctx):
    if ctx.message.content.startswith('//map update'):
        print("-->Update map command received" + get_info(ctx))
        await ctx.send('Updating the map...')
        mapCommand.gen_claimsMap()
        await ctx.send('Map was updated successfuly!')
        print("<--Map was successfully updated {} (manual)".format(strftime("%H:%M:%S", localtime())))
    else:
        print("-->Map command received" + get_info(ctx))
        await ctx.send('Actual Droneboi Map:')
        await ctx.send(file=discord.File('outputs/claimsMap.png'))


# help command
@bot.command('help')
async def help(ctx):
    await ctx.send(strings.help)
    print("-->Help command received" + get_info(ctx))


# new command
@bot.command('new')
async def new(ctx):
    await ctx.send(strings.new)
    print("-->New command received" + get_info(ctx))


# faction tree. Changes faction color claims.
@bot.group('faction',invoke_without_command=True)
async def faction(ctx):
    ctx.send('### Faction Command Tree. ```faction command\n\n//faction color set "{Hex code}" - edit faction custom color\n     Hex code format should be "#rrggbb"\n     Example: "//faction color set "#ffffff""\n\n//faction color get - return faction colors value.```')

@faction.command('color')
async def faction_color(ctx, *arg):
    #set mode
    if arg[0] == "set":
        #checks HEX code vality
        if len(arg[1]) != 7:
            await ctx.send("Invalid HEX code.\nHEX format should be `#rrggbb`")
            return
        #checks if is on the whitelist
        if faction_color.get_faction(ctx.message.author.name) == "None":
            await ctx.send("You're not allowed to change faction colors in any faction. To be added to the whitelist, ask your faction leader to contact Ninja")
        else:
            #try to change color.
            try:
                await ctx.send(faction_color.edit_color(faction_color.get_faction(ctx.message.author),arg[1]))
                print("--> Faction cmd. Color changed successfuly! {}".format(get_info(ctx)))
            except Exception as Exp:
                await ctx.send("I ran into some internal erros. Please contact my creator.")
                print("\033[31m ERROR! Exception at 'faction color set' : {}".format(Exp), "\033[0m" )
    #get mode
    elif arg[0] == "get":
        #opens database, caches each faction/color pair, then outputs it.
        with open("database/custom_faction_colors.txt") as file:
            String = "```"
            for line in file:
                String += line[line.find("faction:"):line.find("'$'")] + "\n" + line[line.find("color:"):line.find(
                    "color:") + 13] + "\n"
        String += "```"
        await ctx.send(String)
        del String
        print("--> Faction cmd. Color pairs outputed! {}".format(get_info(ctx)))
    else:
        ctx.send("Invalid argument.")


# just print my name.
@bot.command('owner')
async def owner(ctx):
    await ctx.send("Made by Ninja.")
    print("-->Owner command  " + get_info(ctx))


# God mode
@bot.command('god_mode:')
async def GodMod(ctx):
    if ctx.message.author.name == "el_ninja.brain":
        await god_action.god_actions(ctx)
        print("-->God mode" + get_info(ctx) + "[" + ctx.message.content + "]")
    else:
        await ctx.send("You don't have access to that command.")
        print("-->Tried god mode - " + get_info(ctx))


# idk why but feedback
@bot.command('feedback')
async def feedback(ctx):
    if len(ctx.message.content) <= len("//feedback "):
        await ctx.send(
            "This is the feedback command. You can send me ideias pinging me, through a DM or using this command. To use this command, simply type '//feedback (your message)'.")
    else:
        await ctx.send("Your message was received")
        print("-->Yo got feedback" + get_info(ctx))
        with open("database/feedback.txt", "a") as file:
            file.write(ctx.message.content + " " + get_info(ctx) + "\n")


# leaderboard command
@bot.command('leaderboard')
async def leaderboard(ctx):
    print('-->Leaderboard command was used - ' + get_info(ctx))
    await ctx.send("Here is the leaderboard:\n```" + Functions.get_leadership_board() + "```")

@bot.command('lb')
async def lb_short(ctx):
    await leaderboard(ctx)


# crystals command
@bot.command('crystal')
async def crystals(ctx):
    print('--> Crystal command received - ' + get_info(ctx))
    Functions.crystalsLocationMap().save('outputs/CrystalsLocationMap.png')
    await ctx.send('Here is where you can find and buy rift crystals:')
    await ctx.send(file=discord.File('outputs/CrystalsLocationMap.png'))

@bot.command('crystals')
async def crystalls(ctx):
    await crystals(ctx)


##Fun Commands!
# duck
@bot.command('duck')
async def duck(ctx):
    print('-->DUCK!!!' + get_info(ctx))
    fileNumber = random.randint(1, 3)
    if fileNumber == 2:
        await ctx.send(file=discord.File('duck/duck' + str(fileNumber) + '.gif'))
    else:
        await ctx.send(file=discord.File('duck/duck' + str(fileNumber) + '.png'))


# cat
@bot.command('cat')
async def duck(ctx):
    print('-->CAT!!!' + get_info(ctx))
    fileNumber = random.randint(1, 3)
    if fileNumber == 2:
        await ctx.send(file=discord.File('duck/cat' + str(fileNumber) + '.gif'))
    else:
        await ctx.send(file=discord.File('duck/cat' + str(fileNumber) + '.png'))
#No fun anymore!


#market tree
@bot.group('market',invoke_without_command=True)
async def market(ctx):
    await ctx.send('### Market Command Tree.```//market map - Shows a map containing all market types.\n//market get {item name} - Shows a map with the locations to buy and sell the item specified. "//market get" for more info.\n//market info {market name} - Item list that you can buy and sell in that market type. "//market info" for details.```')

#cmd: market map
@market.command('map')
async def market_map(ctx):
    #Gen then caches.
    Functions.marketsTypeMap().save('outputs/MarketTypes.png')
    print('-->Market Type Map command received - ' + get_info(ctx))
    await ctx.send('Market map:')
    await ctx.send(file=discord.File('outputs/MarketTypes.png'))

#cmd: market type map
@market.command('type')
async def market_type_map(ctx, arg):
    if arg == "map":
        #this was the intended way, the other one that is actually the shortcut.
        await market_map(ctx)

#cmd: market get {item}
@market.command('get')
async def market_get(ctx, arg=None):
    if arg == None:
        await ctx.send( 'This is the "`//market get {item name}`" command. Use this command to get a map showing stars that sell and buy specified item.\n Use "`//market get minerals`" to see all the stars that buy rock, iron, gold and titanium.\n Use "`//market get Rift Crystal`" or "`//crystal`" (shortcut) to see all stars that sell Rift Crystals.')
    elif arg == "minerals":
        Functions.marketGetItem(ctx.message.content).save('outputs/marketGet.png')
        print('-->Minerals Location Command Received - ' + get_info(ctx))
        await ctx.send("Minerals can be found:", file=discord.File('outputs/marketGet.png'))
    else:
        resultado = Functions.marketGetItem(ctx.message.content)
        if resultado == None:
            await ctx.send('Item could not be found.')
        else:
            print('--> Market get cmd {{}}. {} ' + ctx.message.content[13:] + ' - ' + get_info(ctx))
            resultado.save('outputs/marketGet.png')
            await ctx.send("Item can be found:", file=discord.File('outputs/marketGet.png'))
        del resultado

#cmd: market info {market type}
@market.command("info")
async def market_info(ctx,arg=None):
    #if empty
    if arg == None:
        stringa="### Market info command. Uses:\n"
        for key in preliminaryData.allMarkets:
            stringa += '`//market info {}`\n'.format(key)
        await ctx.send(stringa)
    #if type exists
    elif arg in preliminaryData.allMarkets.keys() or arg in ['refinery', 'agriculture' ,'military', 'tech', 'tourism', 'industrial']:
        #return market type table
        await ctx.send(arg+ ":\n" + Functions.getMarketTable(arg))
        print('-->Market info about ' + arg + ' - ' + get_info(ctx))
    #if invalid
    else:
        await ctx.send("Invalid command.\nHave u tried `tourismMarket` or `tech`?")


#automatic map updates tree.
@bot.group('auto',invoke_without_command=True)
async def auto(ctx):
    await ctx.send("### Automatic Claims Map Updates command tree.\n'`auto map`' for short.\n'`auto map help`' for more details.")

#other half of the command syntax
@auto.group('map',invoke_without_command=True)
async def auto_map(ctx):
    await ctx.send("### Automatic Claims Map Updates command tree.\n'`auto map`' for short.\n'`auto map help`' for more details.")

#auto map set
@auto_map.command('set')
async def auto_map_set(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and arg[0] == "n":
        try:
            await ctx.send(Functions.setUpdateChannel(ctx))
            print("--> auto map set command received!" + get_info(ctx))
        except:
            await ctx.send("Error... I feel like... something inside me is broken")
            print("--> \033[31m an ERROR ocurred while executing the command set-update.\033[0m")
    else:
        await ctx.send("You must be an ADMIN to set a channel for auto updates.")

#auto map get
@auto_map.command('get')
async def auto_map_get(ctx):
    print("--> auto map get command received!" + get_info(ctx))
    if Functions.getUpdatesChannel(ctx) == None:
        await ctx.send("There's no Channel defined to get auto updates on this server.")
    else:
        channel = (int(Functions.getUpdatesChannel(ctx)))
        await ctx.send(
            "The https://discord.com/channels/{}/{} channel will receive auto map updates!".format(ctx.guild.id,channel))

#auto map test
@auto_map.command('test')
async def auto_map_test(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and arg[0] == 'n':
        print("--> auto map test command received!" + get_info(ctx))
        if Functions.getUpdatesChannel(ctx) == None:
            await ctx.send("There's no Channel defined to get auto updates on this server.")
        else:
            channel = (bot.get_channel(int(Functions.getUpdatesChannel(ctx))) or bot.fetch_channel(int(Functions.getUpdatesChannel(ctx))))
            await channel.send("<@{}> This channel will receive auto map updates!".format(ctx.author.id))
    else:
        await ctx.send("You must be an ADMIN to use this command.")

#auto map help
@auto_map.command('help')
async def auto_map_help(ctx):
    await ctx.send(strings.help_update)


# change logs cmd
@bot.command('change-log')
async def change_log(ctx, *arg):
    #help if empty
    if not arg:
        await ctx.send("### Change Log Command.\nUsed to see all past changes and improvements.\nSyntax: '//change-log <arg>'\nExamples: '`//change-log 0`', '`//change-log 2 3 4 7`'.\nYou can also gather everything using `all` as argument. Be aware that it will return *all* of them.")
    #print every single one if all
    elif arg[0] == "all":
        for log in changeLog.change_list:
            await ctx.send(log)
            await asyncio.sleep(0.5)
    #checks if valid and handles each output
    else:
        await ctx.send("Change Log:")
        print("--> Change Log Cmd {} {}".format(arg,get_info(ctx)))
        for i in arg:
            try:
                int(i)
                if int(i) <= len(changeLog.change_list)-1:
                    try: await ctx.send(changeLog.change_list[int(i)])
                    except Exception as Exp:
                        await ctx.send("Error. Probably invalid argument `{}`".format(i))
                        print("\033[91mError on //change-log:",Exp,"\033[0m")
                else:
                    await ctx.send("Argument is too big. Max is `{}`".format(len(changeLog.change_list)-1))
            except Exception as Exp:
                    await ctx.send("Invalid argument `{}`".format(i))
                    print("\033[91mError on //change-log:",Exp,"\033[0m")

#maybe add other way to call change logs?


# Siege Pings Cmd
@bot.group('siege-ping', invoke_without_command=True)
async def siege_pings(ctx):
    await ctx.send(strings.siege_ping)

# test command
@siege_pings.command("test")
async def siege_test(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        try:
            pchannel = Functions.getSiegePingChannel(ctx)
            if pchannel == "Err:1":
                await ctx.send("Guild inexistent. Use '`//siege-ping set channel`' first.")
            else:
                pchannel = bot.get_channel(int(pchannel))
                try:
                    pingsLine = ""
                    for id in Functions.getSiegePingIds(ctx):
                        pingsLine += "<@{}>, ".format(id)
                    await pchannel.send("**{}** will get attacked in 10 minutes by **{}** at **{}**!!\n{}".format(
                        "~~*Defending Faction*~~", "~~*Attacking Faction*~~", "~~*Star & Sector*~~", pingsLine))
                except Exception as exc:
                    await ctx.send("Seems like i ran to an error. I'm sorry.")
                    print("\033[91mError at siege_test intern try: {}\033[0m".format(exc))
        except Exception as exc:
            await ctx.send("Error while trying to send ping.")
            print("\033[91mError at siege_test external try: {}\033[0m".format(exc))
    else:
        await ctx.send("You must be an admin to use this command.")


# set branch
@siege_pings.group('set', invoke_without_command=True)
async def siege_set(ctx):
    await ctx.send("set `channel`")


@siege_set.command('channel')
async def siege_set_channel(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not arg:
            await ctx.send(
                "Here you should send a `channel ID` to receive siege pings. Or send `here` to use currently channel.")
        else:
            if arg[0] == "here":
                arg = [x for x in arg]
                arg[0] = str(ctx.channel.id)
            try:
                ctx.guild.get_channel(int(arg[0]))
            except:
                await ctx.send("Invalid channel ID")
            else:
                try:
                    Functions.setSiegePingChannel(ctx, arg[0])
                    await ctx.send("Channel set")
                    print("--> Channel for siege pings was set. " + get_info(ctx))
                except Exception as er:
                    print("\033[91;1mError\033[0m on siege_set_channel ({})".format(er))
                    await ctx.send("Something went wrong... Error on siege_set_channel")
    else:
        await ctx.send("You must be an admin to use this command.")


# get brench
@siege_pings.group('get', invoke_without_command=True)
async def siege_get(ctx):
    await ctx.send("get `channel`, `ids` or `factions`")


@siege_get.command('channel')
async def siege_get_channel(ctx):
    try:
        await ctx.send(
            "Siege pings will be sent to https://discord.com/channels/{}/{}\n-# if the link is broken, you're probably using the command wrong.".format(
                ctx.guild.id, Functions.getSiegePingChannel(ctx)))
    except Exception as er:
        print("\033[91;1mError\033[0m on siege_get_channel ({})".format(er))
        await ctx.send("Something went wrong... Error on siege_get_channel")


@siege_get.command('factions')
async def siege_get_factions(ctx):
    try:
        textin = ""
        for fac in Functions.getSiegePingFactions(ctx):
            textin += fac + "\n"
        await ctx.send("These faction names will trigger pings: ```{}```".format(textin))
    except Exception as er:
        print("\033[91;1mError\033[0m on siege_get_factions ({})".format(er))
        await ctx.send("Something went wrong... Error on siege_get_factions")


@siege_get.command('ids')
async def siege_get_factions(ctx):
    try:
        textin = ""
        for item in Functions.getSiegePingIds(ctx):
            try:
                name = await bot.fetch_user(item)
                textin += "{} <user:{}>\n".format(item, name.name)
            except:
                try:
                    name = ctx.guild.get_role(int(item[1:]))
                    textin += "{} <role:{}>\n ".format(item, name.name)
                except:
                    textin += "{} <uknown>\n".format(item)
        await ctx.send("These ids will be pinged:\n```{}```".format(textin))
    except Exception as er:
        print("\033[91;1mError\033[0m on siege_get_ids ({})".format(er))
        await ctx.send("Something went wrong... Error on siege_get_ids")


# add brench
@siege_pings.group('add', invoke_without_command=True)
async def siege_add(ctx):
    await ctx.send(
        "add `id` or `faction`\n`id` can be player id or role with & before it\n`faction` NEEDS to be the exact full name of the faction in-game.")


@siege_add.command('id')
async def siege_add_id(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not arg:
            await ctx.send(
                "Here you shoud send user's or role's ids to receive pings. When adding a role's id, add a `&` just before the id.")
        else:
            validID = False
            try:
                name = await bot.fetch_user(arg[0])
                validID = True
            except:
                try:
                    name = ctx.guild.get_role(int(arg[0][1:]))
                    validID = True
                except:
                    pass
            if validID == True:
                try:
                    res = Functions.addSiegePingId(ctx, arg[0])
                    if res == "Suc":
                        try:
                            name = await bot.fetch_user(arg[0])
                            name = "{} <user:{}>\n".format(arg[0], name.name)
                        except:
                            try:
                                name = ctx.guild.get_role(int(arg[0][1:]))
                                name = "{} <role:{}>\n ".format(arg[0], name.name)
                            except:
                                name = "{} <uknown>\n".format(arg[0])
                        await ctx.send("Successfully added the id `{}`".format(name))
                        print("--> Added id to siege pings. " + get_info(ctx))
                    elif res == "Err:1":
                        await ctx.send("Guild not found. Did you add it with `//siege-ping set channel`?")
                    elif res == "Err:4":
                        await ctx.send("The  id <{}> already exists.".format(arg[0]))
                    else:
                        print("SOMETHING IS WRONG2 ")
                except Exception as er:
                    print("\033[91;1mError\033[0m on siege_add_id ({})".format(er))
                    await ctx.send("Something went wrong... Error on siege_add_id")
            else:
                await ctx.send("Invalid ID. It should be an user id or a role id.")
    else:
        await ctx.send("You need to be an admin to use this command.")


@siege_add.command('faction')
async def siege_add_faction(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not arg:
            await ctx.send(
                'Here you should send a full in-game faction name to trigger pings. If the faction name has spaces, put it between "". Can be yours, your allie, even your enemie. Add one at a time.\n For intance: "Frog", Frog, Star, "Star" or "Massive Manufacturing Machines" will work.')
        else:
            try:
                res = Functions.addSiegePingFaction(ctx, arg[0])
                if res == "Suc":
                    await ctx.send("Faction ''{}'' added.".format(arg[0]))
                    print("--> Added trigger to siege pings. " + get_info(ctx))
                elif res == "Err:1":
                    await ctx.send("Guild not found. Did you add it with `//siege-ping set channel`?")
                elif res == "Err:2":
                    await ctx.send("''{}'' already exists.".format(arg[0]))
                else:
                    print("SOMETHING IS WRONG ")
            except Exception as er:
                print("\033[91;1mError\033[0m on siege_add_faction ({})".format(er))
                await ctx.send("Something went wrong... Error on siege_add_faction")
    else:
        await ctx.send("You must be an admin to use this command.")


# del brench
@siege_pings.group('del', invoke_without_command=True)
async def siege_del(ctx):
    await ctx.send(
        "delete an `id` or `faction`\n`id` can be player id or role with & before it\n`faction` should be it's name.")


@siege_del.command('id')
async def siege_del_id(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not arg:
            await ctx.send(
                "Here you shoud send user's or role's ids to delete. When deleting a role's id, add a `&` just before the id.")
        else:
            try:
                res = Functions.delSiegePingId(ctx, arg[0])
                if res == "Suc":
                    await ctx.send("Id ''{}'' deleted.".format(arg[0]))
                    print("--> Deleted ID to siege pings. " + get_info(ctx))
                elif res == "Err:1":
                    await ctx.send("Guild not found. Did you add it with `//siege-ping set channel`?")
                elif res == "Err:3":
                    await ctx.send("''{}'' already inexistent.".format(arg[0]))
                else:
                    print("SOMETHING IS WRONG ")
            except Exception as er:
                print("\033[91;1mError\033[0m on siege_del_id ({})".format(er))
                await ctx.send("Something went wrong... Error on siege_del_id")
    else:
        await ctx.send("You must be an admin to use this command.")


@siege_del.command('faction')
async def siege_del_faction(ctx, *arg):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and "n" in arg:
        if not arg:
            await ctx.send(
                'Here you should send the faction name. If the faction name has spaces, put it between "". Del one at a time.\n For intance: "frog clan", Star, "Star" or "Massive Manufacturing Machines" will work.')
        else:
            try:
                res = Functions.delSiegePingFaction(ctx, arg[0])
                if res == "Suc":
                    await ctx.send("Faction ''{}'' deleted.".format(arg[0]))
                    print("--> Deleted trigger to siege pings. " + get_info(ctx))
                elif res == "Err:1":
                    await ctx.send("Guild not found. Did you add it with `//siege-ping set channel`?")
                elif res == "Err:3":
                    await ctx.send("''{}'' already inexistent.".format(arg[0]))
                else:
                    print("SOMETHING IS WRONG ")
            except Exception as er:
                print("\033[91;1mError\033[0m on siege_del_faction ({})".format(er))
                await ctx.send("Something went wrong... Error on siege_del_faction")
    else:
        await ctx.send("You must be an admin to use this command")


# command used for me to help people in other servers
@bot.group('call', invoke_without_command=True)
async def sosCall(ctx):
    await ctx.send(strings.sosCall)


@sosCall.command('status')
async def callStatus(ctx, *arg):
    print(arg)
    if len(arg) > 0 and arg[0] == 'all':
        with open("database/calls.txt") as file:
            listCalls = ""
            for line in file:
                if str(ctx.guild.id) in line:
                    pieces = line.split(";")
                    match pieces[2]:
                        case "0":
                            status = "🟠 Waiting Connection"
                        case "1":
                            status = "🟢 Connected"
                        case "2":
                            status = "🟡 Paused"
                    listCalls += "\n`Channel:`https://discord.com/channels/{}/{}  `ID:{}\nStatus:{}`\n".format(
                        pieces[0], pieces[1], pieces[1], status)
            await ctx.send("List of request status:\n{}".format(listCalls))

    else:
        with open("database/calls.txt") as file:
            for line in file:
                if str(ctx.guild.id) in line and str(ctx.channel.id) in line:
                    pieces = line.split(";")
                    if "\n" in pieces[2]: pieces[2] = pieces[2][:-1]
                    match pieces[2]:
                        case "0":
                            status = "🟠 Waiting Connection"
                        case "1":
                            status = "🟢 Connected"
                        case "2":
                            status = "🟡 Paused"
                    break
            try:
                status
            except:
                status = "🔴 Closed"
            await ctx.send("`Connection Status: {}`".format(status))


@sosCall.command('help')
async def callHelp(ctx):
    print("--> A Call was requested.{}".format(get_info(ctx)))
    with open("database/calls.txt") as file:
        existent = False
        for line in file:
            if str(ctx.guild.id) in line and str(ctx.channel.id) in line:
                pieces = line.split(";")
                if "\n" in pieces[2]: pieces[2] = pieces[2][:-1]
                match pieces[2]:
                    case "0":
                        status = "🟠 Waiting Connection"
                    case "1":
                        status = "🟢 Connected"
                    case "2":
                        status = "🟡 Paused"
                await ctx.send("Request already exists for this channel.\n`Connection Status: {}`".format(status))
                existent = True
    if existent == False:
        with open("database/calls.txt", "a") as file:
            file.write("{};{};0\n".format(ctx.guild.id, ctx.channel.id))
            await ctx.send("Request Made.\n `Connection Status: 🟠 Waiting Connection`")
            message = bot.get_channel(1357771433580953951)
            with open("database/calls.txt") as file:
                index = 0
                for line in file:
                    index += 1
            await message.send("<@1195827600925405245> You're getting called! Index:{}".format(index))


@sosCall.command('cancel')
async def callCancel(ctx):
    with open("database/calls.txt") as file:
        newFile = ""
        for line in file:
            if str(ctx.guild.id) not in line and str(ctx.channel.id) not in line:
                newFile += line
            else:
                pieces = line.split(";")
                print(pieces)
                if pieces[2] in ["1\n", "1"]:
                    global sosCallsChI
                    sosCallsChID = 0
        if newFile == file:
            await ctx.send("There's no call request to cancel in this channel.\n`Connection Status: 🔴 Closed`")
        else:
            await ctx.send("Canceled the call request.\n`Connection Status: 🔴 Closed`")
            with open("database/calls.txt", "w") as fil:
                fil.write(newFile)


# the counter part of sosCall. sosAttend
@bot.group("attend", invoke_without_command=True)
async def sosAttend(ctx):
    if ctx.channel.id == 1357771433580953951:
        await ctx.send(
            "Command tree *attend* used to help people.\n\n```//attend list\n//attend accept {index}\n//attend decline {index}```")


@sosAttend.command("list")
async def sosAttendList(ctx):
    if ctx.channel.id == 1357771433580953951:
        with open("database/calls.txt") as file:
            listCalls = ""
            index = 0
            for line in file:
                if "\n" in line: line = line[:-1]
                pieces = line.split(";")
                if len(pieces) > 1:
                    match pieces[2]:
                        case "0":
                            status = "🟠 Waiting Connection"
                        case "1":
                            status = "🟢 Connected"
                        case "2":
                            status = "🟡 Paused"
                    listCalls += "{}# Faction:'{}'  Channel:'{}' Status:{}\n\n".format(index,
                                                                                       await bot.fetch_guild(pieces[0]),
                                                                                       await bot.fetch_channel(
                                                                                           pieces[1]), status)
                else:
                    listCalls += "{}# ".format(index) + line + "\n\n"
                index += 1
            await ctx.send("```{}```".format(listCalls))


@sosAttend.command("decline")
async def sosAttendDecline(ctx, *arg):
    if ctx.channel.id == 1357771433580953951:
        with open("database/calls.txt") as file:
            index = 0
            newFile = ""
            for line in file:
                if str(index) not in arg:
                    newFile += line
                else:
                    pieces = line.split(";")
                    if len(pieces) > 1:
                        message = bot.get_channel(int(pieces[1]))
                        global sosCallsChID
                        sosCallsChID = 0
                        await message.send("Your Call was declined or was closed.\n`Connection Status: 🔴 Closed`")
                index += 1
            with open("database/calls.txt", "w") as fil:
                fil.write(newFile)
        await ctx.send("Declined")


@sosAttend.command("accept")
async def sosAttendAccept(ctx, arg):
    if ctx.channel.id == 1357771433580953951:
        with open("database/calls.txt") as file:
            index = 0
            newFile = ""
            for line in file:
                pieces = line.split(";")
                if str(index) != arg:
                    if len(pieces) > 1 and "1" in pieces[2]:
                        message = bot.get_channel(int(pieces[1]))
                        await message.send("Your call was put on wait mode.\n`Connection Status: 🟡 Paused`")
                        pieces[2] = "2\n"
                    else:
                        pass
                elif str(index) == arg:
                    pieces[2] = "1\n"
                    global sosCallsChID
                    sosCallsChID = int(pieces[1])
                    await ctx.send("Connected to {}#   `Status: 🟢 Connected`".format(index))
                index += 1
                try:
                    line = "{};{};{}".format(pieces[0], pieces[1], pieces[2])
                except:
                    pass
                newFile += line
            with open("database/calls.txt", "w") as fil:
                fil.write(newFile)
            print("!-!Call Completed")


# image generation by @a_person_that_exists1 (KaasKroket)
@bot.group("image", aliases=["im"],invoke_without_command=True)
async def image(ctx):
    return


@image.command("help")
async def send_help_message_image(ctx, arg: str = ""):
    if arg == "": (
        await ctx.send(
            "# Command tree 'image'\nTwo really cool functions by **@KaasKroket** (aka Warden), one applies an image (**//image help apply**), and the other generates an image (**//image help generate**)"
        )
    )
    elif arg == "apply": (
        await ctx.send(
            "```'//image apply (drone width) (drone height)'```**IMPORTANT** To use the command you need to attach an image and a .dbv file.\n\nTo get a processed drone in game, you should copy the folder that the bot outputs into your local drone folder. \nFor android users this folder should be at: ```Android/Data/com.rizenplanet.droneboiconquest/files/Vehicles```\nFor PC users (Windows) this folder should be located at: ```C:\\Users\\(your user)\\AppData\\LocalLow\\Rizen Planet Studios\\Droneboi_ Conquest\\Vehicles```\n You can do this by downloading it directly from the bot, it is formatted correctly so it should automatically work."
        )
    )
    elif arg == "generate": (
        await ctx.send(
            "```'//image generate (drone width) (drone height) (drone name)'```**IMPORTANT** To use the command you need to attach an image.\n\nTo get a processed drone in game, you should copy the folder that the bot outputs into your local drone folder. \nFor android users this folder should be at: ```Android/Data/com.rizenplanet.droneboiconquest/files/Vehicles```\nFor PC users (Windows) this folder should be located at: ```C:\\Users\\(your user)\\AppData\\LocalLow\\Rizen Planet Studios\\Droneboi_ Conquest\\Vehicles```\n You can do this by downloading it directly from the bot, it is formatted correctly so it should automatically work."
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

    image_path = "outputs/temp_image.png"
    dbv_path = "outputs/input.dbv"
    output_path = "outputs/updated_blocks.dbv"

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
async def img_generate(ctx, droneW: int, droneH: int, droneName: str):
    if (droneW > 500 or droneH > 500):
        if not(ctx.author.id in BOT_OWNER_IDS) :
            await ctx.send("Too large size, request denied when greater then 500 blocks.")
            return

    image_path = "outputs/temp_file_404.png"
    dbv_path = "outputs/output_blocks.dbv"
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
    for j in range(droneH):
        for i in range(droneW):
            r, g, b, a = pixels[j, i]
            if a == 0:
                continue

            rgb = (r, g, b)
            closest_color = min(color_palette, key=lambda c: compare_colors(rgb, c["rgb"]))

            px = i - droneW // 2
            py = j - droneH // 2

            blocks.append({
                "n": closest_color["type"],
                "p": [float(px), float(py) * -1],
                "r": 0,
                "f": False,
                "s": closest_color["name"],
                "wg": 3,
                "c": [],
                "ni": []
            })

    ls_value = 3 if ctx.author.id in BOT_OWNER_IDS else 2
    full_output = {
        "n": droneName,
        "gv": "1.5.4",
        "dt": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "ls": ls_value,
        "b": blocks,
        "nc": [],
        "ci": []
    }

    with open(dbv_path, "w") as f:
        json.dump(full_output, f, separators=(",", ":"))

    await ctx.send("Converted image to drone:", file=discord.File(dbv_path, filename=f"{droneName}.dbv"))



@image.command("ratio")
async def image_ratio(ctx, dimension: str = None):
    import discord
    from PIL import Image
    from math import gcd

    image_path = "outputs/temp_ratio_check.png"

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





bot.run('MTM3MTg4NjY1MjUwNjc2NzQwMQ.GGV7X3.ZQzcvmAgcEr3xRMb-opLj3Apmurov_eF8tHY0U')


# trash that i keep here for some reason
# these are "debug" and testing functions i use from time to time.

@bot.command('test')
async def tst(ctx):
    print(ctx.guild.id)
    print("hm")


# @bot.command('embed')
async def emb(ctx, id):
    mes = await ctx.channel.fetch_message(id)
    mis = (mes.embeds)[0].fields[0]
    print(mes.embeds[0].fields[3])
    print(mis.value)


@bot.command('embed')
async def emb(ctx, id):
    mes = await ctx.channel.fetch_message(id)
    mis = (mes.embeds)[0].fields[0]
    print(mes.embeds[0].fields[3])
    print(mis.name)
    print(mes.embeds[0].fields[3].value.lower())
    print(mes.embeds[0].timestamp)
    print(mes.created_at)


@bot.command('embedo')
async def emb(ctx, id):
    mes = await ctx.channel.fetch_message(id)
    embe = (mes.embeds)
    await ctx.send(mes.content, embeds=embe)
    for i in embe:
        a = (i.timestamp)
        print(i.timestamp)
    print(mes.created_at)
    print(a - (mes.created_at))
    print((mes.created_at) - a)
