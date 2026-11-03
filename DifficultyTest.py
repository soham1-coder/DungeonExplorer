from Difficulty import Difficulties
from CommandLine import getDifficulty
from Combat import fight
from PlayerTest import choose_hero


if __name__ == "__main__":
    print("All difficulties:")
    for level, difficulty in Difficulties.items():
        boss = difficulty.makeBoss()
        print(f"  {level}: {boss.name}, {boss.health} health, {boss.attack_power} attack\n")

    difficulty = getDifficulty()

    boss = difficulty.makeBoss()
    boss.DisplayStatus()

    hero = choose_hero()
    hero.DisplayStatus()

    result = fight(hero, boss)
    print(f"Result: {result}")
