import random
import time

# bits for grid drawing
gridSpace = " " * 14
gridLine = "#" * 14
grid=[]
taken=[0,1,2,3,4,5,6,7,8]
# circle pixel art
o = []
o.append("   oooooo   ")
o.append(" ooo    ooo ")
o.append("oo        oo")
o.append("oo        oo")
o.append(" ooo    ooo ")
o.append("   oooooo   ")
# cross pixel art
x = []
x.append("xx        xx")
x.append("  xx    xx  ")
x.append("    xxxx    ")
x.append("    xxxx    ")
x.append("  xx    xx  ")
x.append("xx        xx")

def topBottom():
    for n in range(6):
        for i in range(2):
            grid.append(gridSpace)
            grid.append("#")
        grid.append(gridSpace + "\n")
    return None

def line():
    for i in range(3):
        grid.append(gridLine)
    grid.append("##" + "\n")
    return None

def drawGrid():
    for i in range(2):
        topBottom()
        line()
    topBottom()
    return None

# o shape for circle x shape for cross
def circleCross(position, shape, mini):
    if position <= 2: 
        x = 0
    elif position <= 5: 
        x = 28
    else: 
        x = 56
    for i in range(0, 6):
        # Making sure newline does not get deleted
        # Spot is the corect place to put the shapes
        spot = ((position*2) + (i*5) + x)
        if "\n" in grid[spot]: 
            grid[spot] = " " + shape[i] + " \n"
        else: 
            grid[spot] = " " + shape[i] + " "
    taken[position] = mini
    return None

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
                print("x is the winner!")
                return True
            elif o == 3:
                print("o is the winner!")
                return True
            # Exits after one check for the diagonals
            if n >= 3: break
    # Check if the grid is full, if so then its a draw
    k = [k for k in taken if isinstance(k, int)]
    if not k: 
        print("It's a draw!")
        return None
    # No winner found
    return False
    
def computerInput(computer):
    if "x" in computer[0]: symbol = "x"
    else: symbol = "o"
    # Two of a kind? Take the third.
    # Rows, Columns, Diagonal TL to BR, Diagonal TR to BL. In that order
    for n in range(4):
        for i in range(3):
            start = [i*3, i, 0, 2]
            stop = [i*3+3, len(taken), len(taken), 8]
            step = [1, 3, 4, 2]
            x = taken[start[n]:stop[n]:step[n]].count("x")
            o = taken[start[n]:stop[n]:step[n]].count("o")
            if x == 2 and o == 0 or o == 2 and x == 0:
                # Updates grid
                g = [k for k in taken[start[n]:stop[n]:step[n]] if isinstance(k, int)]
                circleCross(g[0], computer, symbol)
                # Updates taken
                taken[start[n]:stop[n]:step[n]] = [symbol if isinstance(k, int) else k for k in taken[start[n]:stop[n]:step[n]]]
                return None
            # Exits after one check for the diagonals
            if n >= 3: break
        
    # Makes a random move otherwise
    array = []
    for i in range(9):
        if isinstance(taken[i], int):
            array.append(i)
    circleCross(random.choice(array), computer, symbol)
    return None

def userTurn(shape, user):
    position = None
    while position == None:
        position = input()
        # Ensures an int
        if not position.isdigit():
            position = None
            print("Must be a whole number!")
        position = int(position)
        # Ensures int is within grid
        if position > 9 or position < 1:
            position = None
            print("Must be 1 to 9!")
        # Ensures position is not taken
        elif not isinstance(taken[position-1], int):
            position = None
            print("Must be an empty space!")
    # Updates grid with choice
    circleCross(position-1, shape, user)
    # Prints new grid
    print("".join(grid))
    # Ends the program if there is a winner or a draw
    n = checkWinner()
    if n == True: return True
    elif n == None: return None
    else: return False

def computerTurn(computer):
    # Plays the computers turn
    computerInput(computer)
    # Waits for a bit
    time.sleep(2)
    # Prints new grid
    print("".join(grid))
    # Ends the program if there is a winner or a draw
    n = checkWinner()
    if n == True: return True
    elif n == None: return None
    else: return False

drawGrid()
print("Welcome to Tic-Tac-Toe!\nx Goes first.")
user = None
while not user == "x" and not user == "o":
    print("Are you x or o?")
    user = input()
    if user == "o": 
        shape, computer = o, x
    else: 
        shape, computer = x, o

print("".join(grid))
print("Line up 3 of your shape in any direction to win!\nPlease type a number to make a choice it looks like this:\n1 2 3\n4 5 6\n7 8 9")

while True:
    if user == "x":
        n = userTurn(shape, user)
        if n == True or n == None: break
        n = computerTurn(computer)
        if n == True or n == None: break
    else:
        n = computerTurn(computer)
        if n == True or n == None: break
        n = userTurn(shape, user)
        if n == True or n == None: break

print("Thanks for playing!")