'''
Holds dada that is manual and static to the game version.
'''

#star names. Left to right
existingStars = ["Mekan","Aurona","Quasar","Tams","Boah","Astrin","Bunnta","Snicker","Miata","Zephyros","Zubenelgenubi","Kaabel","Azur","Nowhere","Nimbral","Magnetar","Eden","Nebulon"]

#star coords. Left to right. 
cordStarList=[(72,1070),(273,270),(274,1969),(522,820),(722,2068),(872,1468),(972,2369),(1072,971),(1471,1170),(1471,2669),(1522,1567),(1723,870),(1775,2169),(1974,1320),(1975,68),(2272,670),(2772,470),(3072,769)]

#fusion of stars Name and Coordinates
starsNC={}
for star in existingStars:
    starsNC[star] = cordStarList[existingStars.index(star)]

#market data set
marketTypeList={'Mekan':['industrialMarket'],'Aurona':['industrialMarket','techMarket'],'Quasar':['tourismMarket'],'Tams':['militaryMarket'],'Snicker':['agricultureMarket'],'Zephyros':['tourismMarket'],'Miata':['techMarket','industrialMarket'],'Zubenelgenubi':['refineryMarket'],'Kaabel':['refineryMarket'],'Nimbral':['militaryMarket'],'Nebulon':['techMarket','industrialMarket','refineryMarket']}

industrialMarket= {'buy':[("Cannon Ammo",2),("Rotary Cannon Ammo",2),("Electronics",16),("Fuel Injector",31),("Hydraulics",23),("Microchip",27),("Rift Crystal",50),('Blocks',"--")],'sell':[('Rock',6),('Iron Ore',20),('Gold Ore',35),('Titanium Ore',45),('Bread',1),('Canned Tuna',2),('Drinking Water',3),('Frog In A Jar',15),('Medical Supplies',27),('Nomster Energy',4)]}

tourismMarket= {'buy':[('Blocks',"--")],'sell':[('Rock',6),('Iron Ore',20),('Gold Ore',35),('Titanium Ore',45),('Bread',1),('Canned Tuna',2),('Drinking Water',3),('Frog In A Jar',15),('Medical Supplies',27),('Nomster Energy',4),('Electronics',8),('Fuel Injector',15),('Hydraulics',11),('Microchip',13)]}

techMarket= {'buy':[("Cannon Ammo",2),("Rotary Cannon Ammo",2),("Electronics",16),("Fuel Injector",31),("Hydraulics",23),("Microchip",27),("Rift Crystal",50),('Blocks',"--")],'sell':[('Rock',6),('Iron Ore',20),('Gold Ore',35),('Titanium Ore',45),('Bread',1),('Canned Tuna',2),('Drinking Water',3),('Frog In A Jar',15),('Medical Supplies',27),('Nomster Energy',4)]}

militaryMarket= {'buy':[('Blocks',"--")],'sell':[("Cannon Ammo",1),("Rotary Cannon Ammo",1)]}

agricultureMarket= {'buy':[('Bread',2),('Canned Tuna',4),('Drinking Water',6),('Frog In A Jar',31),('Medical Supples',55),('Nomster Energy',9),('Blocks',"--")],'sell':[('Biowate',1),('Electronics',8),('Fuel Injector',15),('Hydraulics',11),('Microchip',13)]}

refineryMarket= {'buy':[('Ice',8),('Sand',2),('Soil',2),('Blocks',"--")],'sell':[('Biowaste',1),('Rock',3),('Iron Ore',10),('Gold Ore',17),('Titanium Ore',22),('Ice',4),('Bread',1),('Canned Tuna',2),('Drinking Water',3),('Frog In A Jar',15),('Medical Supplies',27),('Nomster Energy',4)]}

allMarkets={'refineryMarket':refineryMarket,'agricultureMarket':agricultureMarket,'militaryMarket':militaryMarket,'techMarket':techMarket,'tourismMarket':tourismMarket,'industrialMarket':industrialMarket}
#market data set

#market type colors
marketColor={'refineryMarket':'#534290','agricultureMarket':'#629d25','militaryMarket':'#956a4a','techMarket':'#2776ea','tourismMarket':'#dc2c64','industrialMarket':'#ffa500'}

#set of colors to avoid repetition
#Not the best approach, but better than nothing.
pallValues=[255,152,50]
pallet=[]
for r in pallValues:
    for g in pallValues:
        for b in pallValues:
            pallet+=[(r,g,b)]
for color in pallet:
    if color[0]==color[1] and color[1]==color[2] and color[2]==color[0]:
        pallet.pop(pallet.index(color))
#We pop colors too near to another color a faction already holds.
pallet.pop(pallet.index((152,50,255)))