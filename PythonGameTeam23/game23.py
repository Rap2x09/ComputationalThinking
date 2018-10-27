from player import *
from gameparser import *
from suspects import *
from map import *
from weapons import *
from TitleASCII import *
import random
import winsound

def reset_all():

    global current_room
    
    for x in rooms:
        rooms[x]["notebook_status"]="neutral"
        rooms[x]["clue"]=""
    for x in weapons:
        weapons[x]["notebook_status"]="neutral"
    for x in suspects:
        suspects[x]["notebook_status"]="neutral"

    current_room = rooms["lobby"]
    
def new_game():
    reset_all()
    introduction()
    main()
    
def introduction():
    current_room = rooms["lobby"]
    winsound.PlaySound("lobby", winsound.SND_ASYNC | winsound.SND_LOOP )
    global player_name
    global attempts_remaining
    global difficulty
    title()
    while True:
        print("Enter your name:")
        player_name = input("...")

        if 0 == len(player_name.strip()):
            print("\nYou entered nothing.\n")

        elif len(player_name) <= 20:
            break
            
        else:
            print("Plese enter a shorter name\n")

    age_verification(player_name)
    
    difficulty_picked = False
    
    while difficulty_picked == False:

        difficulty = normalise_input(input("Use number key or difficulty name.\n..."))
        
        if difficulty == ["hard"] or difficulty == ["3"]:
            attempts_remaining = 1
            difficulty_picked = True
            
        elif difficulty == ["medium"] or difficulty == ["2"]:
            attempts_remaining = 3
            difficulty_picked = True
            
        elif difficulty == ["easy"] or difficulty == ["1"]:
            attempts_remaining = 5
            difficulty_picked = True
        else:
            print("please enter a valid input\n")

    cls()
    intro()

    global correct_accusation
    correct_accusation = False
    global found_clues
    found_clues = []
    generate_mystery()
    
    

 
def intro():

    #Intro
    scroll_text("\n\nRing Ring,", 0.04)
    time.sleep(0.4)
    scroll_text("\nRing Ring,", 0.04)
    time.sleep(0.4)
    scroll_text("\n" + """A rusty voice at the other end of the line grunts,
'Hello? Is this Inspector """ + player_name.title() +  "?'.\n", 0.03)
    time.sleep(0.5)
    scroll_text("""You answer, huskily, 'It certainly is'.\n""", 0.03)
    time.sleep(0.5)                
    scroll_text("'Professor Parker has been murdered in Morebrandt mansion and we need your help!'",0.03)
    time.sleep(0.7)
    scroll_text("\n'We have all 6 suspects gathered in the lobby, and all the rooms are available for inspection'.",0.03)
    time.sleep(0.9)
    scroll_text("\n'We are counting on you to bring the killer to justice'.\n", 0.03)
    time.sleep(0.4)
    scroll_text("\n" + "15 minutes later you arrive at the mansion.\n", 0.03)
    time.sleep(1)
    cls()

def main():
    display_room(current_room)
    
    while True:

        command = ask_for_command()

        execute_command(command)

def generate_mystery():
    ### This function should randomly generate a dictionary (called "mystery")
    ###that uses the terms "suspect", "weapon" and "room"
    ###as keys and randomly picks a room, suspect and weapon from the respective
    ###dicitonaries and asigns them as values. Once it has done this, the
    ###function should then call the generate_clues function to finish off the
    ###setup.
    global mystery
    mystery = {
        "suspect": random.choice(list(suspects)),
        "weapon" : random.choice(list(weapons)), 
        "room": random.choice(list(rooms)[1:])
    }
    init_clues(mystery)
    generate_clues(mystery)

def generate_clues(mystery):
    ###This function is responsible for generating the correct clues to solve the
    ###mystery given to it and then asigning each of them to a room.

    rooms[mystery["room"]]["clue"] = clues["room"]

    random_clue_list = list(clues)
    random_room_list = list(rooms)
    random_clue_list.remove("room")
    random_room_list.remove("lobby")
    random_room_list.remove(mystery["room"])
    
    random.shuffle(random_clue_list)
    random.shuffle(random_room_list)

    for n in range(0,4):
        rooms[random_room_list[n]]["clue"] = clues[random_clue_list[n]]

def ask_for_command():

    print("What do you want to do?  (Type HELP for list of commands)")
    user_command = input("...")

    input_normalised = normalise_input(user_command)

    return input_normalised

def display_help(exits):

    print("\nYou can use commands:\n")
    
    for direction in exits:
        print_exit(direction, destination(exits, direction))

    print("CHECK + <object> for closer inspection.")
    print("ACCUSE to make accusation.")
    print("OPEN NOTEBOOK to open notebook\n")
    
def print_exit(direction, leads_to):

    print("GO " + direction.upper() + " to " + leads_to + ".")

def move(exits, direction):

    return(rooms[exits[direction]])

def destination(exits, direction):

    return rooms[exits[direction]]["name"]

def is_valid_exit(exits, chosen_destination):

    return chosen_destination in exits

def execute_command(command):

    if 0 == len(command):
        return

    if command[0] == "go":
        if len(command) > 1:
            cls()
            execute_go(command[1])
        else:
            print("Go where?")

    elif command[0] == "check":
        if len(command) > 1:
            execute_inspect(command[1])
        else:
            print("inspect what?")

    elif command[0] == "help":
        display_help(current_room["exits"])

    elif command == ["open", "notebook"]:
        display_notebook()

    elif command == ["accuse"]:
        make_accusation()
        

    else:
        print("This makes no sense.")

def make_accusation():
    print (mystery)
    comparison_mystery = {}
    global attempts_remaining
    for element in mystery:
    	comparison_mystery.update({element: normalise_input(mystery[element])})

    accusation = {
    "suspect": "",
    "weapon": "",
    "room": ""
    }
    cls()
    while True:
        a=input("""\nTo make an accusation you need to find out:

    • The suspected killer
    • The supected murder weapon
    • The room of the murder

There will be consequences if you get the case incorrect.

Are you sure you want to make an accusation? (Yes/No)
...""")
        if normalise_input(a)==["yes"] or normalise_input(a)==["y"] or normalise_input(a)==["yeah"]:

            while True:
                
                print("\nThe suspects you have highlighted as highly suspicious are:\n")
                x=[]
                for suspect in suspects:
                    if suspects[suspect]["notebook_status"] == "highly suspicious":
                        print("\t• " + suspects[suspect]["name"])
                    else:
                        if suspects[suspect]["notebook_status"] != "highly suspicious":   
                            x.append(suspect)
                            if len(x)==8:
                                print ("\tNONE")
                print("\nWho are you going to accuse? (type 'Help' for help)")
                suspect_accused = normalise_input(input("..."))

                if "".join(normalise_input(suspect_accused)) in list(suspects):
                    accusation["suspect"] = suspect_accused

                    while True:
                        
                        print("\nThe weapons you have highlighted as highly suspicious are:\n")
                        y=[]
                        for weapon in weapons:
                            if weapons[weapon]["notebook_status"] == "highly suspicious":
                                print("\t• " + weapons[weapon]["name"])
                            else:
                                if weapons[weapon]["notebook_status"] != "highly suspicious":   
                                    y.append(weapon)
                                    if len(y)==6:
                                        print ("\tNONE")
                        print("\nWhat weapon do you think they used? (type 'Help' for help)")
                        weapon_accused = normalise_input(input("...")) 

                        if "".join(normalise_input(weapon_accused)) in list(weapons):
                                accusation["weapon"] = weapon_accused

                                while True:
                                    
                                    print("\nThe rooms you have highlighted as highly suspicious are:\n")
                                    z=[]
                                    
                                    for room in rooms:
                                        if rooms[room]["notebook_status"] == "highly suspicious":
                                            print("\t• " + rooms[room]["name"])
                                        else:
                                            if weapons[weapon]["notebook_status"] != "highly suspicious":   
                                                z.append(room)
                                                if len(z)==6:
                                                    print ("\tNONE")
                                    print("\nWhich room do you think the murder took place in? (type 'Help' for help)")
                                    room_accused = normalise_input(input("...")) 
                                    if " ".join(room_accused) in list(rooms):
                                        accusation["room"] = room_accused
                                        if accusation == comparison_mystery:
                                            game_won()
                                        else:
                                            print("\nYour accusation doesn't make sense.\n")
                                            attempts_remaining-=1
                                            incorrect_accusations()
                                            if attempts_remaining==0:
                                                game_over()
                                                        
                                            else:
                                                main()


                                    elif room_accused == ["help"]:
                                        print("\nYou can choose from the following rooms:\n")
                                        for room in rooms:
                                            print("\t" + rooms[room]["name"])
                                    else:
                                        print("Please enter a valid room")


                        elif weapon_accused == ["help"]:
                            print("\nYou can choose from the following weapons:\n")
                            for weapon in weapons:
                                print("\t" + weapons[weapon]["name"])

                        else:
                            print("Please enter a valid weapon name")


                elif suspect_accused == ["help"]:
                    print("\nYou can choose from the following suspect:\n")
                    for suspect in suspects:
                        print("\t" + suspects[suspect]["name"])
                else:
                    print("Please enter a valid name")
        elif normalise_input(a)==["no"] or normalise_input(a)==["n"] or normalise_input(a)==["nah"]:
            main()
        else:
            print("Please answer Yes or No")
            
def incorrect_accusations():
    global difficulty
    if difficulty == ["easy"] or difficulty == ["1"]:
        if attempts_remaining==4:
            print("The case seems to be more complicated than you think, the residents of Morebrandt are giving you some space to try to piece the puzzle together.")
        elif attempts_remaining==3:
            print("The residents of Morebrandt are starting to look a bit more worried, but even the best detectives make mistakes. Right?")
        elif attempts_remaining==2:
            print("People are getting more and more nervous as you can't seem to make sense of the clues you have.")
        elif attempts_remaining==1:
            print("What little hope that remained of the Morebrandt residents has completely vanished, everyone is panicking. You feel as though you have 1 more attempt at finding the killer.")  
    elif difficulty == ["medium"] or difficulty == ["2"]:
        if attempts_remaining==2:
            print("The residents of Morebrandt are starting to look a bit more worried, but even the best detectives make mistakes. Right?")
        elif attempts_remaining==1:
            print("What little hope that remained of the Morebrandt residents has completely vanished, everyone is panicking. You feel as though you have 1 more attempt at finding the killer.")  
        
def execute_go(direction):

    global current_room

    exits = current_room["exits"]
    if is_valid_exit(exits, direction):
        current_room = move(exits, direction)
        display_room(current_room)
        winsound.PlaySound(current_room["room_sound"], winsound.SND_ASYNC | winsound.SND_LOOP )
    
    else:
        print("You cannot go there.")

def display_details(room):
    #This function combines the 3 red herrings and the clue from a room, randomly inserting the clue to hide it.
    #it then returns the text as one string to be printed after the rooms description. 
    pass


def display_notebook():
    cls()
    while execute_notebook != "close":
        print('''\nYou opened your notebook, which section do you want to turn to?

0) Close (to close notebook)
1) Suspects
2) Weapons
3) Rooms
4) Clues

(Use number key or page name)''')
        execute_notebook(normalise_input(input("...")))
    return

def execute_notebook(command):
    #Displays the notebook for the player to change the suspicion on any of the mystery elements or to look at any clues that they've previously discovered
    #The player should input which section they'd like to view, Suspects, Weapons, Rooms or clues
        global placeholder
        if 0 == len(command):
            return

        if command[0] == "suspects" or command[0] == "1":
            cls()
            notebook_suspects()
            return
        
        elif command[0] == "weapons" or command[0] == "2" :
            cls()
            notebook_weapons()
            return

        elif command[0] == "rooms" or command[0] == "3":
            cls()
            notebook_rooms()
            return

        elif command[0] == "clues" or command[0] == "4":
            cls()
            notebook_clues()
            return

        if command[0] == "close" or command[0] == "0":
            print("\nYou have closed the notebook.")
            cls()
            main()

        else:
            print("This makes no sense.")
            return

def command_directory():
    global normalised_command
    global placeholder

    if normalised_command[0] == "highlight":
        if len(normalised_command) > 1 and normalised_command[1:3]==['dining', 'room']:
            suspicion_change((" ".join(normalised_command[1:3])), "highly suspicious")
        elif len(normalised_command) > 1:
            suspicion_change(normalised_command[1], "highly suspicious")
        else:
            print("Highlight what?\n")
            editing_within_notebook_without_question(placeholder)

    elif normalised_command[0] == "cross":
        if len(normalised_command) > 1 and normalised_command[1:3]==['dining', 'room']:
            suspicion_change((" ".join(normalised_command[1:3])), "unlikely")
        elif len(normalised_command) > 1:
            suspicion_change(normalised_command[1], "unlikely")
        else:
            print("Cross what?\n")
            editing_within_notebook_without_question(placeholder)

    elif normalised_command[0] == "reset":
        if len(normalised_command) > 1 and normalised_command[1:3]==['dining', 'room']:
            suspicion_change((" ".join(normalised_command[1:3])), "neutral")
        elif len(normalised_command) > 1:
            suspicion_change(normalised_command[1], "neutral")
        else:
            print("Reset what?\n")
            editing_within_notebook_without_question(placeholder)

    else:
        print("This makes no sense.\n")
        
def editing_within_notebook_without_question(page):
    global placeholder
    global normalised_command
    if placeholder=="suspects":
        while True:
            for a in suspects:
                
                player_command = input("What would you like to do to the suspects list? (type 'Help' for help):\n...")
                normalised_command = normalise_input(player_command)

                if 0 == len(normalised_command):
                    continue
                
                elif normalised_command[0] == "close":
                    print("You have closed the notebook.\n")
                    cls()
                    main()
                
                elif normalised_command[0] == "back":
                    display_notebook()
                    cls()
                    
                    
                elif normalised_command[0] == "help":
                    notebook_display_help("suspect")

                elif normalised_command[0]=="highlight" or normalised_command[0]=="cross" or normalised_command[0]=="reset":
                    command_directory()
                

                elif len(normalised_command) == 1:
                    print("This makes no sense\n")
            
                
                elif normalised_command[1] in suspects:
                    command_directory()
                    
                elif normalised_command[1]in suspects[a]["sex"]:
                    command_directory()

                elif normalised_command[1] in suspects[a]["build"]:
                    command_directory()
                    
                elif normalised_command[1] in suspects[a]["hair colour"]:
                    command_directory()
                    

                elif normalised_command[1] in weapons or normalised_command[1] in rooms:
                    print("You are on the wrong page! This is the suspects page.\n")
                    
                else:
                    print("You cannot edit that.")
    elif placeholder == "weapons":
        while True:
                player_command = input("What would you like to do to the weapons list? (type 'Help' for help):" "\n" "...")
                normalised_command = normalise_input(player_command)

                if 0 == len(normalised_command):
                    continue
                
                elif normalised_command[0] == "close":
                    print("You have closed the notebook.\n")
                    cls()
                    main()

                elif normalised_command[0] == "help":
                    notebook_display_help("weapon")

                elif normalised_command[0] == "back":
                    print("You return to the contents page.\n")
                    display_notebook()
                    cls()
                    
                elif len(normalised_command)==1 and (normalised_command[0]=="highlight" or normalised_command[0]=="cross" or normalised_command[0]=="reset"):
                    command_directory()

                elif len(normalised_command) == 1:
                    print("This makes no sense\n")
            
                elif normalised_command[1] in weapons:
                    command_directory()

                elif normalised_command[1] in suspects or normalised_command[1] in rooms:
                    print("You are on the wrong page! This is the weapons page.\n")
                    
                else:
                    print("You cannot edit that.\n")
                    
    elif placeholder == "rooms":
        while True:
                player_command = input("What would you like to do to the rooms list? (type 'Help' for help):" "\n" "...")
                normalised_command = normalise_input(player_command)
                
                if 0 == len(normalised_command):
                    continue
                
                elif normalised_command[0] == "close":
                    print("You have closed the notebook.\n")
                    cls()
                    main()

                elif normalised_command[0] == "help":
                    notebook_display_help("room")

                elif normalised_command[0] == "back":
                    print("You return to the contents page.\n")
                    display_notebook()
                    cls()

                elif len(normalised_command)==1 and (normalised_command[0]=="highlight" or normalised_command[0]=="cross" or normalised_command[0]=="reset"):
                    command_directory()

                elif len(normalised_command) > 1 and normalised_command[1:3]==['dining', 'room']:
                    command_directory()

                elif len(normalised_command) == 1:
                    print("This makes no sense.\n")
            
                
                elif normalised_command[1] in rooms:
                    command_directory()
                    
                elif normalised_command[1] in weapons or normalised_command[1] in suspects:
                    print("You are on the wrong page! This is the rooms page.\n")
                    
                else:
                    print("You cannot edit that.\n")
                    
def editing_within_notebook(page):

    while True:
        
        yes_no_input = input("Would you like to edit the " + str(page)+ " list? (Yes/No):" "\n" "...")
        print("")
        yes_or_no = normalise_input(yes_no_input)
        
        if yes_or_no == ['yes'] or yes_or_no == ['yeah'] or yes_or_no == ['y']:
            editing_within_notebook_without_question(page)
        elif yes_or_no == ['no'] or yes_or_no == ['nah'] or yes_or_no == ['n']:
            display_notebook()
            break
        else:
            print("That is not a valid input. Please answer with Yes or No" + "\n")

def notebook_display_help(page):

    print("You can use commands:\n")
    print("HIGHLIGHT + \'" + page + "_name\'")
    print("CROSS + \'" + page + "_name\'")
    print("RESET + \'" + page + "_name\'")
    print("BACK to return to contents page")
    print("CLOSE to close notebook\n")

def print_suspects():
    # Displays the list of suspects sorted by their suspicion level
    print("\n\tLIST OF SUSPECTS\n")
    global placeholder
    placeholder="suspects"
    for suspicion in ["highly suspicious", "neutral", "unlikely"]:
        printed = False
        print("-" + suspicion.upper() + "-\n")
        for suspect in suspects:
            if suspects[suspect]["notebook_status"] == suspicion:
                for key in suspects[suspect]:
                    if key != "notebook_status":
                        print(key.title() + ": " + str(suspects[suspect][key]))
                        printed = True
                print()
        if printed == False:
            print("   None")
            print()

def notebook_suspects():
    print_suspects()
    editing_within_notebook("suspects")
    return

def print_weapons():
    # Displays the list of weapons sorted by their suspicion level
    print("\nYou open your notebook to the weapons section the list reads:")
    print("\n\tLIST OF WEAPONS\n")
    global placeholder
    placeholder="weapons"
    for suspicion in ["highly suspicious", "neutral", "unlikely"]:
        printed = False
        print("-" + suspicion.upper() + "-\n")
        for weapon in weapons:
            if weapons[weapon]["notebook_status"] == suspicion:
                print("Weapon: " + weapons[weapon]["name"])
                print("Description: " + weapons[weapon]["description"] + "\n")
                printed = True
                print()
        if printed == False:
            print("   None")
            print()

def notebook_weapons():
    print_weapons()
    editing_within_notebook("weapons")
    return

def print_rooms():
    # Displays the list of rooms sorted by their suspicion level
    print("\nYou open your notebook to the weapons section the list reads:")
    print("\n\tLIST OF ROOMS\n")
    global placeholder
    placeholder="rooms"
    for suspicion in ["highly suspicious", "neutral", "unlikely"]:
        printed = False
        print("-" + suspicion.upper() + "-\n")
        for room in rooms:
            if rooms[room]["notebook_status"] == suspicion:
                print(rooms[room]["name"] + ".")
                printed = True
                print()
        if printed == False:
            print("   None")
            print()
    
def notebook_rooms():
    print_rooms()
    editing_within_notebook("rooms")
    return

def notebook_clues():
    # Displays the list of clues previously discovered by the player
    print("\n\tLIST OF CLUES\n")
    if found_clues != []:
        for explored_room in found_clues:
            print("You explored the " + explored_room["name"] + " and investigated the " + explored_room["clue"]["detail"] + ":")
            print()
            print(explored_room["clue"]["closer inspection"]+ "\n")
    else:
        print("You are yet to find any useful clues.")
    
def suspicion_change(subject, suspicion):
    edited = False
    for element in [weapons, suspects, rooms]:
        if subject in element:
                element[subject]["notebook_status"] = suspicion
                edited = True
                if element == weapons:
                    print_weapons()
                    editing_within_notebook_without_question("weapons")
                elif element == suspects:
                    print_suspects()
                    editing_within_notebook_without_question("suspects")
                elif element == rooms:
                    print_rooms()
                    editing_within_notebook_without_question("rooms")

                
        if element == suspects:
            for suspect in suspects:
                for attribute in ["sex", "build", "hair colour"]:
                    if subject == suspects[suspect][attribute]:
                        suspects[suspect]["notebook_status"] = suspicion
                        edited = True
                    
                
            if edited == True:
                print_suspects()
                editing_within_notebook_without_question("suspects")
                #editing_within_notebook_without_question("rooms")

    if edited != True:
        print("You can't edit that\n")


def display_room(room):
    print("\n" + room["name"].upper() + "\n\n" + room["description"] + "\n")
    
    if room != rooms["lobby"]:
        clue_number = random.randint(0, 3)
        if clue_number == 0:
            print(room["clue"]["first look"])
        position = 1
        for red_herring in room["red herrings"]:
            print(red_herring)
            if position == clue_number:
                print(room["clue"]["first look"])
            position = position + 1

        print()

def init_clues(mystery):
    global clues
    clue_room = {
        "detail": "stain",
        "first look": "There's a small red STAIN on the floor just visible behind the open door.",
        "closer inspection": """As you look more closely you discover a larger puddle of blood.
Clearly this must be the room in which the murder was committed.""",
    }

    clue_witness = {
        "detail": "butler",
        "first look": "The BUTLER is in this room, tidying up",
        "closer inspection": """You ask the butler if he saw anything.
He replies in a frail voice
'I did, I saw the silhouette of a person dragging off what looked like a body earlier.'
'I couldn't tell who it was but they were definitely a """ + suspects[mystery["suspect"]]["build"] + """ person.'
'I'm sorry but that's all I know.'
You thank the butler""" 
    }

    clue_clothes = {
        "detail": "fabric",
        "first look": "Snagged on the door, you spot a scrap of FABRIC.",
        "closer inspection": """As you look closer at the fabric, you noticed spots of blood on what must be a scrap of clothing.
You also notice that the scrap is from """ + suspects[mystery["suspect"]]["sex"] + "'s clothing."
    }

    clue_hair = {
        "detail": "scuff",
        "first look": "There's a SCUFF on the wall, it looks like someone scraped against the wall, carrying something heavy.",
        "closer inspection": """You look more carefully and realise that the mark was clearly form the killer on there way past, dragging the body.
There are drips of blood and you also find a lock of hair, snagged on a nail that the killer must have brushed past on their way.
The hair is clearly """ + suspects[mystery["suspect"]]["hair colour"] + "."
    }

    clue_weapon = {
        "detail": "rug",
        "first look": "There's something vaugley shiny sticking out from under a RUG.",
        "closer inspection": "You peel back the corner of the rug and find a blood stained " + mystery["weapon"] + """.
The killer must have used this to commit the murder and then hidden it here."""
    }


    clues = {
        "room": clue_room,
        "witness": clue_witness,
        "clothes": clue_clothes,
        "hair": clue_hair,
        "weapon": clue_weapon
    }

def execute_inspect(detail):
    
    if current_room == rooms["lobby"]:
        print("You cant inspect that.")
    elif detail == current_room["clue"]["detail"]:
        if current_room in found_clues:
            #print(current_room["clue"]["closer inspection"])
            print("\nYou have already inspected " + detail.upper() + " and added clue to your notebook")
        else:
            print()
            print(current_room["clue"]["closer inspection"])
            found_clues.append(current_room)
            print("\nYou've made a note of this in the clues section of your notebook") 
    elif detail in current_room["details"]:
        detail_number = current_room["details"].index(detail)
        print()
        print(current_room["red herrings"][list(current_room["red herrings"])[detail_number]])
    else:
        print("You can't inspect that.")
    print()

def game_won():
    scroll_text("\nInspector " + player_name.title() + ", Congratulations!", 0.03)
    time.sleep(0.4)
    scroll_text("\nYour accusations were correct, and the killer has been brought to justice.", 0.03)
    time.sleep(0.4)
    scroll_text("\nThe residents of Morebrandt Mansion can rest easy knowing the killer is behind bars.", 0.03)
    time.sleep(0.4)
    while True:
        restart_game = input("\n\nWould you like to play again? (Yes/No)\n...")
        if normalise_input(restart_game)==["yes"] or normalise_input(restart_game)==["y"] or normalise_input(restart_game)==["yeah"]:
            new_game()
        elif normalise_input(restart_game)==["no"] or normalise_input(restart_game)==["n"] or normalise_input(restart_game)==["nah"]:
            print("\n\n\n")
            scroll_text("Thanks for playing!", 0.03)
            time.sleep(4)
            quit()
        else:
            print("Please answer Yes or No")            

def game_over():
    scroll_text("Inspector " + player_name.title() +",\nYou have failed this case. ", 0.05)
    time.sleep(0.4)
    scroll_text("\nThe murder of Morebrandt mansion remains unsolved.", 0.05)
    time.sleep(0.4)
    scroll_text("\n\nGAME OVER",0.06)
    time.sleep(0.4)
    while True:
        restart_game = input("\n\nWould you like to try again? (Yes/No)\n...")
        if normalise_input(restart_game)==["yes"] or normalise_input(restart_game)==["y"] or normalise_input(restart_game)==["yeah"]:
            new_game()
        elif normalise_input(restart_game)==["no"] or normalise_input(restart_game)==["n"] or normalise_input(restart_game)==["nah"]:
            print("\n\n\n")
            scroll_text("Thanks for playing!", 0.03)
            time.sleep(4)
            quit()
        else:
            print("Please answer Yes or No")

def cls():
    print("\n" * 100)
            
if __name__ == "__main__":
    introduction()
    main()


