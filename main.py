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
def draw_maze(maze, explorer):
    print()
    for r, row in enumerate(maze.grid):
        line = ""
        for c, cell in enumerate(row):
            line += explorer.direction.symbol if (r, c) == (explorer.row, explorer.col) else cell
        print(line)
    print()


def Play():
    print("=== Maze Explorer ===")
    hero = choose_hero()
    print()
    hero.DisplayStatus()

    maze = Maze()
    explorer = Explorer(maze)
    exit_pos = maze.find_exit()

    while True:
        draw_maze(maze, explorer)
        show_status(explorer)
        print("Other:     S = show hero status")
        action = input("> ").strip().upper()

        if action == "F":
            if not explorer.move_forward():
                print("You bump into a wall.")
            elif maze.is_boss(explorer.row, explorer.col):
                boss = Player("Boss", 60, 15)
                result = fight(hero, boss)
                if result == "win":
                    maze.clear_boss(explorer.row, explorer.col)
                elif result == "lose":
                    print("Game over.")
                    return
                else:
                    print("You flee back into the maze.")
            if (explorer.row, explorer.col) == exit_pos:
                draw_maze(maze, explorer)
                print("You found the exit. You win!")
                return
        elif action == "L":
            explorer.turn_left()
        elif action == "R":
            explorer.turn_right()
        elif action == "S":
            hero.DisplayStatus()
        elif action == "Q":
            print("Thanks for playing.")
            return
        else:
            print("Invalid input.")


def main():
    Play()


if __name__ == '__main__':
    main()
