import argparse
import os
from time import sleep
from random import shuffle

timeDelay = None

# Mazename flag
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--mazename', help='The path to the maze txt file', required=True)
parser.add_argument('-a', '--algorithm', help='The search algorithm you wish to use: bfs, dfs, gbfs, a*', required=True)
parser.add_argument('-d', '--delay', help='Time delay per-move in seconds -> if you do not wish to use a delay, do not use this flag')

args = parser.parse_args()

MAZE_NAME = args.mazename
ALGORITHM = args.algorithm
if args.delay != None: timeDelay = float(args.delay)


class Player:
    def __init__(self):
        self.frontier = []
        self.currentSquare = self.currentPos()
        self.exploredSquares = [] # All the explored squares
        self.knownSquares = [[]] # format => [[squareCoords1], [squareCoords2]], with each index being the moves it took to get to the desired square
        self.exploredSquares.append(self.currentSquare)
        self.knownSquares[0].append(self.currentSquare)
        self.paths = [] # A list of lists, containing the different sequences of moves that we have made. The sequence at index 0 is the current/best one.
        self.paths.append([self.currentSquare])

    def currentPos(self):
        playerIndex = ''
        for row in maze:
            if 'A' not in row:
                continue
            playerIndex = [maze.index(row), row.index('A')]
            break

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

    def squareCost(self, givenSquare):
        moves = 0
        for squares in self.knownSquares:
            if givenSquare in squares:
                movesToSquare = moves
                break
            moves += 1

        return self.heuristic(givenSquare)+movesToSquare

    def getAvailableSquares(self, square):
        goodChars = ['0', 'Z', 'A']
        currentRow, currentCol = square
        directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        goodSquares = []

        for row, column in directions:
            newRow, newCol = currentRow + row, currentCol + column

            if 0 <= newRow < len(maze) and 0 <= newCol < len(maze[newRow]):
                if maze[newRow][newCol] in goodChars:
                    goodSquares.append([newRow, newCol])

        return goodSquares

    def addKnownSquare(self, square):
        moves = 0
        for avaSquare in self.getAvailableSquares(square):
            count = 0
            for i in self.knownSquares:
                count += 1
                if avaSquare in i:
                    moves = count
                    break

        if len(self.knownSquares) <= moves:
            self.knownSquares.append([])

        self.knownSquares[moves].append(square)

    def addToFrontier(self):
        avaSquares = self.getAvailableSquares(self.currentPos())
        shuffle(avaSquares)

        for square in avaSquares:
            if square not in self.exploredSquares and square not in self.frontier:
                self.frontier.append(square)
                self.addKnownSquare(square)

        if not self.frontier:
            return True

        maze[self.currentSquare[0]][self.currentSquare[1]] = '0'

        return self.goalStateReachable()

    def goalStateReachable(self):
        if goalPos in self.frontier:
            self.currentSquare = goalPos
            self.cleanUp()
            return True
        return False

    def addToPaths(self, squareMovingTo):
        for square in self.getAvailableSquares(squareMovingTo): # Iterate through the squares next to the square we are about to move to
            sequenceTrack = 0 # Used to track which sequence we're on, allowing us to use this as an index

            for squares in self.paths: # Iterate through the sequences in self.paths
                if square in squares:
                    currentCorrectPath = self.paths[sequenceTrack]
                    currentCorrectPath = currentCorrectPath[:currentCorrectPath.index(square)+1] # We only want the sequence up to where the square is
                    self.paths.insert(0, currentCorrectPath) # Insert at 0, as it is the best
                    self.paths[0].append(squareMovingTo)
                    break # Our work here is done...

                sequenceTrack += 1

    def cleanUp(self):
        self.frontier.remove(self.currentSquare)
        maze[self.currentSquare[0]][self.currentSquare[1]] = 'A'

        self.exploredSquares.append(self.currentSquare)

    # Only to be called at the end of solving
    def showPath(self):
        localMaze = maze
        isGoalState = self.checkGoalState()

        for square in self.exploredSquares:
            localMaze[square[0]][square[1]] = '?'
        if isGoalState:
            for square in self.paths[0]:
                localMaze[square[0]][square[1]] = '!'
            localMaze[goalPos[0]][goalPos[1]] = 'A'
        else:
            localMaze[self.paths[0][-1][0]][self.paths[0][-1][1]] = 'A' # If no solution, leave 'A' at the last square it was at

        displayMaze(self, localMaze)

# Breadth-first search
class BFS(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        if self.addToFrontier(): return True

        self.addToPaths(self.frontier[0])
        self.currentSquare = self.frontier[0]

        self.cleanUp()
        return self.checkGoalState()

# Depth-first search
class DFS(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        if self.addToFrontier(): return True

        self.addToPaths(self.frontier[-1])
        self.currentSquare = self.frontier[-1]

        self.cleanUp()
        return self.checkGoalState()

# Greedy best-first search (follows heuristic only)
class GBFS(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        if self.addToFrontier(): return True

        bestSquare = []
        lowestSquareCost = float('inf')
        for square in self.frontier:
            cost = self.heuristic(square)
            if cost <= lowestSquareCost:
                bestSquare = square
                lowestSquareCost = cost

        self.addToPaths(bestSquare)
        self.currentSquare = bestSquare

        self.cleanUp()
        return self.checkGoalState()

class A_Star(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        if self.addToFrontier(): return True

        bestSquare = []
        lowestSquareCost = float('inf')
        for square in self.frontier:
            cost = self.squareCost(square)
            if cost <= lowestSquareCost:
                bestSquare = square
                lowestSquareCost = cost

        self.addToPaths(bestSquare)
        self.currentSquare = bestSquare

        self.cleanUp()
        return self.checkGoalState()


def displayMaze(player, mazeArr):
    clearScreen()
    for row in mazeArr:
        for char in row:
            match char:
                case '#':
                    print("\033[31m#\033[0m", end=' ') # '#' -> red
                case '0':
                    print("0", end=' ') # '0' -> white/normal terminal colour
                case 'A':
                    print("\033[35mA\033[0m", end=' ') # 'A' -> purple
                case 'Z':
                    print("\033[34mZ\033[0m", end=' ') # 'Z' -> blue
                case '?':
                    print("\033[33m0\033[0m", end=' ') # '0' -> orange
                case '!':
                    print("\033[32m0\033[0m", end=' ') # '0' -> green

        print() # Create a new line after every row

    print('\nGoal Position:', goalPos)
    print('Current Position:', player.currentPos())
    print('Heuristic:', player.heuristic(player.currentPos()))
    print('Goal State:', player.checkGoalState())
    print('Squares to move too:', player.getAvailableSquares(player.currentPos()))

def getGoalPos():
    for row in maze:
        if 'Z' not in row:
            continue
        return [maze.index(row), row.index('Z')]

def getTotalAvaSquares():
    totalAvaSquares = 0
    for row in maze:
        for char in row:
            if char == '0' or char == 'Z':
                totalAvaSquares += 1
    return totalAvaSquares

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Opening the maze creating a lists of lists to represent
with open(MAZE_NAME, "r") as mazeFile:
    maze = [list(row.strip()) for row in mazeFile if '0' in row or '#' in row]
goalPos = getGoalPos() # Must be run instantly as the maze will change as the game is played
totalAvaSquares = getTotalAvaSquares()


match ALGORITHM.lower():
    case 'bfs':
        player = BFS()
        displayMaze(player, maze)
    case 'dfs':
        player = DFS()
        displayMaze(player, maze)
    case 'gbfs':
        player = GBFS()
        displayMaze(player, maze)
    case 'a*':
        player = A_Star()
        displayMaze(player, maze)

while True:
    goalState = player.move()

    if timeDelay:
        sleep(timeDelay)
        displayMaze(player, maze)

    if goalState:
        player.showPath()

        lenExploredSquares = len(player.exploredSquares)-1
        if player.checkGoalState:
            print(f'\nExploration Efficiency: {lenExploredSquares}/{totalAvaSquares} ({round(((lenExploredSquares)/totalAvaSquares*100), 1)}%)')
        else:
            print('\nNo solution!')
        break

print()