#import things for saving and reading file
import json
import csv
import os

#import specific things from created files
from Playerinit import Player, mage, warrior, tank, healer
from maze import Maze

#creates a dictonary that sets the python class to a string 
#this helps reading the file as when reading files it treats it as a string
class_map = {
    "mage": mage,
    "warrior": warrior,
    "tank": tank,
    "healer": healer,
    "player": Player,
    "Player": Player
}

#creates a dictonary for player and grabs the row and collum for saving in the maze
def player_to_dict(player, row = 0, col = 0):

    #a dictonary for all stats
    data = {

        #used for all class types
        "class_type": player.__class__.__name__,

        #sets/gets the plater name
        "name": player.name,

        #sets/gets the health
        "health": player.health,

        #sets/gets the players special ability
        "attack_power": player.attack_power,

        #sets/gets the players spot in the maze
        "row": row,
        "col": col
    }
    #these all check for if the player has one of the special abilitys 
    #if the player has one of the abilitys add it to the data dict
    if hasattr(player, "mana"):
        data["mana"] = player.mana
    if hasattr(player, "rage"):
        data["rage"] = player.rage
    if hasattr(player, "deflect"):
        data["deflect"] = player.deflect
    if hasattr(player, "heal"):
        data["heal"] = player.heal

    #returns the new data dict
    return data

def player_from_dict(data):
    #gets class_type if it doesnt work gets player instead
    class_type = data.get("class_type", "Player")
    
    #gets name if it doesnt work gets Unkown hero instead
    name = data.get("name", "Unkown Hero")

    #looks at the object in class_map using class_type if it can't find it get Player instead
    cls = class_map.get(class_type, Player)

    #asks if the class gotten is in the Player class list
    if cls is Player: 

        #sets the hero to be the Player with the player class
        # gets the name
        #gets the health but if it can't find it sets it to 100
        #same with attack_power but if it cant find it sets it to 15
        hero = Player(name, data.get("health", 100), data.get("attack_power", 15))
    else:
        #init the class name 
        hero = cls(name)
        #changes health and attack_power to get the stats for it in the saved file
        hero.health = data.get("health", hero.health)
        hero.attack_power = data.get("attack_power", hero.attack_power)

    #asks if the special ability exist and if it does use the stored value 
    if "mana" in data and hasattr(hero, "mana"):
        hero.mana = data["mana"]
    if "rage" in data and hasattr(hero, "rage"):
        hero.rage = data["rage"]
    if "deflect" in data and hasattr(hero, "deflect"):
        hero.deflect = data["deflect"]
    if "heal" in data and hasattr(hero, "heal"):
        hero.heal = data["heal"]
    #returns the updated hero information
    return hero

#saves the entire game to the point of being saved
def save_game(filepath, player, row, col, maze, steps = 0, extra_info = None):
    """
        filepath (str): Path to save destination file.
        player (Player): Active player instance.
        row (int): Current player row position.
        col (int): Current player col position.
        maze (Maze): Active Maze instance (preserves cleared bosses).
        steps (int): Counter for player steps taken.
        extra_info (dict): Optional additional metadata.
    """
    #stores the maze in string for easier saving
    grid_strings = ["".join(r) for r in maze.grid]

    #game session details
    game_state = {
        #version for age of file
        "version": "1.0",
        #saves player, row and col position
        "player": player_to_dict(player, row, col),
        #saves the layout of the maze
        "maze_grid": grid_strings,
        #saves the steps taken for better position saving
        "steps": steps,
        #saves the extra info if not use a empty dict
        "extra_info": extra_info or {}
    }
    #grabs the path from the file
    dirname = os.path.dirname(filepath)

    #asks if the path exist in the file
    if dirname:
        # makes the missing dirs 
        # exist_ok = true is used so it doesn't break if the dirs exist 
        os.makedirs(dirname, exist_ok = True)

    # opens the file for writing
    #utf-8 is used so the file will close if an error or its done writing 
    with open (filepath, "w", encoding = "utf-8") as f:
    
        #makes game_state a json text file w 4 indents and writes to it
        json.dump(game_state, f, indent = 4)
    
    #states that it was saved properly
    print(f"Game saved to {filepath}")

#get json file patj
def load_game(filepath):
    #looks for the file and ask if it exists
    if not os.path.exists(filepath):

        #show error msg if it doesn't exist 
        raise FileNotFoundError(f"Save File {filepath} doesn't exitst")
    
    #once found read the file with utf-8 encoding
    with open(filepath, "r", encoding = "utf-8") as f:
    
        #sets the file to a dict
        game_state = json.load(f)
    
    #grabs player if it cant find it set to a empty dict
    p_data = game_state.get("player", {})
    
    #passes player dict to get the hero 
    hero = player_from_dict(p_data)
    
    #gets the last row and column the player was in
    row = p_data.get("row", 0)
    col = p_data.get("col", 0)
    
    #grabs the last maze layout 
    maze_grid = game_state.get("maze_grid")
    
    #creates the maze from the saved maze
    loaded_maze = Maze(rows = maze_grid) if maze_grid else Maze()
    
    #grabs the step counter if it can't find it set to 0
    steps = game_state.get("steps", 0)
    
    #grab extra data if none set to a empty dict
    extra_info = game_state.get("extra_info", {})
    
    #outputs saying it loaded successfully 
    print(f"Game loaded successfully from '{filepath}'.")
    
    #returns all the info updateding the data
    return hero, row, col, loaded_maze, steps, extra_info

#saveed high score function
def save_high_score(filepath, player_name, class_type, steps, bosses_defeated, status="VICTORY"):
    
    #checks if the file exists
    file_exists = os.path.exists(filepath)
    
    #grabs the path for later use
    dirname = os.path.dirname(filepath)
    
    #looks for subfolder 
    if dirname:
    
        #if it doesnt exist make it but if it does follow the second arg
        os.makedirs(dirname, exist_ok=True)
    
    #append the file
    with open(filepath, "a", newline="", encoding="utf-8") as f:
    
        #creates a csv writer
        writer = csv.writer(f)
    
        # if teh csv file was just created or doesn't exits add all the info needed
        if not file_exists:
            writer.writerow(["Player Name", "Class", "Steps", "Bosses Defeated", "Status"])
        writer.writerow([player_name, class_type, steps, bosses_defeated, status])
    
    #print that it was successfull
    print(f"High score recorded in '{filepath}'.")

#function for loading the high score
def load_high_scores(filepath):
    
    #if the file doesn't exist put a empty dict
    if not os.path.exists(filepath):
        return []
    
    #used for storing the empty list
    scores = []
    
    #open file to write 
    with open(filepath, "r", encoding="utf-8") as f:
    
        #intis dictReader
        reader = csv.DictReader(f)
    
        #for statement that goes threw each row
        for row in reader:
    
            #appends the scores to the rows
            scores.append(row)
            
    # Sort by steps for victories
    scores.sort(key=lambda x: int(x.get("Steps", 9999)))
    
    #return the highscore
    return scores