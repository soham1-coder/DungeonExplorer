import random

from Playerinit import Player

class Difficulty:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def makeBoss(self):
        health = 50 * self.health
        attack_power = 10 * self.attack
        return Player("Goblin", health, attack_power)

    def description(self):
        return f"Boss: {self.name},Health:  {self.health}, Attack Power: {self.attack}"

Difficulties = {
    "easy": Difficulty("Goblin", 0.75, 0.75),
    "Normal": Difficulty("Orc", 1, 1),
    "Hard": Difficulty("Troll", 1.5, 1.5)
}