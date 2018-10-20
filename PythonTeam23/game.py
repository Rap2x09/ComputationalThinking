from map import rooms
from player import *
from items import *
from gameparser import *
from suspects import *
#from notebook import *
#from weapons import *
import random

def main():

    #Intro
    print("""
            Game Title

            Intro.....

            """)

    player_name = input("Enter your name: ")

    age_verification(player_name)
    
    current_room = rooms["Lobby"]

    display_room(current_room)

    while True:

        command = menu(current_room["exits"], current_room["items"], inventory)

        execute_command(command)

        #Victory condition
        #if whatever:
        #    print("Congratulations")
        #    break
        #Game over
        #elif life == 0:
        #    print("Game over")
        #    break
        
def menu(exits, room_items, inv_items): # Not inv items

    print("\nType HELP for list of commands")
    print("What do you want to do?")
    
    user_command = input("...")

    input_normalised = normalise_input(user_command)

    return input_normalised

def display_help(exits, room_items, inv_items):#formerly print_menu

    print("\nYou can use commands:\n")
    
    for direction in exits:
        print_exit(direction, destination(exits, direction))

    for items in room_items:
        #print("TAKE " + items["id"].upper() +  " to add " + items["name"] + " in your inventory.")
        print("CHECK " + items["id"].upper() +  " to inspect item or TAKE " + items["id"].upper()  + " to add " + items["name"] + " to your inventory.")

    for item in inv_items:
        print("USE " + item["id"].upper() + " to use " + item["name"] + ".")


def print_exit(direction, leads_to):

    print("GO " + direction.upper() + " to " + leads_to + ".")

def move(exits, direction):

    return(rooms[exits[direction]])

def destination(exits, direction): #formerly exit_leads_to

    return rooms[exits[direction]]["name"]

def is_valid_exit(exits, chosen_destination):

    return chosen_destination in exits

def execute_command(command): #Use different commands

    global inventory

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "take":
        if len(command) > 1:
            execute_take(command[1])
        else:
            print("Take what?")

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            print("Drop what?")

    elif command[0] == "use":
        if len(command) > 1:
            execute_use(command[1])            
        else:
            print("Use what?")
            
    elif command[0] == "help":
        #if len(command) > 1:
        display_help(current_room["exits"], current_room["items"], inventory)

    elif command[0] == "status":
        if len(command) > 1:
            show_status(command[1])

    elif command[0] == "talk to":
        if len(command) > 1:
            execute_talk_to(command[1])

    else:
        print("This makes no sense.")

def execute_go(direction):

    global current_room

    exits = current_room["exits"]
    if is_valid_exit(exits, direction):
        current_room = move(exits, direction)
        display_room(current_room)
    else:
        print("You cannot go there.")

def generate_mystery():
    ### This function should randomly generate a dictionary (called "mystery")
    ###that uses the terms "suspect", "weapon" and "room"
    ###as keys and randomly picks a room, suspect and weapon from the respective
    ###dicitonaries and asigns them as values. Once it has done this, the
    ###function should then call the generate_clues function to finish off the
    ###setup.
    mystery = {
        "suspect": random.choice(list(suspects))
        #"weapon": random.choice(list(weapons)) #Awaiting dictionary
        #"room": random.choice(list(room)) #Awaiting dictionary
    }
    generate_clues(mystery)

def generate_clues(mystery):
    ###This function is responsible for generating the correct clues to solve the
    ###mystery given to it and then asigning each of them to a room.

    clues = {
        "room": """On closer inspection of the room, you notice a splatter of
                      blood on the wall and below it a puddle of yet more blood.
                      clearly this is the room in which the murder took place""",
        "witness": "" + suspects[mystery[suspect]]["build"] + "", ###A string about interviewing a witness of some kind who claims they saw a sillhouette of the murderer and that they were (tall/short)
        "clothes" : "" + suspects[mystery[suspect]]["sex"] + "", ###A string about finding a scrap of (male/female) clothing clearly belonging to the murderer
        "hair": "" + suspects[mystery[suspect]]["hair"] + "", ###A string about finding a lock of (black/blonde) hair clearly belonging to the murderer
        "weapon": "" + mystery["weapon"] + "" ###A string about finding the murder weapon using mystery["weapon"]    
        }

    rooms[mystery[room]][clue] = clues[room]

    for room in rooms:
        if room[name] != "lobby" and room[clue] == "":
            room[clue] = clues[random.choice(list(clues)[1:])]

def display_details(room):
    #This function combines the 3 red hearings and the clue from a room, randomly inserting the clue to hide it.
    #it then returns the text as one string to be printed after the rooms description. 
    pass

def execute_inspect(detail):
    #This will return the "Closer inspection" text asigned to each red hearing and each clue
    pass

def display_notebook():
    #Displays the notebook for the player to change the suspicion on any of the mystery elements or to look at any clues that they've previously discovered
    #The player should input which section they'd like to view, Suspects, Weapons, Rooms or clues
    pass

def notebook_suspects():
    # Displays the list of suspects sorted by their suspicion level
    for suspicion in ["highly suspicious", "neutral", "unlikely"]:
        printed = False
        print("-" + suspicion.upper() + "-")
        for suspect in suspects:
            if suspects[suspect]["notebook_status"] == suspicion:
                for key in suspects[suspect]:
                    if key != "notebook_status":
                        print("Suspect " + key + ": " + str(suspects[suspect][key]))
                        printed = True
                print()
        if printed == False:
            print()
            print("None")
            print()

def notebook_weapons():
    # Displays the list of weapons sorted by their suspicion level
    pass

def notebook_rooms():
    # Displays the list of rooms sorted by their suspicion level
    pass

def notebook_clues():
    # Displays the list of clues previously discovered by the player
    pass

def notebook_mark(subject):
    subject["notebook_status"] = "highly suspicious"

def notebook_reject(subject):
    subject["notebook_status"] = "unlikely"

def show_status():
    pass

def display_room(room):

    print("\n" + room["name"].upper() + "\n\n" + room["description"])

def print_inventory_items(items):

    if items == []:
        print("You inventory is empty")
    else:
        print("You have " + items_list(items) + ".\n")

def items_list(items):

    lists = []

    for item in items:
        lists.append(item.get("name"))

    return ", ".join(lists)

def execute_take(item_id):
    
    current_items = []

    for items in current_room["items"]:        
        current_items.append(items["id"])
        
    if item_id in current_items:
        if item_id == "biscuits":
            inventory.append(item_biscuits)
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(item_biscuits)
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(item_biscuits)
                
        elif item_id == "id":
            inventory.append(globals()["item_id"])
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(globals()["item_id"])
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(globals()["item_id"])
                
        elif item_id == "money":
            inventory.append(item_money)
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(item_money)
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(item_money)
                
        elif item_id == "laptop":
            inventory.append(item_laptop)
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(item_laptop)
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(item_laptop)
                
        elif item_id == "pen":
            inventory.append(item_pen)
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(item_pen)
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(item_pen)
                
        elif item_id == "handbook":
            inventory.append(item_handbook)
            weight_check = check_mass()
            if weight_check > 3:
                inventory.remove(item_handbook)
                print("Cannot take item. Inventory is too heavy.")
            else:
                current_room["items"].remove(item_handbook)
    else:
        print("You cannot take that")

def execute_drop(item_id):

    inventory_items = []

    for items in inventory:
        inventory_items.append(items["id"])
    
    if item_id in inventory_items:
        if item_id == "id":
            inventory.remove(globals()["item_id"])
            current_room["items"].append(globals()["item_id"])
            
        elif item_id == "laptop":
            inventory.remove(item_laptop)
            current_room["items"].append(item_laptop)
            
        elif item_id == "money":
            inventory.remove(item_money)
            current_room["items"].append(item_money)
            
        elif item_id == "biscuits":
            inventory.remove(item_biscuits)
            current_room["items"].append(item_biscuits)
            
        elif item_id == "pen":
            inventory.remove(item_pen)
            current_room["items"].append(item_pen)
            
        elif item_id == "handbook":
            inventory.remove(item_handbook)
            current_room["items"].append(item_handbook)
    else:
        print("You cannot drop that")    

if __name__ == "__main__":    
    main()

