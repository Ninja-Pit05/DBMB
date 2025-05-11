# technically, it was edited on 2.0, but since all i did was put it into a function, I'll let it slide. and im not touching it for now...
    
def gen_claimsMap():
    #1.6.2
    from urllib import request
    from PIL import Image, ImageDraw, ImageFont
    import random
    #imports
    from database import preliminaryData
    from functions import Functions
    #our imports
    
    #Request
    site1 = r"https://droneboi.io/api/Conquest/GetClaims"
    URLrequest = request.Request(site1 , data=None, headers = {'User-Agent': 'Mozilla/5.0'})
    
    #requests and stores an HTTP response object. Then into str object.
    WebObj=request.urlopen(URLrequest)
    info=str(WebObj.read())
    
    #pre made tests
    #info='[{"quadrant":"Delta","starSystem":"Astrin","sector":9,"stationName":"Caravan Palace","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufactung Machines"},{"quadrant":"Delta","starSystem":"Tams","sector":15,"stationName":"Sevastopol","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Macyzgavufacturing Machines"},{"quadrant":"Delta","starSystem":"Kaabel","sector":6,"stationName":"Lost Launchpads","ownerId":"e422fbc5-5e1d-46ea-9de5-e9bf825aa0dc","ownerName":"The Eklipse"},{"quadrant":"Delta","starSystem":"Kaabel","sector":5,"stationName":"Utrecht Centraal","ownerId":"16e4244f-cea7-4dd3-a012-4429eebd90b1","ownerName":"Federal Diety of Refuge "},{"quadrant":"Delta","starSystem":"Mekan","sector":20,"stationName":"Bean Terminal","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"},{"quadrant":"Delta","starSystem":"Zubenelgenubi","sector":4,"stationName":"Zubeneschamali","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"},{"quadrant":"Delta","starSystem":"Nowhere","sector":3,"stationName":"Some Station","ownerId":"e207ed47-9a86-4a91-a732-9e86feacab64","ownerName":"Rocks.CO"},{"quadrant":"Delta","starSystem":"Miata","sector":2,"stationName":"Frontier City","ownerId":"20c2885c-4697-4ddd-8ce0-a00f9a0eb050","ownerName":"DroneBoi United"},{"quadrant":"Delta","starSystem":"Nebulon","sector":23,"stationName":"Jazmin Terminal","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Zephyros","sector":30,"stationName":"Solaris Hub","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Nebulon","sector":23,"stationName":"Tokeletesseg Outpost","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Aurona","sector":24,"stationName":"Aether Fortuna","ownerId":"668fe639-df6d-4e02-a204-ff6fa620e83b","ownerName":"Scrapyards Swift Coalition "},{"quadrant":"Delta","starSystem":"Nimbral","sector":26,"stationName":"Galaxys Edge","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Aurona","sector":24,"stationName":"Fortuna Forgery","ownerId":"668fe639-df6d-4e02-a204-ff6fa620e83b","ownerName":"Scrapyars Swift Coalition "},{"quadrant":"Delta","starSystem":"Nebulon","sector":28,"stationName":"Yggdrasil Colony","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Fuuog Clan"},{"quadrant":"Delta","starSystem":"Nebulon","sector":28,"stationName":"Yggdrasil Colony","ownerId":"26948158-8296-440e-a885-94f240c275d8","ownerName":"Frog Clan"},{"quadrant":"Delta","starSystem":"Quasar","sector":27,"stationName":"Ninja Station","ownerId":"30226832-4839-4d39-b7a9-24ffcd0bbd79","ownerName":"SOLAR EVIL"},{"quadrant":"Delta","starSystem":"Snicker","sector":7,"stationName":"Bobr Arc","ownerId":"b0fc2495-54ed-4386-a21f-2d480c3ed08d","ownerName":"Massive Manufacturing Machines"}]'
    '''
    with open('predata.py') as file:
        exec(file.read())
        
    with open('Functions.py') as file:
        exec(file.read())'''
    #for tests
    
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
    
    #Organize what i want into a Dic
    infoDic={}
    #for index in total of blocks
    for i in range(blocks):
        infoDic[i]={}
        #for each piece after splitting commas
        for piece in list(rawList[i].split(',')):
            
            #get some characters out of piece
            output=""
            for a in range(len(piece)):
                if piece[a] not in ["{","}",'"']:
                    output+=piece[a]
            piece=output
            del output
            
            #stores into the dictionary
            key = list(piece.split(":"))[0]
            content = list(piece.split(":"))[1]
            infoDic[i][key]=content
    
    
    #defines some stelar system needed info
    claimableStars=[]
    for key in infoDic:
        claimableStars += [infoDic[key]['starSystem']]
    
    #existingStars
    
    #Create a dic with a color for each faction
    paLLet=preliminaryData.pallet
    colorDic={}
    with open("database/custom_faction_colors.txt") as fil:
        file=fil.read()
        for key in infoDic:
            owner=infoDic[key]['ownerName']
            foundin = file.find("faction:"+owner)
            if owner not in file:
                if len(paLLet)>0:
                    SelectedColor=paLLet[random.randint(0,len(paLLet)-1)]
                    paLLet.pop(paLLet.index(SelectedColor))
                    colorDic[owner]=SelectedColor
                    del SelectedColor
                else: colorDic[owner] = colorDic[owner] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            else:
                if file[foundin+len(owner)+17:file.find("\n",foundin)] == "N/A":
                    if len(paLLet)>0:
                        SelectedColor=paLLet[random.randint(0,len(paLLet)-1)]
                        paLLet.pop(paLLet.index(SelectedColor))
                        colorDic[owner]=SelectedColor
                        del SelectedColor
                    else: colorDic[owner] = colorDic[owner] = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                else:
                    colorDic[owner] = file[foundin+len(owner)+17:file.find("\n",foundin)]
    del paLLet
    
     
    #####     END OF INFORMATION HANDLING     #######
    
    
    
    
    
    
    
    ### START POINT OF DRAWING HANDLING     #####
    
    #get base image, w and h and set im1 draw
    im = Image.open('assets/map.png')
    width, height = im.size
    draw = ImageDraw.Draw(im)
    
    #do draw grid?
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
        
    
    #create new canvas to bigger borders.
    im2 = Image.new(im.mode,(width+400, height+600),color="#000000")
    im2.paste(im,(200,100))
    
    #redefines some objects and trash
    im=im2
    draw = ImageDraw.Draw(im)
    del im2
    
    
    #cordStarList
    
    
    #Do coordinates draw test?
    CordTest=False
    if CordTest:
        for star in cordStarList:
            Functions.drawCenteredSquare((star[0]+200,star[1]),3,"blue",3)
            
    #do i really need this one? It facilitates later tho. Fuses star name with owners in that stars system.
    starsSO={}
    for key in infoDic:
        try:
            starsSO[infoDic[key]['starSystem']] += [infoDic[key]['ownerName']]
        except:
            starsSO[infoDic[key]['starSystem']] = [infoDic[key]['ownerName']]
    
    
    #!problem
    starsNC=preliminaryData.starsNC
    
    
    #time to draw labels
    #this one is the big square.
    draw.rectangle(((200, height+200),(200+width, height+570)),fill="#101020")
    
    #now the texts
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
            
    #Draw the rectangles
    for star in starsNC:
        if star not in claimableStars:
           Functions.drawCenteredSquare((starsNC[star][0]+200,starsNC[star][1]+100),150,"gray",5,im)
           
        else:
            Functions.draw_claims(star,150,10,im,starsSO,colorDic)
    
    
    
    im.save("outputs/claimsMap.png")
    im.save("test.png")
    
    #"debug" variables?
    #starsSO, starsNC