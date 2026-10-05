
#Starter maze (can be adjusted to add checkpoints, bosses)
DEFAULT_MAZE = [
    "#####################",
    "    #     #         #",
    "# # # ### # ####### #",
    "# #   #   #   B   # #",
    "# ##### ######### # #",
    "#     #     B     # #",
    "##### ########### # #",
    "#   #           # # #",
    "# # ##### ##### # # #",
    "# #     # #   B #    ",
    "#####################",
]

#Generates maze using a grid based output on the terminal
class Maze:
    def __init__(self, rows=None):
        self.grid = [list(row) for row in (rows or DEFAULT_MAZE)]

    def is_wall(self, row, col):
        #any row or col outside the maze array counts as a wall
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[row]):
            return True
        return self.grid[row][col] == "#"

    #Boss fight detection (based on position in array)
    def is_boss(self, row, col):
        if self.is_wall(row, col):
            return False
        return self.grid[row][col] == "B"


    #The entrance is the open cell in the left (first) column
    def find_entrance(self):
        for row in range(len(self.grid)):
            if not self.is_wall(row, 0):
                return row
        raise ValueError("Dungeon/Maze has no entrance")
    


    #The exit will be the open row in the right most columm (TBD)
    def find_exit(self):
        last_col = len(self.grid[0]) - 1
        for row in range(len(self.grid)):
            if not self.is_wall(row, last_col):
                return (row, last_col)
        raise ValueError("Dungeon/Maze has no exit")


    #Checks if they went pass the boss position
    def clear_boss(self, row, col):
        self.grid[row][col] = " "

