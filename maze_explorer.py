from enum import Enum

#Using enumeration to keep a clear name of the directions used in the game and avoid magic numbers

from maze import Maze


class Direction(Enum):
    #Each direction stores its name, an arrow symbol, and position change when moving forward throughout the array
    UP = ("UP", "^", -1, 0)
    RIGHT = ("RIGHT", ">", 0, 1)
    DOWN = ("DOWN", "v", 1, 0)
    LEFT = ("LEFT", "<", 0, -1)

    def __init__(self, label, symbol, d_row, d_col):
        self.label = label
        self.symbol = symbol
        self.d_row = d_row
        self.d_col = d_col

    def turn_right(self):
        order = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        return order[(order.index(self) + 1) % 4]

    def turn_left(self):
        order = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        return order[(order.index(self) - 1) % 4]



class Explorer:
    def __init__(self, maze):
        self.maze = maze
        self.row = maze.find_entrance()
        self.col = 0
        self.direction = Direction.RIGHT  #starts facing into the maze/dungeon

    def turn_right(self):
        self.direction = self.direction.turn_right()

    def turn_left(self):
        self.direction = self.direction.turn_left()

    def move_forward(self):

        new_row = self.row + self.direction.d_row
        new_col = self.col + self.direction.d_col
        if self.maze.is_wall(new_row, new_col):
            return False
        self.row, self.col = new_row, new_col
        return True


def show_status(explorer):
    print(f"You are facing: {explorer.direction.label} ({explorer.direction.symbol})")
    print("Controls:  F = move forward | L = turn left | R = turn right | Q = quit")
    print("Legend:    # = wall | B = boss | arrow = you")



