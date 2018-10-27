#from items import *
from map import rooms
from gameparser import *

current_room = rooms["lobby"]

def age_verification(name):

    while True:

        try:
            print("How old are you?")
            player_age = int(input("..."))

            if player_age < 0 or player_age > 100:
                print("Please enter age between 1-100")
                continue

            elif player_age >= 13:
                print_welcome(name)

            else:
                print("You are too young to play this game.")
                quit()
            break
        
        except ValueError:
            print("You did not enter a valid number.")

def print_welcome(name):

    print()
    print('''Please choose a difficulty level.

    1) Easy
    2) Medium
    3) Hard
    ''')
    

