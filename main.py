import argparse

# Mazename flag
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--mazename", required=True)
args = parser.parse_args()
mazeName = args.mazename


def currentPos():
    playerIndex = ''
    for row in maze:
        if 'A' not in row:
            continue
        playerIndex = str(maze.index(row)) + str(row.index('A'))

    return playerIndex

def getGoalPos():
    for row in maze:
        if 'Z' not in row:
            continue
        return str(maze.index(row)) + str(row.index('Z'))
    
def checkGoalState():
    if currentPos() == goalPos:
        return True
    return False

# Calculates the estimated closeness of any given square, ignoring hedges (obviously)
def heuristic(givenSquare):
    x1, y1 = map(int, givenSquare)
    x2, y2 = map(int, goalPos)
    return abs(x2-x1) + abs(y2-y1)


# Opening the maze creating a lists of lists to represent
with open(mazeName, "r") as mazeFile:
    maze = [list(row.strip()) for row in mazeFile]
goalPos = getGoalPos()

print('Goal Position:', goalPos)
print('Current Position:', currentPos())
print('Heuristic:', heuristic(currentPos()))
maze[3][2] = 'A'
maze[5][0] = '0'
print('Current Position:', currentPos())
print('Heuristic:', heuristic(currentPos()))
maze[3][2] = '0'
maze[0][5] = 'A'
print('Current Position:', currentPos())
print('Heuristic:', heuristic(currentPos()))
print('Goal State:', checkGoalState())