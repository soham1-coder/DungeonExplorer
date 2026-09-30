
# Creates a player class for ease of use when initilizing is also used for other classes 
class Player: 
    # this initializes the name, health and attack power for later use in all of the classes 
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
    #This displays all the status of all the self. functions that are defined in the __init__ above 
    def DisplayStatus(self):
        print(f"Name: {self.name} ")
        print(f"Health: {self.health}")
        print(f"Attack_power: {self.attack_power}")
        
# creates a subclassed named mage. Gives attack power health and the name of the created player with the addition
# of a special stat exclusive to the Subclass
class mage(Player):
    def __init__(self, name):
        super().__init__(name, health = 80, attack_power = 40)
        self.mana = 100
        print(f"Mana: {self.mana}")
        

# creates a subclassed named warrior. Gives attack power health and the name of the created player with the addition
# of a special stat exclusive to the Subclass        
class warrior(Player):
    def __init__(self,name):
        super().__init__(name, health=100, attack_power= 30)
        self.rage = 0
        print(f"Rage: {self.rage}")


# creates a subclassed named tank. Gives attack power health and the name of the created player with the addition
# of a special stat exclusive to the Subclass
class tank(Player): 
    def __init__(self, name):
        super().__init__(name, health = 150, attack_power = 10)
        self.deflect = 2
        print(f"Deflect: {self.deflect}")

# creates a subclassed named healer. Gives attack power health and the name of the created player with the addition
# of a special stat exclusive to the Subclass
class healer(Player):
    def __init__(self, name,):
        super().__init__(name, health = 110, attack_power = 15)
        self.heal = 3
        print(f"Heal: {self.heal}")