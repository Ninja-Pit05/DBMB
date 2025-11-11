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



#Used to extract my weird db from before 2.1
def a():
    fileName="../database/to_update/siegePingList.txt"
    outlist={}
    with open(fileName) as file:
        for line in file:
            outlist[line[:line.find(":")]]={'channel':line[line.find("::")+2:line.find(";;")],"factions":line[line.find(";;")+2:line.find(";:;:")].split(","),"ids":line[line.find(";:;:")+4:line.find(":;:;")].split(",")}
    return outlist