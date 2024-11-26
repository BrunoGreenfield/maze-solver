import argparse
from random import choice

# Mazename flag
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--mazename", help='The path to the maze txt file', required=True)
args = parser.parse_args()
mazeName = args.mazename


class Player:
    def __init__(self):
        self.squareCosts = []
        self.frontier = []

    def currentPos(self):
        playerIndex = ''
        for row in maze:
            if 'A' not in row:
                continue
            playerIndex = str(maze.index(row)) + str(row.index('A'))

        return playerIndex
    
    def checkGoalState(self):
        if self.currentPos() == goalPos:
            return True
        return False
    
    # Calculates the estimated closeness of any given square, ignoring hedges (obviously)
    def heuristic(self, givenSquare):
        x1, y1 = map(int, givenSquare)
        x2, y2 = map(int, goalPos)
        return abs(x2-x1) + abs(y2-y1)

    def chooseRandom(self):
        pass

class BFS(Player):
    def __init__(self):
        super().__init__()

    def play(self):
        print(self.frontier)

class DFS(Player):
    def __init__(self):
        super().__init__()
    
    def play(self):
        pass


def displayMaze():
    print()
    for row in maze:
        for char in row:
            match char:
                case '#':
                    print("\033[31m#\033[0m", end=' ') # '#'
                case '0':
                    print("\033[32m0\033[0m", end=' ') # '0'
                case 'A':
                    print("\033[33mA\033[0m", end=' ') # 'A'
                case 'Z':
                    print("\033[34mZ\033[0m", end=' ') # 'Z'
        print() # Create a new line after every row

def getGoalPos():
    for row in maze:
        if 'Z' not in row:
            continue
        return str(maze.index(row)) + str(row.index('Z'))


# Opening the maze creating a lists of lists to represent
with open(mazeName, "r") as mazeFile:
    maze = [list(row.strip()) for row in mazeFile if '#' in row]
goalPos = getGoalPos() # Must be run instantly as the maze will change as the game is played

player = BFS()

displayMaze()
print('Goal Position:', goalPos)
print('Current Position:', player.currentPos())
print('Heuristic:', player.heuristic(player.currentPos()))
maze[3][2] = 'A'
maze[5][0] = '0'
displayMaze()
print('Current Position:', player.currentPos())
print('Heuristic:', player.heuristic(player.currentPos()))
maze[3][2] = '0'
maze[0][5] = 'A'
displayMaze()
print('Current Position:', player.currentPos())
print('Heuristic:', player.heuristic(player.currentPos()))
print('Goal State:', player.checkGoalState())