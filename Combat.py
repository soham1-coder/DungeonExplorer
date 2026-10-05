from Playerinit import Player, tank
import random

def apply_damage(target, amount):
    if isinstance(target, tank):
        amount = amount // target.deflect
    target.health = target.health - amount
    return amount

def attack(attacker, target):
    damage = apply_damage(target, attacker.attack_power)
    print(f"{attacker.name} hits {target.name} for {damage} damage.")

def show_health(hero, enemy):
    print(f"\n{hero.name} = {hero.health} HP | {enemy.name} = {enemy.health} HP")

def player_turn(hero, enemy):
    while True:
        action = input("Attack or Run? (A, R)\n").strip().upper()
        if action == "A":
            attack(hero, enemy)
            return "continue"
        if action == "R":
            if random.random() < 0.5:
                print("You have escaped")
                return "ran away"
            print("Couldn't escape!")
            return "continue"
        print("invalid inp")

def fight(hero, enemy):
    print(f"\nA {enemy.name} appears!\n")

    while hero.health > 0 and enemy.health > 0:
        show_health(hero, enemy)

        if player_turn(hero, enemy) == "ran away":
            return "ran away"
        if enemy.health <= 0:
            print(f"{enemy.name} have been defeted")
            return "win"

        attack(enemy, hero)

    print(f"{hero.name} have fallen...")
    return "lose"