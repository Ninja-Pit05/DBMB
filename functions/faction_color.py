def get_faction(owner):
    with open("database/Allowed_Faction_Owners.txt") as file:
        for line in file:
            if str(owner) in line[line.find("name:")+5:line.find("'$'")].split(","):
                return line[line.find("faction:")+8:]
                break
        return "None"
            
def check_0f(txt):
    for letter in txt[1:]:
        if letter not in ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]:
            return False
            break
    return True
def edit_color(faction,color):
    faction=faction[:len(faction)-1]
    #line 11 usually crashes when len(faction)==1
    while faction[0]==" ":
        faction=faction[1:]
    while faction[len(faction)-1]==" ":
        faction=faction[:len(faction)-1]
    
    with open("database/custom_faction_colors.txt") as fil:
        file = fil.read()
        if file.find("faction:"+faction) != -1:
            if color[0] == "#" and len(color) <= 7 and check_0f(color):
                file=file[:file.find("color:",file.find("faction:"+faction))+6] +color+file[file.find("\n",file.find("faction:"+faction)):]
                with open("database/custom_faction_colors.txt","w+") as output:
                    output.write(file)
                return "Faction color changed successful!"
            else:
                print("Error! Invalid color code.")
                return "Error! Invalid color code."
        else: print("Error! Faction not found. (EC)")