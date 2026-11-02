import os
from Playerinit import mage, warrior, tank
from maze import Maze
from save_system import (
    player_to_dict,
    player_from_dict,
    save_game,
    load_game,
    save_high_score,
    load_high_scores,
)

print("\nPlayer testing")
# Create a player, take damage, and spend special attack
hero1 = mage("Merlin")
hero1.health = 55
hero1.mana = 40

# Convert player to dict and print it
player_dict = player_to_dict(hero1, row=2, col=5)
print("Saved Player Dict:", player_dict)

# tests player from dict and check values
old_hero = player_from_dict(player_dict)
print("Name:", old_hero.name)
print("Class:", old_hero.__class__.__name__)
print("HP:", old_hero.health)
print("Mana:", old_hero.mana)

print("\nsave and load game test")
# Create hero and maze
player2 = warrior("hmmm")
player2.health = 90
player2.rage = 20

game_maze = Maze()

# Clear a boss at position (3, 14)
print("Clearing boss")
game_maze.clear_boss(3, 14)

# Save the game to a json file
save_file = "test_game.json"
save_game(
    save_file,
    player2,
    row=3,
    col=14,
    maze=game_maze,
    steps=15,
    extra_info={"difficulty": "hard"},
)

# Load the game from json file
loaded_hero, r, c, loaded_maze, steps, extra = load_game(save_file)

print("\nloading hero test")
print("Name:", loaded_hero.name)
print("Class:", loaded_hero.__class__.__name__)
print("HP:", loaded_hero.health)
print("Rage:", loaded_hero.rage)
print("Position: Row", r, "Col", c)
print("Steps taken:", steps)
print("does the boss exists:", loaded_maze.is_boss(3, 14))

print("\n high score test")
score_file = "test_scores.csv"

# Remove test score file if it exists from a previous run
if os.path.exists(score_file):
    os.remove(score_file)

# Save 3 test runs 
save_high_score(score_file, "Thor", "warrior", 45, 2, "victory")
save_high_score(score_file, "Merlin", "mage", 18, 3, "Victory")
save_high_score(score_file, "Bob", "tank", 60, 0, "Lost")

# Read and print high scores
scores = load_high_scores(score_file)
print("\nhigh score test")
for s in scores:
    print(s)

# Clean up test files
if os.path.exists(save_file):
    os.remove(save_file)
if os.path.exists(score_file):
    os.remove(score_file)