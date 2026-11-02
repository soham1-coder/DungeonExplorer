import os
from save_system import save_game, load_game, save_high_score, load_high_scores

from Playerinit import Player, mage, warrior, tank, healer
from maze import Maze
from maze_explorer import Explorer, show_status
from Combat import fight
from PlayerTest import choose_hero

CLASSES = {"mage": mage, "warrior": warrior, "tank": tank, "healer": healer}
SAVE_FILE = "savegame.json"
SCORE_FILE = "high_scores.csv"


#initializes a maze upon game start
class Play:
    def __init__(self, hero=None, maze=None, row=None, col=None, steps=0, bosses_defeated=0):
            if hero is None:
                name = input("What is the name of your character? ")
                while True:
                    choice = input("What class would you like to be? -help(TBD) for info").lower()
                    if choice in CLASSES:
                        self.hero = CLASSES[choice](name)
                        break
                    else:
                        print("Invalid, (mage, warrior, tank, healer)")

                self.maze = Maze()
                self.explorer = Explorer(self.maze)
            else:
                # Rebuild state from loaded save file
                self.hero = hero
                self.maze = maze if maze else Maze()
                self.explorer = Explorer(self.maze)
                if row is not None and col is not None:
                    self.explorer.row = row
                    self.explorer.col = col

            self.exit = self.maze.find_exit()
            self.steps = steps
            self.bosses_defeated = bosses_defeated


    def game_loop(self):

        #ensuring that while the player is "alive  " the game remains active allowing movement through the maze and engaging with the surroudings
        while self.hero.health > 0:

            #shows a new maze every turn to keep player symbol updated
            draw_maze(self.maze, self.explorer)
            show_status(self.explorer)

            # recieves players input for direction, movement as well as saving and quitting out
            choice = input("F = move, L = left, R = right, S = save, Q = quit: ").lower()

            if choice == "f":

                if self.explorer.move_forward():

                    # seeing if there is a boss, if so it engages the "fight" function from Combat
                    if self.maze.is_boss(
                        self.explorer.row,
                        self.explorer.col
                    ):
                        enemy = Player("Goblin", 50, 10)

                        result = fight(self.hero, enemy)

                        if result == "win":
                            self.maze.clear_boss(
                                self.explorer.row,
                                self.explorer.col
                            )

                        elif result == "lose":
                            save_high_score(SCORE_FILE, self.hero.name, self.hero.__class__.__name__, self.steps, self.bosses_defeated, "DEFEATED")
                            break

                    #reaching the exit cell in the right column wins the game
                    if (self.explorer.row, self.explorer.col) == self.exit:
                        draw_maze(self.maze, self.explorer)
                        print("You found the exit. You win!")

                        #Log high score on win
                        save_high_score(SCORE_FILE, self.hero.name, self.hero.__class__.__name__, self.steps, self.bosses_defeated, "VICTORY")
                        break
                        
                #running the other possiblities so we dont run into an error and the recursion continues
                else:
                    print("There is a wall!")

            elif choice == "l":
                self.explorer.turn_left()

            elif choice == "r":
                self.explorer.turn_right()

            elif choice == "s":
                try:
                    save_game(SAVE_FILE, self.hero, self.explorer.row, self.explorer.col, self.maze, self.steps, {"bosses_defeated": self.bosses_defeated})    
                    print("Game saved!")
                except (OSError, TypeError) as e:
                        print(f"Could not save: {e}")

            #elif choice == "q" and saved != True:  
               # print("Are you sure you would like to quit before saving?")  

            elif choice == "q":
                break

            else:
                print("Invalid input")

        print("Game Over")

#Loops through the maze object to recreate and display it with a player symbol (an arrow) on the player's current position
def draw_maze(maze, explorer):

    print()

    #Checks row and column index(r,c) for each cell: 
    #If it equals player position: set the cell to an arrow and append to line.
    #Otherwise appends the character that was already in the maze cell
    for r, row in enumerate(maze.grid):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == (explorer.row, explorer.col):
                char = explorer.direction.symbol
            else:
                char = cell
            line += char
        print(line)
    print()

def view_leaderboard():
    scores = load_high_scores(SCORE_FILE)
    if not scores:
        print("\nNo high score records found yet!")
        return
    print("\nhigh scores")
    print(f"{'Rank':<5} {'Name':<15} {'Class':<10} {'Steps':<8} {'Bosses':<8} {'Status':<10}")
    print("-" * 60)
    for idx, entry in enumerate(scores, 1):
        print(
            f"{idx:<5} {entry.get('Player Name',''):<15} {entry.get('Class',''):<10} "
            f"{entry.get('Steps',''):<8} {entry.get('Bosses Defeated',''):<8} {entry.get('Status',''):<10}")

def main():

    while True:
        print("\nDungeon Explorer")
        print("1. Start New Game")
        print("2. Load Saved Game")
        print("3. View Leaderboard")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ").strip()

        if choice == "1":
            game = Play()
            game.game_loop()

        elif choice == "2":
            try:
                hero, row, col, dungeon, steps, extra = load_game(SAVE_FILE)
                bosses = extra.get("bosses_defeated", 0)
                game = Play(hero=hero, maze=dungeon, row=row, col=col, steps=steps, bosses_defeated=bosses)
                game.game_loop()
            except FileNotFoundError:
                print(f"\nNo save file found at '{SAVE_FILE}'. Please start a new game ")
            except Exception as e:
                print(f"\nError loading save file: {e}")

        elif choice == "3":
            view_leaderboard()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid selection! Please enter 1, 2, 3, or 4.")


if __name__ == '__main__':
    main()
