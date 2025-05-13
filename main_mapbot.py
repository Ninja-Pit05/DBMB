# version 2.0

# Python imports
from discord.ext import commands
import discord
from urllib import request
from PIL import Image, ImageDraw, ImageFont
import random
from time import strftime, localtime
import asyncio
# Python imports

# Our imports
from assets import strings
from functions import mapCommand
from functions import faction_color
from functions import god_action
from functions import Functions
from database import preliminaryData
from database import changeLog

# Our imports


# first bot sets
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='//', intents=intents, help_command=None)


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
    gen_map() if False else 0
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
        with open("mapCommand.py") as file: exec(file.read())
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
    elif ctx.message.content == ('//map'):
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


# faction color command
@bot.command('faction')
async def faction(ctx):
    message = (ctx.message.content)
    print("-->faction command received" + get_info(ctx))
    # Set color part
    if message[:20] == "//faction color set ":
        if len(message) == 29:
            if faction_color.get_faction(ctx.message.author.name) == "None":
                await ctx.send(
                    "You're not allowed to change faction colors in any faction. To be added to the whitelist, ask your faction leader to dm Ninja")
                print("<--User not allowed '{}' for faction set color command".format(ctx.message.author.name))
            else:
                try:
                    await ctx.send(faction_color.edit_color(faction_color.get_faction(ctx.message.author),
                                                            ctx.message.content[21:-1]))
                    print("<--User '{}' tried change '{}' color to '{}'.".format(ctx.message.author.name,
                                                                                 faction_color.get_faction(
                                                                                     ctx.message.author)[:-1],
                                                                                 ctx.message.content[21:-1]))
                except Exception as ex:
                    await ctx.send("Uh... I ran into some internal errors. Please contact my creator.   :{}".format(ex))
        else:
            await ctx.send('Invalid command. Command format should be: //faction color set "#rrggbb"')
    # get part
    elif message[:19] == "//faction color get":
        with open("database/custom_faction_colors.txt") as file:
            String = "```"
            for line in file:
                String += line[line.find("faction:"):line.find("'$'")] + "\n" + line[line.find("color:"):line.find(
                    "color:") + 13] + "\n"
        String += "```"
        await ctx.send(String)
        del String
        print("<--It was a get color command")

    else:
        await ctx.send(
            '```faction command\n\n//faction color set "{Hex code}" - edit faction custom color\n     Hex code format should be "#rrggbb"\n     Example: "//faction color set "#ffffff""\n\n//faction color get - return faction colors value.```')


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
    print('-->Crystals command received - ' + get_info(ctx))
    Functions.crystalsLocationMap().save('outputs/CrystalsLocationMap.png')
    await ctx.send('Here is where you can find and buy rift crystals:')
    await ctx.send(file=discord.File('outputs/CrystalsLocationMap.png'))


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


# market related command
@bot.command('market')
async def maket(ctx):
    if ctx.message.content in ['//market', '//market ']:
        await ctx.send(
            'This is the market command.```//market map - Shows a map containing all market types.\n//market get {item name} - Shows a map with the locations to buy and sell the item specified. "//market get" for more info.\n//market info {market name} - Item list that you can buy and sell in that market type. "//market info" for details.```')
    elif ctx.message.content.startswith('//market type map') or ctx.message.content.startswith('//market map'):
        Functions.marketsTypeMap().save('outputs/MarketTypes.png')
        print('-->Market Type Map command received - ' + get_info(ctx))
        await ctx.send('Market map:')
        await ctx.send(file=discord.File('outputs/MarketTypes.png'))
    elif ctx.message.content in ['//market get', '//market get ']:
        await ctx.send(
            'This is the "`//market get {item name}`" command. Use this command to get a map showing stars that sell and buy specified item.\n Use "`//market get minerals`" to see all the stars that buy rock, iron, gold and titanium.\n Use "`//market get Rift Crystal`" or "`//crystal`" to see all stars that sell Rift Crystals.')
    elif ctx.message.content == '//market get minerals':
        Functions.marketGetItem(ctx.message.content).save('outputs/marketGet.png')
        print('-->Minerals Location Command Received - ' + get_info(ctx))
        await ctx.send("Minerals can be found:", file=discord.File('outputs/marketGet.png'))
    elif ctx.message.content.startswith('//market get '):
        resultado = Functions.marketGetItem(ctx.message.content)
        if resultado == None:
            await ctx.send('Item could not be found.')
        else:
            print('-->cmd Market get ' + ctx.message.content[13:] + ' - ' + get_info(ctx))
            resultado.save('outputs/marketGet.png')
            await ctx.send("Item can be found:", file=discord.File('outputs/marketGet.png'))
        del resultado
    elif ctx.message.content == '//market info':
        print('-->Market info - ' + get_info(ctx))
        stringa = 'Possible commands:\n'
        for key in preliminaryData.allMarkets:
            stringa += '`//market info {}`\n'.format(key)
        await ctx.send(stringa)
    elif ctx.message.content.startswith('//market info '):
        if ctx.message.content[14:] in preliminaryData.allMarkets.keys() or ctx.message.content[14:] in ['refinery',
                                                                                                         'agriculture',
                                                                                                         'military',
                                                                                                         'tech',
                                                                                                         'tourism',
                                                                                                         'industrial']:
            await ctx.send(ctx.message.content[14:] + ":\n" + Functions.getMarketTable(ctx.message.content[14:]))
            print('-->Market info about ' + ctx.message.content[14:] + ' - ' + get_info(ctx))
        else:
            await ctx.send('Invalid market type. Have you tried "refinery", "agriculture" or "tourismMarket"?')
    else:
        await ctx.send('Invalid command.')


# auto map update channel set
@bot.command('set-update')
async def setChannelUpdates(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and ctx.message.content == "//set-update n":
        try:
            await ctx.send(Functions.setUpdateChannel(ctx))
            print("--> set update channel command received!" + get_info(ctx))
        except:
            await ctx.send("Error... I feel like... something inside me is broken")
            print("--> \033[31m an ERROR ocurred while executing the command set-update.\033[0m")
    else:
        await ctx.send("You must be an ADMIN to set a channel for auto updates.")


# auto map update, channel check
@bot.command('test-update')
async def checkChannelUpdates(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.name == "el_ninja.brain" and ctx.message.content == "//test-update n":
        print("--> test update channel command received!" + get_info(ctx))
        if Functions.getUpdatesChannel(ctx) == None:
            await ctx.send("There's no Channel defined to get auto updates on this server.")
        else:
            channel = (bot.get_channel(int(Functions.getUpdatesChannel(ctx))) or bot.fetch_channel(
                int(Functions.getUpdatesChannel(ctx))))
            await channel.send("<@{}> This channel will receive auto map updates!".format(ctx.author.id))
    else:
        await ctx.send("You must be an ADMIN to use this command.")


# get the channel that gets auto updates
@bot.command('get-update')
async def checkChannelUpdates(ctx):
    print("--> get update channel command received!" + get_info(ctx))
    if Functions.getUpdatesChannel(ctx) == None:
        await ctx.send("There's no Channel defined to get auto updates on this server.")
    else:
        channel = (int(Functions.getUpdatesChannel(ctx)))
        await ctx.send(
            "The https://discord.com/channels/{}/{} channel will receive auto map updates!".format(ctx.guild.id,
                                                                                                   channel))


# help for set-update related commands
@bot.command('help-update')
async def help_update(ctx):
    await ctx.send(strings.help_update)


# change log command
@bot.command('change-log')
async def change_log(ctx, arg=None):
    print("--> Accessed change log" + get_info(ctx))
    if arg == None:
        await ctx.send(
            "This is the change log command. You can see all past updates and improvements trough `'//change-log <arg>'` where arg is a number or a list of numbers.\n\nExamples: `//change-log 0`, `//change-log 2,3,4,7`\nYou can also gather all change logs passing 'all' as the argument. Be aware that it will return *all* of them.")
    await ctx.send("DB Map bot - Change Log:")
    try:
        if int(arg) > len(changeLog.change_list) - 1:
            await ctx.send("Too big. Max:{}".format(len(changeLog.change_list) - 1))
        else:
            await ctx.send(changeLog.change_list[int(arg)])
    except Exception as e:
        try:
            for num in arg.split(","):
                await ctx.send(changeLog.change_list[int(num)])
        except Exception as es:
            try:
                if arg == "all":
                    for log in changeLog.change_list:
                        await ctx.send(log)
                        await asyncio.sleep(0.5)
                else:
                    print("\033[31m", e, es, "\033[0m")
                    await ctx.send("Invalid argument.")
            except Exception as et:
                print("\033[31m", e, es, et, "\033[0m")
                await ctx.send("Invalid argument.")


# Branch of code that handles siege pings. I took a diferent approach and used groups and subgroups instead of the previous approach of evaluating message content.
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
                await ctx.send("Guild inexistent. Use //siege-ping set channel first.")
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
        if len(arg) == 0:
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
        if len(arg) == 0:
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
        if len(arg) == 0:
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
        if len(arg) == 0:
            await ctx.send(
                "Here you shoud send user's or role's ids to delete. When adding a role's id, add a `&` just before the id.")
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
        if len(arg) == 0:
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
@bot.group("image", invoke_without_command=True)
async def image(ctx):
    await ctx.send(
        "Command tree 'image'\nA really cool function by @KaasKroket which generates images on DB given an image.\n```'//image apply (drone width) (drone height) (blocks to exclude)'\nGenerates an image.```")


@image.command("apply")
async def img_apply(ctx, droneW, droneH, toExclude):
    await ctx.send("This would be the output? no ideia.{} {} {}".format(droneW, droneH, toExclude))
    if not ctx.message.attachments:
        await ctx.send("You didn't provide any file.")
    else:
        await ctx.channel.typing()
        await ctx.message.attachments[0].save("outputs/temp_file_404.png")

        # Do stuff

        await ctx.send("Aftermath:", file=discord.File("outputs/temp_file_404.png"))


bot.run('')


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
