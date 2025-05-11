
async def god_actions(ctx):
    
    #help
    if ctx.message.content == "//god_mode: get help":
        await ctx.send("```color whitelist\nfaction colors list```")
    
    
    #get modules
    if ctx.message.content == "//god_mode: get color whitelist":
        with open("database/Allowed_Faction_Owners.txt") as file:
            await ctx.send("Changing Faction color whitelist: ```{}```".format(file.read()))
            
    if ctx.message.content == "//god_mode: get faction colors list":
        with open("database/custom_faction_colors.txt") as file:
            await ctx.send("custom faction colors list: ```{}```".format(file.read()))
            
    #edit modules
    if ctx.message.content.startswith("//god_mode: set color whitelist") and ctx.message.content.find("```") != -1 and ctx.message.content.find("```",ctx.message.content.find("```")+3) != -1:
        with open("database/Allowed_Faction_Owners.txt","w") as file:
            file.write(ctx.message.content[ctx.message.content.find("```")+3:ctx.message.content.find("```",ctx.message.content.find("```")+3)])
            await ctx.send("Successful changed file's content.")
            
    if ctx.message.content.startswith("//god_mode: set faction colors list") and ctx.message.content.find("```") != -1 and ctx.message.content.find("```",ctx.message.content.find("```")+3) != -1:
        with open("database/custom_faction_colors.txt","w") as file:
            file.write(ctx.message.content[ctx.message.content.find("```")+3:ctx.message.content.find("```",ctx.message.content.find("```")+3)])
            await ctx.send("Successful changed file's content.")
        