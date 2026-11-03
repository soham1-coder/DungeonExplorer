from Playerinit import Player, mage, warrior, tank, healer
from Combat import fight
from maze import Maze
from maze_explorer import Explorer

#implinents direction when the player is moving throughout the maze
def draw_maze(maze, explorer):
    print()
    for r, row in enumerate(maze.grid):
        line = ""
        for c, cell in enumerate(row):
            line += explorer.direction.symbol if (r, c) == (explorer.row, explorer.col) else cell
        print(line)
    print()

#keeping every single action as a previous move so we can work with the undo
class undoStack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    def is_empty(self):
        return len(self.items) == 0


class Play:

    #brand new and a key part of the undo function. This saves the previous move and in use with the undoStack it allows going back with moves in case of a mistake
    def save_state(self):
        self.history.push((self.explorer.row, self.explorer.col, self.explorer.direction))

   #could be optimized but it works to make a character with a class
    def __init__(self):
        name = input("What is the name of your character? ")

        while True:
            choice = input("What class would you like to be? ").lower()

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
# initialize the main parts of the game generating maze and the player, now also saving the undo history
        self.maze = Maze()
        self.explorer = Explorer(self.maze)
        self.history = undoStack()

    def game_loop(self):
#ensuring that while the player is "alive  " the game remains active allowing movement through the maze and engaging with the surroudings
        while self.hero.health > 0:

            # Show maze, importing the grid of the maze
            draw_maze(self.maze, self.explorer)

            # recieves players input for direction and movement as well as quitting out
            choice = input("F = move, L = left, R = right, U = undo, Q = quit: ").lower()

            if choice == "f":
                #new save state function which is in all 3 movement options
                self.save_state()
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
#running the other possiblities so we dont run into an error and the recursion continues
                else:
                    print("There is a wall!")

            elif choice == "l":
                self.save_state()
                self.explorer.turn_left()

            elif choice == "r":
                self.save_state()
                self.explorer.turn_right()
            elif choice == "u":
                #as long as there is move history, we can undo if there is not then the undo cannot be executed because there is nothing to undo
                if not self.history.is_empty():
                    self.explorer.row, self.explorer.col, self.explorer.direction = self.history.pop()
                else:
                    print("No previous moves, nothing to undo")
            elif choice == "q":
                break

            else:
                print("Invalid input")

        print("Game Over")

#this is the main, all it really does for now is execute the game loop in the Play class
def main():
    game = Play()
    game.game_loop()


if __name__ == "__main__":
    main()