from Playerinit import Player, mage, warrior, tank, healer
from Combat import fight
from maze import Maze
from maze_explorer import Explorer


class Play:
#a little janky but it works to create a character and chose the class
    def __init__(self):
        name = input("What is the name of your char? ")

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

        self.maze = Maze()
        self.explorer = Explorer(self.maze)

    def game_loop(self):
#ensuring that while the player is "alive  " the game remains active allowing movement through the maze and engaging with the surroudings
        while self.hero.health > 0:

            # Show maze, importing the grid of the maze
            for row in self.maze.grid:
                print("".join(row))

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

#this is the main, all it really does for now is execute the game loop in the Play class
def main():
    game = Play()
    game.game_loop()


if __name__ == "__main__":
    main()