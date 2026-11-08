
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

#Bosses only chase the player when they are within this many cells (straight-line, ignoring walls)
BOSS_AGGRO_RANGE = 6

BOSS_HEALTH = 50
#how many forward steps a boss stays frozen after the player successfully runs from it
BOSS_STUN_TURNS = 3

#Generates maze using a grid based output on the terminal
class Maze:
    def __init__(self, rows=None):
        self.grid = [list(row) for row in (rows or DEFAULT_MAZE)]
        #per-boss health and stun, keyed by (row, col); a boss with no entry is at full health and not stunned
        self.boss_state = {}

    #Returns the state dict for the boss at pos, creating a fresh one if the boss hasn't been fought yet
    def get_boss_state(self, pos):
        return self.boss_state.setdefault(pos, {"health": BOSS_HEALTH, "stun": 0})

    #Boss state as a list of plain dicts so it can be written to the save file
    def boss_state_to_list(self):
        return [{"row": r, "col": c, **state} for (r, c), state in self.boss_state.items()]

    def load_boss_state(self, entries):
        self.boss_state = {(e["row"], e["col"]): {"health": e["health"], "stun": e["stun"]}
                           for e in entries}

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
    


    #The exit will be the open row in the right most columm
    def find_exit(self):
        last_col = len(self.grid[0]) - 1
        for row in range(len(self.grid)):
            if not self.is_wall(row, last_col):
                return (row, last_col)
        raise ValueError("Dungeon/Maze has no exit")


    #Checks if they went pass the boss position
    def clear_boss(self, row, col):
        self.grid[row][col] = " "
        self.boss_state.pop((row, col), None)

    #Greedy step: look at the open neighbours and pick the one with the smallest Manhattan distance to the target.
    #Only takes a step that gets strictly closer, so a boss can get stuck behind a wall (no backtracking).
    #Returns None if the target is further than max_dist or no neighbour is closer
    def greedy_step_toward(self, start, target, exit_pos, max_dist=BOSS_AGGRO_RANGE):
        def manhattan(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        best = start
        best_dist = manhattan(start, target)
        if best_dist > max_dist:
            return None
        for d_row, d_col in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (start[0] + d_row, start[1] + d_col)
            if self.is_wall(*nxt) or nxt == exit_pos:
                continue
            #cannot step onto another boss, but can step onto the player
            if nxt != target and self.grid[nxt[0]][nxt[1]] != " ":
                continue
            d = manhattan(nxt, target)
            if d < best_dist:
                best, best_dist = nxt, d
        return None if best == start else best

    #Moves every boss one cell toward the player using the greedy step above.
    #Bosses never step onto other bosses or the exit. Returns True if a boss reached the player
    def move_bosses(self, player_pos, max_dist=BOSS_AGGRO_RANGE):
        exit_pos = self.find_exit()
        bosses = [(r, c) for r, row in enumerate(self.grid)
                  for c, cell in enumerate(row) if cell == "B"]
        for boss in bosses:
            #a stunned boss loses a turn of stun instead of moving
            state = self.boss_state.get(boss)
            if state and state["stun"] > 0:
                state["stun"] -= 1
                continue
            step = self.greedy_step_toward(boss, player_pos, exit_pos, max_dist)
            if step is None:
                continue
            self.grid[boss[0]][boss[1]] = " "
            self.grid[step[0]][step[1]] = "B"
            #the boss keeps its health when it moves
            if state:
                self.boss_state[step] = self.boss_state.pop(boss)
            if step == player_pos:
                return True
        return False

