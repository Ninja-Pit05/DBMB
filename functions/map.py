'''
Map related generation code.
//map //market type map and others.
'''


import aiohttp
import json
from PIL import Image, ImageDraw, ImageFont
import random

from assets import static




#Here some drawing functions to divide a square into multiple parts. Maybe not the best way but rn i don't care.
# 1 Claim/2 Spaces
def _drawCenteredSquare(cords,size,color,widt,image):
    draw = ImageDraw.Draw(image)
    draw.rectangle(((cords[0]-size/2,cords[1]-size/2),(cords[0]+size/2,cords[1]+size/2)), outline=color, width=widt)

#2 Claims/2 Spaces
def _drawCenteredHalfSquare(cords,size,color,widt,image,orient=0):
    draw = ImageDraw.Draw(image)
    if orient==0: orien=-1
    else: orien=1
    #one side
    draw.line(((cords[0]+(-size/2+widt/2)*orien-orien,cords[1]-size/2),(cords[0]+(-size/2+widt/2)*orien-orien,cords[1]+size/2)),fill=color,width=widt)
    #up and down.
    draw.line(((cords[0]+(-size/2+widt/2)*orien,cords[1]-size/2+widt/2),(cords[0]-widt*2*orien,cords[1]-size/2+widt/2)),fill=color,width=widt)
    draw.line(((cords[0]+(-size/2+widt/2)*orien,cords[1]+size/2-widt/2-orien),(cords[0]-widt*2*orien,cords[1]+size/2-widt/2-orien)),fill=color,width=widt)

#3 Claims/3 Spaces
def _drawCenteredThirdSquare(cords,size,color,widt,image,orient=0):
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

#4 Claimes/4 Spaces
def _drawCenteredQuadsSquare(cords,size,color,widt,image,orient=0):
    draw = ImageDraw.Draw(image)
    if orient in [1,3]:
        oriY=1
    else: oriY=-1
    if orient in [1,2]:
        oriX=1
    else: oriX=-1
    draw.line(((cords[0]+(-size/2+widt/2)*oriX-oriX,cords[1]+(-size/2)*oriY+oriY),(cords[0]+(-size/2+widt/2)*oriX-oriX,cords[1]+(-widt*2)*oriY)),fill=color,width=widt)
    draw.line(((cords[0]+(-size/2+widt/2)*oriX,cords[1]+(-size/2+widt/2)*oriY),(cords[0]+(-widt*2)*oriX,cords[1]+(-size/2+widt/2)*oriY)),fill=color,width=widt)

# Abstracts away drawing claims into PIL img objects
def _draw_claims(star,size,widt,image,starsSO,colorDic):#
    draw = ImageDraw.Draw(image)
    if len(starsSO[star]) == 1:
        _drawCenteredSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),size,colorDic[starsSO[star][0]],widt,image)
    if len(starsSO[star]) == 2:
        for owner in range(len(starsSO[star])):
           _drawCenteredHalfSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner)
    if len(starsSO[star]) == 3:
        for owner in range(len(starsSO[star])):
           _drawCenteredThirdSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner)
    if len(starsSO[star]) == 4:
        for owner in range(len(starsSO[star])):
           _drawCenteredQuadsSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),size,colorDic[starsSO[star][owner]],widt,image,owner+1)



async def gen_claimsMap():
    #Request
    async with aiohttp.ClientSession(headers={'User-Agent': 'Mozilla/5.0'}) as session:
        async with session.get(r"https://droneboi.io/api/Conquest/GetClaims") as response:
            info = json.loads(await response.text())
            del response
    
    #Ready to go test dict.
    #Uncomment and we can test img generation without doing requests to the server.
    #info='[{"quadrant":"Delta","starSystem":"Astrin","sector":9,"stationName":"Caravan Palace","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufactung Machines"},{"quadrant":"Delta","starSystem":"Tams","sector":15,"stationName":"Sevastopol","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Macyzgavufacturing Machines"},{"quadrant":"Delta","starSystem":"Kaabel","sector":6,"stationName":"Lost Launchpads","ownerId":"e422fbc5-5e1d-46ea-9de5-e9bf825aa0dc","ownerName":"The Eklipse"},{"quadrant":"Delta","starSystem":"Kaabel","sector":5,"stationName":"Utrecht Centraal","ownerId":"16e4244f-cea7-4dd3-a012-4429eebd90b1","ownerName":"Federal Diety of Refuge "},{"quadrant":"Delta","starSystem":"Mekan","sector":20,"stationName":"Bean Terminal","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"},{"quadrant":"Delta","starSystem":"Zubenelgenubi","sector":4,"stationName":"Zubeneschamali","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"},{"quadrant":"Delta","starSystem":"Nowhere","sector":3,"stationName":"Some Station","ownerId":"e207ed47-9a86-4a91-a732-9e86feacab64","ownerName":"Rocks.CO"},{"quadrant":"Delta","starSystem":"Miata","sector":2,"stationName":"Frontier City","ownerId":"20c2885c-4697-4ddd-8ce0-a00f9a0eb050","ownerName":"DroneBoi United"},{"quadrant":"Delta","starSystem":"Nebulon","sector":23,"stationName":"Jazmin Terminal","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Zephyros","sector":30,"stationName":"Solaris Hub","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Nebulon","sector":23,"stationName":"Tokeletesseg Outpost","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Aurona","sector":24,"stationName":"Aether Fortuna","ownerId":"668fe639-df6d-4e02-a204-ff6fa620e83b","ownerName":"Scrapyards Swift Coalition "},{"quadrant":"Delta","starSystem":"Nimbral","sector":26,"stationName":"Galaxys Edge","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Aurona","sector":24,"stationName":"Fortuna Forgery","ownerId":"668fe639-df6d-4e02-a204-ff6fa620e83b","ownerName":"Scrapyars Swift Coalition "},{"quadrant":"Delta","starSystem":"Nebulon","sector":28,"stationName":"Yggdrasil Colony","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Fuuog Clan"},{"quadrant":"Delta","starSystem":"Nebulon","sector":28,"stationName":"Yggdrasil Colony","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Quasar","sector":27,"stationName":"Ninja Station","ownerId":"30226832-4839-4d39-b7a9-24ffcd0bbd79","ownerName":"SOLAR EVIL"},{"quadrant":"Delta","starSystem":"Snicker","sector":7,"stationName":"Bobr Arc","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"}]'
    '''
    with open('predata.py') as file:
        exec(file.read())
        
    with open('Functions.py') as file:
        exec(file.read())'''
    #for tests
    
    #defines some info needed later.
    claimableStars=[]
    for dic in info:
        claimableStars += [dic['starSystem']]
    
    
    #Create a dic with a color for each faction
    paLLet=static.pallet
    colorDic={}
    with open("database/custom_faction_colors.txt") as fil:
        file=json.loads(fil.read())
        for dic in info:
            owner=dic['ownerName']
            color = file.get(owner.lower())
            if color == None or color == 'N/A':
                #if the factiondoesn't have a color, we pick one from the paLLet.
                #if paLLet is empty, i gen a random one.
                if len(paLLet)>0:
                    SelectedColor=paLLet[random.randint(0,len(paLLet)-1)]
                    paLLet.pop(paLLet.index(SelectedColor))
                    colorDic[owner]=SelectedColor
                    del SelectedColor
                else: colorDic[owner] = colorDic[owner] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            else:
                colorDic[owner] = color
    del paLLet, color, owner
    ### END OF INFORMATION HANDLING ###
    
    ### DRAWING HANDLING ###
    im = Image.open('assets/map.png')
    width, height = im.size
    draw = ImageDraw.Draw(im)
    
    #do draw grid? (Used to help manually set coords)
    DrawGrid=False
    #Draws the grid.
    if DrawGrid:
        siz=10
        max=int(width/siz)
        for x in range(max):
            draw.rectangle(((x*siz,0),(x*siz+1,99999)), fill ="#555555")
        for x in range(max):
            draw.rectangle(((0,x*siz),(99999,x*siz+1)), fill ="#555555")
        #####
        siz=100
        max=int(width/siz)
        for x in range(max):
            draw.rectangle(((x*siz,0),(x*siz+1,99999)), fill ="#aaaaaa")
        for x in range(max):
            draw.rectangle(((0,x*siz),(99999,x*siz+1)), fill ="#aaaaaa")
        #####
        siz=500
        max=int(width/siz)
        for x in range(max):
            draw.rectangle(((x*siz,0),(x*siz+1,99999)), fill ="#aaffaa")
        for x in range(max):
            draw.rectangle(((0,x*siz),(99999,x*siz+1)), fill ="#aaffaa")
        ######
        del siz,max
    
    #increase canvas size with temp object 'im2'
    im2 = Image.new(im.mode,(width+400, height+600),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    draw = ImageDraw.Draw(im)
    del im2

    #Do coordinates draw test? (Used to manually set coords)
    CordTest=False
    if CordTest:
        for star in static.cordStarList:
            _drawCenteredSquare((star[0]+200,star[1]),3,"blue",3)
            
    #Fusion of stars Systems-Owner
    starsSO={}
    for dic in info:
        try:
            starsSO[dic['starSystem']] += [dic['ownerName']]
        except:
            starsSO[dic['starSystem']] = [dic['ownerName']]
    
    #Drawing labels
    #Backgroung
    draw.rectangle(((200, height+200),(200+width, height+570)),fill="#101020")
    #Color samples and text
    font = ImageFont.load_default(60)
    x=250
    y=height+200+40
    for owner in colorDic:
       if x+draw.textlength(str(owner),font=font)+120 > width+200:
           x=250
           y+=100
       draw.rectangle(((x-20,y+20),(x+20,y+60)),fill=colorDic[owner])
       draw.text((x+50, y), str(owner), font=font ,  fill=colorDic[owner])
       x += draw.textlength(str(owner), font=font)+120
            
    #Draw the claims rectangles.
    for star in static.starsNC:
        if star not in claimableStars:
           #We do not draw the gray square to non-claimable stars anymore. (Juicco Suggestion)
           #"whyyyy it still here" because i want to.
           #Functions._drawCenteredSquare((static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,"gray",5,im)
           pass
        else:
            _draw_claims(star,150,10,im,starsSO,colorDic)
    #finished.
    im.save("output/claimsMap.png")
    #"debug" variables?
    #starsSO, starsNC






### Market related code. ↓↓
#just to get the crystals location map
def crystals_map():
    from PIL import Image, ImageDraw, ImageFont
    from assets import static
    #imports
    #get base and resize it.
    im = Image.open('assets/map.png')
    width, height = im.size
    im2 = Image.new(im.mode,(width+400, height+200),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    # price background
    draw.rectangle(((width/1.2+50, height/1.2+50),(width/1.2+500, height/1.2+250)),fill="#101020")
    with Image.open('assets/rift100.png') as crital:
        im.paste(crital,(int(width/1.2+100), int(height/1.2+100)),crital)
    #Outline
    for star in static.existingStars:
        if 'techMarket' in static.marketTypeList.get(star,[]) or 'industrialMarket' in static.marketTypeList.get(star,[]):
           _drawCenteredSquare((static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,(163,78,192),10,im)
           #not a weird def anymore :D
    font = ImageFont.load_default(70)
    draw.text((width/1.2+250, height/1.2+115),'50 CR', font=font ,  fill='yellow')
    return(im)




#returns market type map
def markets_type_map():
    #get base, resize it, set drawing object
    im = Image.open('assets/map.png')
    width, height = im.size
    im2 = Image.new(im.mode,(width+600, height+300),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    #background
    draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+1200)),fill="#101020")
    #types outline
    for star in static.existingStars:
        marketTables = static.marketTypeList.get(star,[])
        
        if marketTables:
           _drawCenteredSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,static.marketColor[marketTables[0]],10,im)
       
           if len(marketTables) >= 2:
               _drawCenteredHalfSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,static.marketColor[marketTables[1]],10,im)
           
           if len(marketTables) >= 3:
               #(not so) weird def (but still)
               #set
               cords=(static.starsNC[star][0]+200,static.starsNC[star][1]+100)
               size=150
               color=static.marketColor[marketTables[2]]
               widt= 10
               #execute
               draw.line(((cords[0]-size/3+widt/2,cords[1]-size/2+widt/2-1),(cords[0]+size/3,cords[1]-size/2+widt/2-1)),fill=color,width=widt)
               draw.line(((cords[0]-size/3+widt/2,cords[1]+size/2-widt/2),(cords[0]+size/3,cords[1]+size/2-widt/2)),fill=color,width=widt)
               #weird def, but works
    #draw labels
    font = ImageFont.load_default(60)
    x=width/1.2+100
    y=height/2+100
    for market in static.marketColor:
        draw.rectangle(((x-30,y),(x+30,y+60)),fill=static.marketColor[market])
        draw.text((x+50, y), str(market[:-6].capitalize()+' Market'), font=font ,  fill=static.marketColor[market])
        y+=100
    return(im)
    

#returns maps with goods sell/buy location
def market_get_item(item: str):
    #format the data
    #!!!
    #remeber to code a list of items to select from on the command it self before passing it to this function
    #just little check if its minerals
    item=item.capitalize()
    if item == "Minerals":
        item="Rock"
        mineralsCheck=True
    else:
        mineralsCheck=False
    
    if item in ["Rift Crystal","Rift","Rift Crystals","Crystal","Crystals"]:
        return crystals_map()
    #get market types that has the item
    Deals={"buy":[],"sell":[]}
    for market in static.allMarkets:
        for transaction in static.allMarkets[market]:
            for tuple in static.allMarkets[market] [transaction]:
                if item == tuple[0]:
                    Deals[transaction] += [market]
    
    #quits if the item wasn't found in any market table.
    if not mineralsCheck and len(Deals["buy"]) == 0 and len(Deals["sell"]) == 0:
        return None
        
    #now lets compare and get stars
    Stars={"buy":[],"sell":[]}
    for key in Stars:
        for star in static.marketTypeList:
            for market in static.marketTypeList[star]:
                if market in Deals[key]:
                    Stars[key]+=[star]
                    break
    
    #get base and resize
    im = Image.open('assets/map.png')
    width, height = im.size
    im2 = Image.new(im.mode,(width+600, height+300),color="#000000")
    im2.paste(im,(200,100))
    im=im2
    del im2
    draw = ImageDraw.Draw(im)
    #background
    draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+650)),fill="#101020")
    if mineralsCheck:
        draw.rectangle(((width/1.2, height/2),(width/1.2+900, height/2+1250)),fill="#101020")
    #lets draw the buy squares.
    for star in Stars['buy']:
        _drawCenteredSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,'green',10,im)
    #lets draw the sell squares.
    for star in Stars['sell']:
        if star in Stars['buy']:
            _drawCenteredHalfSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,'red',10,im)
        else:
            _drawCenteredSquare(( static.starsNC[star][0]+200,static.starsNC[star][1]+100),150,'red',10,im)
    
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
    
    if not mineralsCheck:
        #lets get its price
        price={'buy':0,'sell':0}
        for market in static.allMarkets:
            for key in static.allMarkets[market]:
                for tuple in static.allMarkets[market][key]:
                    if item in tuple:
                        price[key]=tuple[1]
                        break
    
        #item name/price
        draw.text((x-30, y+50),str(item), font=font ,  fill="white")
        draw.text((x-30, y+150),"Buy price: {} Sell price: {}".format(price['buy'],price['sell']), font=font ,  fill="white")
        return(im)
        
    else:
      for mineral in ["Rock","Iron Ore","Gold Ore","Titanium Ore"]:
          item=mineral
          #lets get its price
          price={'buy':0,'sell':0}
          for market in static.allMarkets:
              for key in static.allMarkets[market]:
                  for tuple in static.allMarkets[market][key]:
                      if item in tuple:
                          price[key]=tuple[1]
                          break
          #item name/price
          draw.text((x-30, y+50),str(item), font=font ,  fill="white")
          draw.text((x-30, y+150),"Buy price: {} Sell price: {}".format(price['buy'],price['sell']), font=font ,  fill="white")
          y+=200
    return(im)



#returns market items list
def market_table(market):
    if market in ['refinery','agriculture','military','tech','tourism','industrial']:
        market+='Market'
    else:
        return
    string="```\nYou can buy:\n"
    for tuple in static.allMarkets[market]['buy']:
        string += '  {} for {} CR\n'.format(tuple[0],tuple[1])
    string+="\nYou can sell:\n"
    for tuple in static.allMarkets[market]['sell']:
        string += '  {} for {} CR\n'.format(tuple[0],tuple[1])
    string+="```"
    return string