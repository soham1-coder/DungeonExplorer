from Playerinit import Player, mage, warrior, tank, healer
from Combat import fight


def choose_hero():
    #This takes the input then stores the name in a str for later use
    name = input("What is the name of your char? ")

    #These if statements just ask if what you typed in is a class if not the while loop has you put in a new name
    while(True):
        choice = input("What class would you like to be? ").lower()
        if choice == "mage":
            return mage(name)
        elif choice == "warrior":
            return warrior(name)
        elif choice == "tank":
            return tank(name)
        elif choice == "healer":
            return healer(name)
        else:
            print(f"This is not a class please try again there is only 4 classes mage, tank, warrior, healer")


if __name__ == "__main__":
    hero = choose_hero()
    hero.DisplayStatus()

    Goblin = Player("Goblin", 50, 10)

    fight(hero, Goblin)
