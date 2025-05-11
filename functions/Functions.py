#2.0

#imports
from PIL import Image, ImageDraw, ImageFont
from database.preliminaryData import starsNC
from database.preliminaryData import *
#imports

#
def get_leadership_board():
    from urllib import request
    #needed imports ^
    
    #Request
    site1 = r"https://droneboi.io/api/Conquest/GetClaims"
    URLrequest = request.Request(site1 , data=None, headers = {'User-Agent': 'DBmapBOT'})

    #requests and stores an HTTP response object. Then into str object.
    WebObj=request.urlopen(URLrequest)
    info=str(WebObj.read())
    
    #How many blocks?
    blocks=info.count("{")

    #Put it into a list
    rawList=[]
    last=0
    for i in range(blocks):
       oPen=info.find("{",last)
       close=info.find("}",last)+1
       rawList+=[info[oPen:close]]
       last=close

    #Delete what i don't want
    for item in rawList:
        rawList[rawList.index(item)]=item[item.find('"ownerName":')+12:]
    #del rawList
    
    #a bit more cleaning
    clearList=[]
    for item in rawList:
        output=""
        for a in item:
            if a not in ["{","}",'"']:
                output+=a
        clearList+=[output]
    del output,rawList
    
    #final dic with name and contagem
    finalDic={}
    for item in clearList:
        if item not in finalDic:
            finalDic[item]=1
        else:
            finalDic[item]+=1
    
    #sorting dic
    preDic={}
    keylist=list(finalDic.keys())
    while len(keylist) > 0:
        biigger=""
        n=0
        for item in keylist:
            if finalDic[item] > n:
                biigger , n = item , finalDic[item]
        keylist.pop(keylist.index(biigger))
        preDic[biigger]=n
    finalDic=preDic
    del [preDic,biigger,n,keylist,clearList]
    #now the final str
    String=""
    for faction in finalDic:
        String +=faction+" : owns "+str(finalDic[faction])+" station(s).\n"
    
    #return what matters and clear trash
    return String
    del[String,finalDic]





#here a lot of draw options. Maybe not the best way? but idc
def drawCenteredSquare(cords,size,color,widt,image):
    draw = ImageDraw.Draw(image)
    draw.rectangle(((cords[0]-size/2,cords[1]-size/2),(cords[0]+size/2,cords[1]+size/2)), outline=color, width=widt)
#working perfectly

def drawCenteredHalfSquare(cords,size,color,widt,image,orient=0):
    draw = ImageDraw.Draw(image)
    if orient==0: orien=-1
    else: orien=1
    
    #lado
    draw.line(((cords[0]+(-size/2+widt/2)*orien-orien,cords[1]-size/2),(cords[0]+(-size/2+widt/2)*orien-orien,cords[1]+size/2)),fill=color,width=widt)
    #cima e baixo
    draw.line(((cords[0]+(-size/2+widt/2)*orien,cords[1]-size/2+widt/2),(cords[0]-widt*2*orien,cords[1]-size/2+widt/2)),fill=color,width=widt)
    draw.line(((cords[0]+(-size/2+widt/2)*orien,cords[1]+size/2-widt/2-orien),(cords[0]-widt*2*orien,cords[1]+size/2-widt/2-orien)),fill=color,width=widt)
    
def drawCenteredThirdSquare(cords,size,color,widt,image,orient=0):
    draw = ImageDraw.Draw(image)
    if orient==0:
        draw.line(((cords[0]+(-size/2+widt/2)-1,cords[1]-size/2+1),(cords[0]+(-size/2+widt/2)-1,cords[1]+size/4-widt*2)),fill=color,width=widt)
        draw.line(((cords[0]+(-size/2+widt/2),cords[1]-size/2+widt/2),(cords[0]-widt*2,cords[1]-size/2+widt/2)),fill=color,width=widt)
    elif orient==2:
        draw.line(((cords[0]+size/2-widt/2-1,cords[1]-size/2),(cords[0]+size/2-widt/2-1,cords[1]+size/4-widt*2)),fill=color,width=widt)
        draw.line(((cords[0]+size/2-widt/2,cords[1]-size/2+widt/2),(cords[0]+widt*2,cords[1]-size/2+widt/2)),fill=color,width=widt)
    elif orient==1:
        draw.line(((cords[0]+size/2-widt/2,cords[1]+size/2-widt/2),(cords[0]-size/2+widt,cords[1]+size/2-widt/2)),fill=color,width=widt)
        draw.line(((cords[0]+size/2-widt/2,cords[1]+size/2-1),(cords[0]+size/2-widt/2,cords[1]+size/4+widt*2)),fill=color,width=widt)
        draw.line(((cords[0]-size/2+widt/2,cords[1]+size/2-1),(cords[0]-size/2+widt/2,cords[1]+size/4+widt*2)),fill=color,width=widt)
        
def drawCenteredQuadsSquare(cords,size,color,widt,image,orient=0):
    draw = ImageDraw.Draw(image)
    if orient in [1,3]:
        oriY=1
    else: oriY=-1
    if orient in [1,2]:
        oriX=1
    else: oriX=-1
    draw.line(((cords[0]+(-size/2+widt/2)*oriX-oriX,cords[1]+(-size/2)*oriY+oriY),(cords[0]+(-size/2+widt/2)*oriX-oriX,cords[1]+(-widt*2)*oriY)),fill=color,width=widt)
    draw.line(((cords[0]+(-size/2+widt/2)*oriX,cords[1]+(-size/2+widt/2)*oriY),(cords[0]+(-widt*2)*oriX,cords[1]+(-size/2+widt/2)*oriY)),fill=color,width=widt)


def draw_claims(star,size,widt,image,starsSO,colorDic):
    
    
    draw = ImageDraw.Draw(image)
    if len(starsSO[star]) == 1:
        drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),size,colorDic[starsSO[star][0]],widt,image)
    if len(starsSO[star]) ==2:
        for owner in range(len(starsSO[star])):
           drawCenteredHalfSquare(( starsNC[star][0]+200,starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner)
    if len(starsSO[star])==3:
        for owner in range(len(starsSO[star])):
           drawCenteredThirdSquare(( starsNC[star][0]+200,starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner)
    if len(starsSO[star])==4:
        for owner in range(len(starsSO[star])):
           drawCenteredQuadsSquare(( starsNC[star][0]+200,starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner+1)




#just to get the crystals location map
def crystalsLocationMap():
    from functions.Functions import drawCenteredSquare
    from PIL import Image, ImageDraw, ImageFont
    #imports
    
    #get image
    im = Image.open('assets/map.png')
    width, height = im.size
    #resize it
    im2 = Image.new(im.mode,(width+400, height+200),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    #big square draw
    draw.rectangle(((width/1.2+50, height/1.2+50),(width/1.2+500, height/1.2+250)),fill="#101020")
    with Image.open('assets/rift100.png') as crital:
        im.paste(crital,(int(width/1.2+100), int(height/1.2+100)),crital)
    
    #image for crystals
    for star in existingStars:
        inTheList=False
        for tuple in marketTypeList:
            if star in tuple:
                for piece in tuple:
                    if piece in ['techMarket','industrialMarket']:
                        inTheList=True
                        break
        if inTheList==False:
            continue
       
        if inTheList==True:
           drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,(163,78,192),10,im)
           #weird def
    
    #little font
    font = ImageFont.load_default(70)
    draw.text((width/1.2+250, height/1.2+115),'50 CR', font=font ,  fill='yellow')
    return(im)




#returns market type map
def marketsTypeMap():
    #get image
    im = Image.open('assets/map.png')
    width, height = im.size
    #resize it
    im2 = Image.new(im.mode,(width+600, height+300),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    #big square draw
    draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+1200)),fill="#101020")
    
    #image for types
    for star in existingStars:
        inTheList=False
        for tuple in marketTypeList:
            if star in tuple:
                    color=marketColor[tuple[1]]
                    actualTuple=tuple
                    inTheList=True
                    break
                
        if inTheList==False:
           drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,'gray',10,im)
       
        if inTheList==True:
           drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,marketColor[actualTuple[1]],10,im)
       
           if len(actualTuple) > 2:
               drawCenteredHalfSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,marketColor[actualTuple[2]],10,im)
           
           if len(actualTuple) > 3:
           
               #weird def
               #set
               cords=(starsNC[star][0]+200,starsNC[star][1]+100)
               size=150
               color=marketColor[actualTuple[3]]
               widt= 10
               #execute
               draw.line(((cords[0]-size/3+widt/2,cords[1]-size/2+widt/2-1),(cords[0]+size/3,cords[1]-size/2+widt/2-1)),fill=color,width=widt)
               draw.line(((cords[0]-size/3+widt/2,cords[1]+size/2-widt/2),(cords[0]+size/3,cords[1]+size/2-widt/2)),fill=color,width=widt)
               #weird def

    #draw labels
    font = ImageFont.load_default(60)
    x=width/1.2+100
    y=height/2+100
    for market in marketColor:
        draw.rectangle(((x-30,y),(x+30,y+60)),fill=marketColor[market])
        draw.text((x+50, y), str(market[:-6].capitalize()+' Market'), font=font ,  fill=marketColor[market])
        y+=100
    return(im)
    



#this generates maps for specified items
def marketGetItem(string):
    #format the data
    string=string[13:].title()
    while string[len(string)-1] == " ":
        string=string[:-1]
    
    #just little check if its minerals
    if string == "Minerals":
        string="Rock"
        mineralsCheck=True
    else:
        mineralsCheck=False
    
    if string == "Rift Crystal":
        return crystalsLocationMap()
    #get market types that has the item
    Have={"buy":[],"sell":[]}
    for market in allMarkets:
        for insidekey in allMarkets[market]:
            for tuple in allMarkets[market] [insidekey]:
                if string == tuple[0]:
                    Have[insidekey] += [market]
    
    #lets check if item in fact exists
    if mineralsCheck == False and len(Have["buy"]) == 0 and len(Have["sell"]) == 0:
        return None
        
    #now lets compare and get stars
    Stars={"buy":[],"sell":[]}
    for key in Stars:
        for tuple in marketTypeList:
            for mklist in list(tuple)[1:]:
                if mklist in Have[key]:
                    Stars[key]+=[tuple[0]]
                    break
    
    #get image
    im = Image.open('assets/map.png')
    width, height = im.size
    #resize it
    im2 = Image.new(im.mode,(width+600, height+300),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    #big square draw
    draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+650)),fill="#101020")
    if mineralsCheck== True:
        draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+1250)),fill="#101020")
    
    #lets draw the buy squares.
    for star in Stars['buy']:
        drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,'green',10,im)
    #lets draw the sell squares.
    for star in Stars['sell']:
        if star in Stars['buy']:
            drawCenteredHalfSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,'red',10,im)
        else:
            drawCenteredSquare(( starsNC[star][0]+200,starsNC[star][1]+100),150,'red',10,im)
    
    #draw labels
    font = ImageFont.load_default(70)
    x=width/1.2+100
    y=height/2+100
    
    #buy one
    draw.rectangle(((x-20,y),(x+30,y+50)),fill="green")
    draw.text((x+50, y), str("Here you can buy"), font=font ,  fill="green")
    y+=100
    
    #sell one
    draw.rectangle(((x-20,y),(x+30,y+50)),fill="red")
    draw.text((x+50, y), str("Here you can sell"), font=font ,  fill="red")
    y+=100
    
    if mineralsCheck==False:
        #lets get its price
        price={'buy':0,'sell':0}
        for market in allMarkets:
            for key in allMarkets[market]:
                for tuple in allMarkets[market][key]:
                    if string in tuple:
                        price[key]=tuple[1]
                        break
    
        #item name/price
        draw.text((x-30, y+50),str(string), font=font ,  fill="white")
        draw.text((x-30, y+150),"Buy price: {} Sell price: {}".format(price['buy'],price['sell']), font=font ,  fill="white")
        return(im)
        
    if mineralsCheck==True:
      for mineral in ["Rock","Iron Ore","Gold Ore","Titanium Ore"]:
        string=mineral
        #lets get its price
        price={'buy':0,'sell':0}
        for market in allMarkets:
            for key in allMarkets[market]:
                for tuple in allMarkets[market][key]:
                    if string in tuple:
                        price[key]=tuple[1]
                        break
    
    
        #item name/price
        draw.text((x-30, y+50),str(string), font=font ,  fill="white")
        draw.text((x-30, y+150),"Buy price: {} Sell price: {}".format(price['buy'],price['sell']), font=font ,  fill="white")
        y+=200
    return(im)






#returns market items list
def getMarketTable(market):
    if market in ['refinery','agriculture','military','tech','tourism','industrial']:
        market+='Market'
    string="```\nYou can buy:\n"
    for tuple in allMarkets[market]['buy']:
        string += '  {} for {} CR\n'.format(tuple[0],tuple[1])
    string+="\nYou can sell:\n"
    for tuple in allMarkets[market]['sell']:
        string += '  {} for {} CR\n'.format(tuple[0],tuple[1])
    string+="```"
    return string
    




#set channel for auto updates
def setUpdateChannel(ctx):
    listChanFile="database/autoUpdatesChannels.txt"
    #first phase: check existence
    with open(listChanFile) as fil:
        file = fil.read()
        if str(ctx.guild.id) in file:
            exists=True
        else:
            exists=False
    #second phase: append
    if exists==False:
        with open(listChanFile,"a") as file:
            file.write(str(ctx.guild.id)+"::"+str(ctx.message.channel.id)+";;\n")
        return "Added server and Channel to auto update list!"
    #second phase: edit channel
    if exists==True:
        with open(listChanFile) as fil:
            file = fil.read()
            cursor=file.find("::",file.find(str(ctx.guild.id)))
            end=file.find(";;",cursor)
            newfile=file[:cursor+2]+str(ctx.message.channel.id)+file[end:]
        with open(listChanFile,"w") as fil:
            fil.write(newfile)
        return "Updated server's Channel on auto update list!"
            
            
#this one gets the channel where it will be posted on
def getUpdatesChannel(ctx):
    listChanFile="database/autoUpdatesChannels.txt"
    #first phase: check existence
    with open(listChanFile) as fil:
        file = fil.read()
        if str(ctx.guild.id) in file:
            cursor=file.find("::",file.find(str(ctx.guild.id)))
            end=file.find(";;",cursor)
            return file[cursor+2:end]
        else:
            return None
           
#gets all channels for updates
def getUpdatesChannels():
    listChanFile="database/autoUpdatesChannels.txt"
    output=[]
    with open(listChanFile,"r") as fil:
        for line in fil:
            cursor=line.find("::")
            end=line.find(";;",cursor)
            output += [int(line[cursor+2:end])]
    return output



#set channel for siege pings
def setSiegePingChannel(ctx,channel_id):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if yes, append guild and channel
    if str(ctx.guild.id) not in file:
        with open(Listfile,"a") as fil:
            fil.write(str(ctx.guild.id)+"::"+channel_id+";;"+";:;::;:;\n")
    #if no, overwrite old channel id
    else:
        cursor=file.find("::",file.find(str(ctx.guild.id)))
        end=file.find(";;",cursor)
        newfile=file[:cursor+2]+str(channel_id)+file[end:]
        with open(Listfile,"w") as file:
            file.write(newfile)
        return "Suc"

#get channel for siege pings
def getSiegePingChannel(ctx):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    #if yes, add faction.
    else:
        cursor=file.find("::",file.find(str(ctx.guild.id)))
        end=file.find(";;",cursor)
        return file[cursor+2:end]




#add faction name for siege pings
def addSiegePingFaction(ctx,faction):
    faction=faction.lower()
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    #if yes, add faction.
    else:
        #sets position
        cursor=file.find(";;",file.find(str(ctx.guild.id)))
        end=file.find(";:;:",cursor)
        #gets list of factions
        factions=file[cursor+2:end].split(',')
        #cleans list if empty
        if factions==[""]: factions=[]
        #add item to the list if not there already
        if faction not in factions:
            factions+=[faction]
        else: return "Err:2"
        #gets the list into a str
        out=""
        for i in range(len(factions)):
            out+=factions[i]
            if i != len(factions)-1:
                out+=","
        #finally writes it back
        newfile=file[:cursor+2]+out+file[end:]
        with open(Listfile,"w") as file:
            file.write(newfile)
        return "Suc"

#del faction name for siege pings
def delSiegePingFaction(ctx,faction):
    faction=faction.lower()
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    else:
        #sets position
        cursor=file.find(";;",file.find(str(ctx.guild.id)))
        end=file.find(";:;:",cursor)
        #gets list of factions
        factions=file[cursor+2:end].split(',')
        #cleans list if empty
        if factions==[""]: factions=[]
        #del item from the list if there
        if faction in factions:
            factions.pop(factions.index(faction))
        else: return "Err:3"
        #gets the list into a str
        out=""
        for i in range(len(factions)):
            out+=factions[i]
            if i != len(factions)-1:
                out+=","
        #finally writes it back
        newfile=file[:cursor+2]+out+file[end:]
        with open(Listfile,"w") as file:
            file.write(newfile)
        return "Suc"

#get faction names for siege pings
def getSiegePingFactions(ctx):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    else:
        #sets position
        cursor=file.find(";;",file.find(str(ctx.guild.id)))
        end=file.find(";:;:",cursor)
        #gets list of factions
        factions=file[cursor+2:end].split(',')
        #cleans list if empty
        if factions==[""]: factions=[]
        return factions




#add id for siege pings
def addSiegePingId(ctx,id):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    #if yes, add faction.
    else:
        #sets position
        cursor=file.find(";:;:",file.find(str(ctx.guild.id)))
        end=file.find(":;:;",cursor)
        #gets list of ids
        ids=file[cursor+4:end].split(',')
        #cleans list if empty
        if ids==[""]: ids=[]
        #add item to the list if not there already
        if id not in ids:
            ids+=[id]
        else: return "Err:4"
        #gets the list into a str
        out=""
        for i in range(len(ids)):
            out+=ids[i]
            if i != len(ids)-1:
                out+=","
        #finally writes it back
        newfile=file[:cursor+4]+out+file[end:]
        with open(Listfile,"w") as file:
            file.write(newfile)
        return "Suc"

#del id for siege pings
def delSiegePingId(ctx,id):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    else:
        #sets position
        cursor=file.find(";:;:",file.find(str(ctx.guild.id)))
        end=file.find(":;:;",cursor)
        #gets list of ids
        ids=file[cursor+4:end].split(',')
        #cleans list if empty
        if ids==[""]: ids=[]
        #del item from the list if there
        if id in ids:
            ids.pop(ids.index(id))
        else: return "Err:3"
        #gets the list into a str
        out=""
        for i in range(len(ids)):
            out+=ids[i]
            if i != len(ids)-1:
                out+=","
        #finally writes it back
        newfile=file[:cursor+4]+out+file[end:]
        with open(Listfile,"w") as file:
            file.write(newfile)
        return "Suc"

#get ids for siege pings
def getSiegePingIds(ctx):
    Listfile="database/siegePingList.txt"
    #set file as read of target file
    with open(Listfile) as fil:
        file = fil.read()
    #checks if guild_id exists in the file
    #if no, return err1. Guild not existent
    if str(ctx.guild.id) not in file:
        return "Err:1"
    else:
        #sets position
        cursor=file.find(";:;:",file.find(str(ctx.guild.id)))
        end=file.find(":;:;",cursor)
        #gets list of factions
        ids=file[cursor+4:end].split(',')
        #cleans list if empty
        if ids==[""]: ids=[]
        return ids


#checks for triggers then returns a list of channels and ids to ping.
def triggeredSiegePings(trigger):
    fileName="database/siegePingList.txt"
    outlist={}
    with open(fileName) as file:
        for line in file:
            if trigger in line:
                outlist[line[line.find("::")+2:line.find(";;")]]=[id for id in line[line.find(";:;:")+4:line.find(":;:;")].split(',')]
    return outlist

