import random
import time

taken=[0,1,2,3,4,5,6,7,8]

o = []
o.append("   oooooo   ")
o.append(" ooo    ooo ")
o.append("oo        oo")
o.append("oo        oo")
o.append(" ooo    ooo ")
o.append("   oooooo   ")

x = []
x.append("xx        xx")
x.append("  xx    xx  ")
x.append("    xxxx    ")
x.append("    xxxx    ")
x.append("  xx    xx  ")
x.append("xx        xx")

def createGridRow(grid):
    for _ in range(6):
        grid.append(list(" " * 14 + "#" + " " * 14 + "#" + " " * 14 + "\n"))

def createGridSeperator(grid):
    grid.append("#" * 44 + "\n")

def createEmptyGrid():
    grid = []
    createGridRow(grid)
    createGridSeperator(grid)
    createGridRow(grid)
    createGridSeperator(grid)
    createGridRow(grid)
    return grid

def populateGrid(grid):
    for i in range(len(taken)):
        if not isinstance(taken[i], int):
            if i <= 2: row = 0
            elif i <= 5: row = 7
            else: row = 14

            if i in [0,3,6]: col = 0
            elif i in [1,4,7]: col = 15
            else: col = 30

            if taken[i] == "x":
                for n in range(6):
                    grid[row + n][col+1:col+13] = x[n]
            else:
                for n in range(6):
                    grid[row + n][col+1:col+13] = o[n]

def printGrid(grid):
    for i in range(len(grid)):
        print("".join(grid[i]), end="")
    print("")

def printTerminalGrid():
    grid = createEmptyGrid()
    populateGrid(grid)
    printGrid(grid)

def checkWinner():
    # Rows, Columns, Diagonal TL to BR, Diagonal TR to BL. In that order
    for n in range(4):
        for i in range(3):
            start = [i*3, i, 0, 2]
            stop = [i*3+3, len(taken), len(taken), 8]
            step = [1, 3, 4, 2]
            x = taken[start[n]:stop[n]:step[n]].count("x")
            o = taken[start[n]:stop[n]:step[n]].count("o")
            if x == 3:
                return "x"
            elif o == 3:
                return "o"
            # Exits after one check for the diagonals
            if n >= 3: break
    # Check if the grid is full, if so then its a draw
    k = [k for k in taken if isinstance(k, int)]
    if not k: 
        return "draw"
    
def computerInput(computerShape):
    # Two of a kind? Take the third.
    # Rows, Columns, Diagonal Top Left to Bottom Right, Diagonal Top Right to Bottom Left. In that order
    for n in range(4):
        for i in range(3):
            start = [i*3, i, 0, 2]
            stop = [i*3+3, len(taken), len(taken), 8]
            step = [1, 3, 4, 2]
            x = taken[start[n]:stop[n]:step[n]].count("x")
            o = taken[start[n]:stop[n]:step[n]].count("o")
            if x == 2 and o == 0 or o == 2 and x == 0:
                # Updates taken
                taken[start[n]:stop[n]:step[n]] = [computerShape if isinstance(k, int) else k for k in taken[start[n]:stop[n]:step[n]]]
                return None
            # Exits after one check for the diagonals
            if n >= 3: break
        
    # Makes a random move otherwise
    array = []
    for i in range(9):
        if isinstance(taken[i], int):
            array.append(i)
    taken[random.choice(array)] = computerShape

def validateUserInput():
    position = None
    while position == None:
        position = input()
        # Ensures an int
        if not position.isdigit():
            position = None
            print("Must be a whole number!")
        # Ensures int is within grid
        elif 1 > int(position) > 9:
            position = None
            print("Must be 1 to 9!")
        # Ensures position is not taken
        elif not isinstance(taken[int(position)-1], int):
            position = None
            print("Must be an empty space!")
        else:
            return position
        
def userTurn(userShape):
    printInstructions()
    position = validateUserInput()
    # Updates grid with choice
    taken[int(position)-1] = userShape

def computerTurn(computerShape):
    # Plays the computers turn
    computerInput(computerShape)
    # Waits for a bit
    time.sleep(2)

def announceWinner(winner):
    if winner == "draw":
        print("Its a draw!")
        return True
    elif winner == "x" or winner == "o":
        print(winner, "is the winner!")
        return True

def printInstructions():
    print("Please type a number to make a choice it looks like this:")
    print(" 1 | 2 | 3")
    print("-----------")
    print(" 4 | 5 | 6")
    print("-----------")
    print(" 7 | 8 | 9")

print("Welcome to Tic-Tac-Toe!\nx Goes first.")
userShape = None
while not userShape == "x" and not userShape == "o":
    print("Are you x or o?")
    userShape = input()
    if userShape == "o": 
        computerShape = "x"
        userGoesNext = False
    else: 
        computerShape = "o"
        userGoesNext = True

while True:
    if userGoesNext:
        userTurn(userShape)
        userGoesNext = False
    else:
        computerTurn(computerShape)
        userGoesNext = True

    printTerminalGrid()
    turnResult = checkWinner()
    if turnResult:
        announceWinner(turnResult)
        break

print("Thanks for playing!")