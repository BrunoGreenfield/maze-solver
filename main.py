import argparse
from time import sleep
import os

# Mazename flag
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--mazename", help='The path to the maze txt file', required=True)
args = parser.parse_args()
mazeName = args.mazename


class Player:
    def __init__(self):
        self.squareCosts = []
        self.frontier = []
        self.goodChars = ['0', 'Z'] # This is a list of characters the player can move too
        self.currentSquare = self.currentPos()
        self.exploredSquares = [] # format => [squareCoords], with each index being the moves it took to get to the desired square

    def currentPos(self):
        playerIndex = ''
        for row in maze:
            if 'A' not in row:
                continue
            playerIndex = [maze.index(row), row.index('A')]

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

    def squareCost(self, givenSquare, movesToSquare):
        return self.heuristic(givenSquare)+movesToSquare

    def getAvailableSquares(self):
        current_row, current_col = self.currentPos()
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        goodSquares = []

        for row, column in directions:
            newRow, newCol = current_row + row, current_col + column

            if 0 <= newRow < len(maze) and 0 <= newCol < len(maze[newRow]):
                if maze[newRow][newCol] in self.goodChars:
                    goodSquares.append([newRow, newCol])

        return goodSquares

class BFS(Player):
    def __init__(self):
        super().__init__()
        self.exploredSquares.append([self.currentSquare])

    def move(self):
        for square in self.getAvailableSquares():
            if not any(square in inner_list for inner_list in self.exploredSquares) and square not in self.frontier:
                self.frontier.append(square)
                # perhaps we can add explored squares here too.

        maze[self.currentSquare[0]][self.currentSquare[1]] = '0'

        self.currentSquare = self.frontier[0]
        self.frontier.remove(self.currentSquare)
        maze[self.currentSquare[0]][self.currentSquare[1]] = 'A'

        self.exploredSquares.append([self.currentSquare])

        if self.checkGoalState():
            return True
        return False

class DFS(Player):
    def __init__(self):
        super().__init__()

    def play(self):
        pass

class A_Star(Player):
    def __init__(self):
        pass


def displayMaze(player):
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

    print('\nGoal Position:', goalPos)
    print('Current Position:', player.currentPos())
    print('Heuristic:', player.heuristic(player.currentPos()))
    print('Goal State:', player.checkGoalState())
    print('Squares to move too:', player.getAvailableSquares())

    print('\nExplored Squares: ')
    for square in player.exploredSquares:
        print(f'  - Square: {square}, Heuristic:')

def getGoalPos():
    for row in maze:
        if 'Z' not in row:
            continue
        return [maze.index(row), row.index('Z')]

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Opening the maze creating a lists of lists to represent
with open(mazeName, "r") as mazeFile:
    maze = [list(row.strip()) for row in mazeFile if '#' in row]
goalPos = getGoalPos() # Must be run instantly as the maze will change as the game is played

clearScreen()
playerBFS = BFS()
displayMaze(playerBFS)

while True:
    sleep(1)
    clearScreen()

    goalState = playerBFS.move()
    displayMaze(playerBFS)

    if goalState:
        break