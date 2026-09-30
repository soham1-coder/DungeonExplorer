from Playerinit import mage, warrior, tank, healer

#This takes the input then stores the name in a str for later use 
name = input("What is the name of your char? ")
#This takes the input for the class then makes it lowercase for easier to write the if statements


#These if statements just ask if what you typed in is a class if not the while loop has you put in a new name 
while(True):
    choice = input("What class would you like to be? ").lower()
    if choice == "mage":
        hero = mage(name)
        break
    elif choice == "warrior":
        hero = warrior(name)
        break
    elif choice == "tank":
        hero = tank(name)
        break
    elif choice == "healer":
        hero = healer(name)
        break
    else:
        print(f"This is not a class please try again there is only 4 classes mage, tank, warrior, healer")

hero.DisplayStatus()