"""
Holds Functions related to '//analysis' Command
"""
#!!! Didn't visit this yet!! Gotta revise everything later!!!

#debug dic
Dic={'taken': {'faction': {'w': {'Mining Space Republic': 3, 'HOTDOG WATER': 5, 'MASTERNTON faction': 3, 'Fury’s Edge Fighting Shark': 14, 'Slavia': 1, 'Guns For Hire': 1, 'where do i buy tomatoes?': 2, "No Sandwiches For Fury's ?": 6, 'The Eklipse': 3}, 'l': {}}, 'station': {'Solaris Hub': 4, 'Ninja Station': 2, 'Utrecht Centraal': 6, 'Frontier City': 1, 'Aether Fortuna': 4, "Bobr's Arc": 2}, 'location': {'Sector 30 (Zephyros)': 4, 'Sector 27 (Quasar)': 2, 'Sector 5 (Kaabel)': 6, 'Sector 2 (Miata)': 1, 'Sector 24 (Aurona)': 4, 'Sector 7 (Snicker)': 2}, 'star': {}}, 'defended': {'faction': {'w': {"SIXER'S": 1, 'Fury’s Edge Fighting Shark': 1, 'Slavia': 4, 'Star Kingdom': 1, 'Massive Manufacturing Machines': 2, 'Xenon': 2, 'Frog Clan': 1, 'Mining Space Republic': 1, 'where do i buy tomatoes?': 2, 'Guns For Hire': 1, 'Polynesia miners space attack': 1, 'Atlas INC': 2, 'The Fryighter Industries': 1}, 'l': {}}, 'station': {'Aether Fortuna': 1, 'Frontier City': 4, 'Caravan Palace': 2, "Galaxy's Edge": 1, 'Lost Launchpads': 1, "Bobr's Arc": 1}, 'location': {'Sector 24 (Aurona)': 1, 'Sector 2 (Miata)': 4, 'Sector 9 (Astrin)': 2, 'Sector 26 (Nimbral)': 1, 'Sector 6 (Kaabel)': 1, 'Sector 7 (Snicker)': 1}, 'star': {}}}

    #now let's sort it
def sortIt(dicLocation):
        pairsList=sorted(dicLocation.items())
        outputPairs=[]
        while len(pairsList) > 0:
            key=""
            value=0
            for item in pairsList:
                if item[1] > value:
                    key , value = item
            pairsList.pop(pairsList.index((key,value)))
            outputPairs+=[(key,value)]
        dicLocation={}
        for pair in outputPairs:
            dicLocation[pair[0]]=pair[1]
        return dicLocation
        
        
def analysisToDic(messages):
    #List index is simple. 0 for winner 1 for losers.
    dictionary={'taken':{'faction':{'w':{},'l':{}},'station':{},'location':{},'star':{}},'defended':{'faction':{'w':{},'l':{}},'station':{},'location':{},'star':{}}}
    for i in range(len(messages)):
        #branches successful and not successful.
        if messages[i].content in ["A siege was completed"]:
            #first add winning faction
            #if faction in dic, add
            if messages[i].embeds[0].fields[3].value in dictionary['taken']['faction']['w'].keys():
                dictionary["taken"]['faction']['w'][messages[i].embeds[0].fields[3].value] += 1
            #if not, then create.
            else:
                dictionary["taken"]['faction']['w'][messages[i].embeds[0].fields[3].value] = 1
            #second add loser faction
            #if faction in dic, add
            if messages[i].embeds[0].fields[2].value in dictionary['taken']['faction']['l'].keys():
                dictionary["taken"]['faction']['l'][messages[i].embeds[0].fields[2].value] += 1
            #if not, then create.
            else:
                dictionary["taken"]['faction']['l'][messages[i].embeds[0].fields[2].value] = 1
            #now adding station
            #if station in dic, add
            if messages[i].embeds[0].fields[0].value in dictionary['taken']['station'].keys():
                dictionary["taken"]['station'][messages[i].embeds[0].fields[0].value] += 1
            #if not, then create.
            else:
                dictionary["taken"]['station'][messages[i].embeds[0].fields[0].value] = 1
            #now adding location
            #if location in dic, add
            if messages[i].embeds[0].fields[1].value in dictionary['taken']['location'].keys():
                dictionary["taken"]['location'][messages[i].embeds[0].fields[1].value] += 1
            #if not, then create.
            else:
                dictionary["taken"]['location'][messages[i].embeds[0].fields[1].value] = 1
       #
       #now defended sieges
        if messages[i].content in ["A siege was defended"]:
            #first add winning faction
            #if faction in dic, add
            if messages[i].embeds[0].fields[2].value in dictionary['defended']['faction']['w'].keys():
                dictionary['defended']['faction']['w'][messages[i].embeds[0].fields[2].value] += 1
            #if not, then create.
            else:
                dictionary['defended']['faction']['w'][messages[i].embeds[0].fields[2].value] = 1
            #second add loser faction
            #if faction in dic, add
            if messages[i].embeds[0].fields[3].value in dictionary['defended']['faction']['l'].keys():
                dictionary['defended']['faction']['l'][messages[i].embeds[0].fields[3].value] += 1
            #if not, then create.
            else:
                dictionary['defended']['faction']['l'][messages[i].embeds[0].fields[3].value] = 1
            #now adding station
            #if station in dic, add
            if messages[i].embeds[0].fields[0].value in dictionary['defended']['station'].keys():
                dictionary['defended']['station'][messages[i].embeds[0].fields[0].value] += 1
            #if not, then create.
            else:
                dictionary['defended']['station'][messages[i].embeds[0].fields[0].value] = 1
            #now adding location
            #if location in dic, add
            if messages[i].embeds[0].fields[1].value in dictionary['defended']['location'].keys():
                dictionary['defended']['location'][messages[i].embeds[0].fields[1].value] += 1
            #if not, then create.
            else:
                dictionary['defended']['location'][messages[i].embeds[0].fields[1].value] = 1
        #i should add stars but not rn
    del messages
    
    #now let's sort it
    #apply sorting function
    dictionary['taken']['faction']['w'] = sortIt(dictionary['taken']['faction']['w'])
    dictionary['taken']['faction']['l'] = sortIt(dictionary['taken']['faction']['l'])
    dictionary['taken']['station'] = sortIt(dictionary['taken']['station'])
    dictionary['taken']['location'] = sortIt(dictionary['taken']['location'])
    
    dictionary['defended']['faction']['w'] = sortIt(dictionary['defended']['faction']['w'])
    dictionary['defended']['faction']['l'] = sortIt(dictionary['defended']['faction']['l'])
    dictionary['defended']['station'] = sortIt(dictionary['defended']['station'])
    dictionary['defended']['location'] = sortIt(dictionary['defended']['location'])
    
    return dictionary




#analysis part
def analysisBoard(dic,type='overview'):
    limit=5
    if type=='overview':
        #good siegers
        output = "## Sieged Successfuly\n"
        for pair in list(dic['taken']['faction']['w'].items()):
            if list(dic['taken']['faction']['w'].keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        #good defenders
        output += "## Defended Successfuly\n"
        for pair in list(dic['defended']['faction']['w'].items()):
            if list(dic['defended']['faction']['w'].keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        #bad siegers
        output += "## Faced Defeat On Siege\n"
        for pair in list(dic['defended']['faction']['l'].items()):
            if list(dic['defended']['faction']['l'].keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        #bad defenders
        output += "## Faced Defeat On Defense\n"
        for pair in list(dic['taken']['faction']['l'].items()):
            if list(dic['taken']['faction']['l'].keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        #most sieges location
        output += "## Most Sieged Sectors\n"
        #count it up
        locations={}
        for pair in list(dic['taken']['location'].items()):
            if pair[0] in list(locations.keys()):
                locations[pair[0]]+=pair[1]
            else:
                locations[pair[0]]=pair[1]
        for pair in list(dic['defended']['location'].items()):
            if pair[0] in locations:
                locations[pair[0]]+=pair[1]
            else:
                locations[pair[0]]=pair[1]
        #counted now sort it
        locations=sortIt(locations)
        for pair in list(locations.items()):
            if list(locations.keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        #most sieged station
        output += "## Most Sieged Stations\n"
        #count it up
        locations={}
        for pair in list(dic['taken']['station'].items()):
            if pair[0] in list(locations.keys()):
                locations[pair[0]]+=pair[1]
            else:
                locations[pair[0]]=pair[1]
        for pair in list(dic['defended']['station'].items()):
            if pair[0] in locations:
                locations[pair[0]]+=pair[1]
            else:
                locations[pair[0]]=pair[1]
        #counted now sort it
        locations=sortIt(locations)
        for pair in list(locations.items()):
            if list(locations.keys()).index(pair[0]) == limit: break
            output+="- {} - {}\n".format(pair[0],pair[1])
        return output
        




#heat map
def heatmap(messages,sensibility):
    #lets count it up
    count={}
    for i in range(len(messages)):
        if messages[i].content in ["A siege just started"]:
            #extract star name
            if len(messages[i].embeds) < 1:
                print("-- Error. No embed on msg ",i)
                continue
            starName = messages[i].embeds[0].fields[1].value[messages[i].embeds[0].fields[1].value.find("(")+1:messages[i].embeds[0].fields[1].value.find(")")]
            #now create or add if existent
            if starName in count.keys():
               count[starName] += 1
            #if not, then create.
            else:
                count[starName] = 1
    ###Finished to gather siege info###
    #return count

    
    ###Start actual heatmap production
    from PIL import Image, ImageDraw, ImageFont
    #imports
    from database import preliminaryData
    #our imports
    
    starsNC = preliminaryData.starsNC
    
    #get base image, w and h and set im1 draw
    im = Image.open('assets/map.png')
    width, height = im.size
    draw = ImageDraw.Draw(im)
    
    #do draw grid?
    DrawGrid=False
    #Draws the grid.
    if DrawGrid:
        #####
        siz=50
        max=int(width/siz+1)
        for x in range(max):
            draw.rectangle(((x*siz,0),(x*siz+1,99999)), fill ="#aaaaaa")
        for x in range(max):
            draw.rectangle(((0,x*siz),(99999,x*siz+1)), fill ="#aaaaaa")
        ####
        #####
        siz=600
        max=int(width/siz+1)
        for x in range(max):
            draw.rectangle(((x*siz,0),(x*siz+1,99999)), fill ="#aafaaa")
        for x in range(max):
            draw.rectangle(((0,x*siz),(99999,x*siz+1)), fill ="#aafaaa")
        ####
        del siz,max
        #21/19
    
    #grid size
    squareSize=70
    gridSize=int(width/squareSize)+1
    
    
    #here we only need coords to the grid. So fixing it rn...
    starsNCb={}
    for star in starsNC.keys():
        starsNCb[star]=(int(starsNC[star][0]/squareSize),int(starsNC[star][1]/squareSize))
    # quickly generate an matrix. Or a two dimensional object if you prefer.
    matrix={i:{a:0 for a in range(gridSize)} for i in range(gridSize)}
    
    #generates heat layer
    heat=Image.new(im.mode,(width, height),color=(0,0,0,0))
    drawH= ImageDraw.Draw(heat)
    
    #apply sensibility
    for key in count:
        count[key]=int(count[key]* sensibility)
    
    #applying heat on coordinates
    for pair in starsNCb.items():
        #checks if exists. And adds value
        if pair[0] in count:
            strength=count[pair[0]] +1
        else:continue
        step=0
        center = pair[1]
        #while for each step of force
        while strength>0:
            x=-step
            y=0
            dx=-1
            dy=-1
            back=0
            #each block for each step
            while back<3:
                    
                    #checks values to cycle
                    if abs(x)==step:
                        dx=-dx
                    if abs(y)>=step:
                        dy=-dy
                    if x==step:
                        back+=1
                    if x==-step:
                        back+=1
                    if step==0: back+=1
                    if back==3 and step!= 0: break
                    #add valie
                    try: matrix[center[0]+x][center[1]+y]+=strength
                    #increase coordinate.
                    except: pass
                    x+=dx
                    y+=dy
            #next step
            strength-=1
            step+=1
            #print(x,y,dx,dy,step, strength )
    #apply heat to image
    for x in matrix:
        for y in matrix[x]:
            #color changes
            if matrix[x][y] != 0:
                value = matrix[x][y]*1
                r=0
                b=100
                if value < 10:
                    b+=value*10
                if value >=10 and value <= 30:
                    b=200
                if value > 10 and value < 30:
                    r+= (value-10)*10
                    b=200
                if value >=30:
                    r=200
                    if value > 30 and value < 50:
                        b= 200-(value-30)*10
                    if value>=50:
                        b=0
                #draw each square heat value
                drawH.rectangle(((x*squareSize,y*squareSize),(x*squareSize+squareSize,y*squareSize+squareSize)), fill =(r,0,b,130))
            else:
                drawH.rectangle(((x*squareSize,y*squareSize),(x*squareSize+squareSize,y*squareSize+squareSize)), fill =(0,0,100,70))
    #apply heat layer
    im = Image.alpha_composite(im, heat)
    del heat
    #save it
    im.save("outputs/heatmap.png")
    return

