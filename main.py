"""Entry point for the group project.

`python main.py` must run your project at every milestone, so keep this file working
from Milestone 1 onward.
"""

from Playerinit import Player, mage, warrior, tank, healer
from maze import Maze
from maze_explorer import Explorer, show_status
from Combat import fight
from PlayerTest import choose_hero

CLASSES = {"mage": mage, "warrior": warrior, "tank": tank, "healer": healer}


#initializes a maze upon game start
class Play:
#a little janky but it works to create a character and chose the class
    def __init__(self):
        name = input("What is the name of your character? ")

        while True:
            choice = input("What class would you like to be? -help for info").lower()

            if choice == "mage":
                self.hero = mage(name)
                break
            elif choice == "warrior":
                self.hero = warrior(name)
                break
            elif choice == "tank":
                self.hero = tank(name)
                break
            elif choice == "healer":
                self.hero = healer(name)
                break
            else:
                print("Invalid, (mage, warrior, tank, healer)")

        self.maze = Maze()
        self.explorer = Explorer(self.maze)
        self.exit = self.maze.find_exit()


    def game_loop(self):

        #ensuring that while the player is "alive  " the game remains active allowing movement through the maze and engaging with the surroudings
        while self.hero.health > 0:

            #shows a new maze every turn to keep player symbol updated
            draw_maze(self.maze, self.explorer)
            show_status(self.explorer)

            # recieves players input for direction and movement as well as quitting out
            choice = input("F = move, L = left, R = right, Q = quit: ").lower()

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
                            break

                    #reaching the exit cell in the right column wins the game
                    if (self.explorer.row, self.explorer.col) == self.exit:
                        draw_maze(self.maze, self.explorer)
                        print("You found the exit. You win!")
                        break
                        
                #running the other possiblities so we dont run into an error and the recursion continues
                else:
                    print("There is a wall!")

            elif choice == "l":
                self.explorer.turn_left()

            elif choice == "r":
                self.explorer.turn_right()

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


def main():
    game = Play()
    game.game_loop()


if __name__ == '__main__':
    main()
