import pyautogui
import time

import math
import numpy as np
import sympy as sympy

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

class Coord:
    x: int
    y: int

BOMB = -2
COVERED = -1
BLANK = 0

class Tile:
    def __init__(self):
        self.value = -1
        self.loc = Coord()
        self.checked = False
        self.covered = True
    loc: Coord
    value: int # -2 = bomb, -1 = covered, 0 = blank, number is number
    covered: bool
    checked: bool

# prompt user to choose mode
mode = pyautogui.prompt("easy_half or hard_full. press q to end")

# error if mode not supported
SUPPORTED_MODES = ['easy_half', 'hard_full']
if mode not in SUPPORTED_MODES:
    pyautogui.alert("Error: Mode not supported. Enter easy_half or hard_full")
    quit()


# set pixel locations. using 2560x1440, 125% scale
if mode == 'hard_full':
    # starting click:
    pyautogui.click(1300,800)

    LEN = 24
    HEIGHT = 20

    XOFFSET=(1654-905)/24 # distance between center of squares along x
    TRX = 905

    YOFFSET=31.2 #distance between center of squares along y
    TRY = 499 # y coord of top left of top left square

elif mode == 'easy_half':
    pyautogui.click(1900,800)

    LEN = 10
    HEIGHT = 8

    XOFFSET = (2201-1639)/10
    TRX  = 1639
    YOFFSET = (1037-588)/8
    TRY = 588

TRX_INIT = TRX + XOFFSET / 2
X_CHECK = int(XOFFSET / 3)
TRY_INIT = TRY + YOFFSET / 2 # y coord of center of top left square
Y_CHECK = int(YOFFSET / 3) # how far in each square to check

def print_board(board):
    """
    board: a 2D list of tiles
    prints a visual representation of the board using:
    'X' to represent a mine, '-' to represent an unknown tile,
    ' ' to represent a blank tile, and a number to represent a numbered tile
    """
    for j in range(HEIGHT):
        for i in range(LEN):
            val = board[j][i].value
            if val == BOMB:
                rep = 'X'
            elif val == COVERED:
                rep = '-'
            elif val == BLANK:
                rep = ' '
            else: 
                rep = val

            print(rep, end=' ')
        print()

def covered(r, g, b):
    """
    r,g,b: integer values representing rgb colors
    returns true if the rgb matches an uncovered tile (light/dark green)
    returns false otherwise
    """

    if ((r == 170 and g == 215 and b == 81) or 
        (r == 162 and g == 209 and b == 73)):
        return True
    else:
        return False


eps = 50  # determines how 'close' colors can be for a match to be found
def check_rgb(r,g,b):
    """
    r,g,b: integer values representing rgb colors
    determines if the rgb colors are close to colors for numbered tiles
    returns True, # if rgb color is close to the color of #
    returns False, 0 otherwise
    """

    p = [r,g,b]
    if math.dist(p,[59, 132, 205]) < eps:
        return True, 1
    elif math.dist(p,[56, 142, 60]) < eps:
        return True, 2
    elif math.dist(p,[212, 60, 57]) < eps:
        return True, 3
    elif math.dist(p,[153, 78, 161]) < eps:
        return True, 4
    elif math.dist(p,[255, 143, 0]) < eps :
        return True, 5
    else:
        return False, 0

def check_num(loc, img):
    """
    loc: (x,y), a tuple of integers representing a pixel location
    img: a PIL image file (such as a pyautogui screenshot)
    checks a range of pixels below target location to find the number
    returns the value of the number if found
    returns 0 if no valid number found
    """

    x = loc[0]
    y = loc[1]
    down = y + Y_CHECK

    # iterate over a range of pixels
    for j in range(y, down):
        # get and set rgb values
        color = img.getpixel(((x,j)))
        r = color[0]; g = color[1]; b = color[2]

        # see if rgb values are similar to a number's color
        found, val = check_rgb(r,g,b)

        # return if a match is found
        if found:
            return val
        
    # no match found
    return 0

# initialize board with coords (a 2D array of Tiles)
def init_board():
    """
    returns a board, a 2D array of tiles, with each tile having its location
    set to the correct pixel location
    """

    # create the board
    board = [[Tile() for i in range(LEN)] for j in range(HEIGHT)]

    # update locations
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            tile.loc.x = int(TRX_INIT + i*XOFFSET)
            tile.loc.y = int(TRY_INIT + j*YOFFSET)
    return board

def check_square_loc(board,x,y):
    # unused, will move cursor to the screen location of a tile
    pyautogui.moveTo(board[y][x].loc.x, board[y][x].loc.y)

def scan(board):
    """
    takes a board object and updates tile info based on the game on screen
    returns the same board with updated tiles
    """

    # take screenshot of board
    # checking screenshots is ~100-1000x faster than making checks to the screen
    img = pyautogui.screenshot()

    # loop over all tiles
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]

            # if tile is not covered, or is a bomb, no need to check again
            if not tile.covered or tile.value == BOMB:
                continue

            # get rgb color of the tile
            loc = [tile.loc.x, tile.loc.y]
            color = img.getpixel(((int(loc[0]), int(loc[1]))))
            r = color[0]; g = color[1]; b = color[2]

            # check if tile is still covered, if not, update info
            if not covered(r,g,b):
                tile.covered = False
                num = check_num(loc, img)
                board[j][i].value = num
    # return board

def get_neighbors(i,j):
    """
    i,j: integers
    for a tile in the ith column and jth row (0-indexing), returns the valid
    x,y pairs for the 8 neighboring tiles
    """

    ret = []

    # set the range of x based on i
    # if i is on an edge, only go up to the edge
    if i == 0:
        start_x = 0
        end_x = i+1
    elif i == LEN-1:
        start_x = i-1
        end_x = i
    else:
        start_x = i-1
        end_x = i+1

    # set the range of y based on j
    if j == 0:
        start_y = j
        end_y = j+1
    elif j == HEIGHT-1:
        start_y = j-1
        end_y = j
    else:
        start_y = j-1
        end_y =j+1

    # add all valid x,y pairs to 
    for y in range(start_y, end_y+1):
        for x in range(start_x, end_x+1):
            if not (x == i and y == j):
                ret.append((x,y))
    
    return ret

#takes a board and returns matrix for unknown squares in ROE form, and dictionary of values
def create_mat(board):
    """
    board: 2D array of tiles
    creates a dictionary to map tiles on the board to columns in a matrix.
    goes over the whole board, and for each numbered square, adds a row to a
    matrix with total number of mines (the number) in the last column, and
    a 1 in each column for each adjacent, uncovered tile (according to the map)
    returns the matrix in RREF form, and the dictionary
    """

    # dic: a dictionary that maps x,y locations on the board to unique indices
    # each tile in the dic will be 
    dic = {} 
    idx = 0
    
    # first create the dictionary by looping over all tiles, and adding an 
    # uncovered tile to the dic if it is adjacent to a numbered tile
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            val = tile.value

            # we only want numbered tiles
            if val < 1:
                continue

            # for each numbered tile, add all adjacent covered tiles
            adj = get_neighbors(i,j)    # get list of adjacent tiles
            for (x,y) in adj:
                # only add if covered
                if board[y][x].value == COVERED:
                    if (x,y) not in dic:
                        dic[(x,y)] = idx
                        idx += 1  # increment idx so each tile is unique
    
    # initialize matrix according to how many covered tiles are in the dic
    mat_len = len(dic) + 1
    mat = np.empty((0,mat_len))

    # loop over all tiles again
    for j in range(HEIGHT):
        for i in range(LEN):
            tile = board[j][i]
            val = tile.value

            # only want numbered tiles
            if val < 1:
                continue

            # get adjacent tiles, initialize row represnting info from the tile
            adj = get_neighbors(i,j)
            row = [0 for i in range(mat_len)]

            for (x,y) in adj:
                if (x,y) in dic:
                    # if tile is in dic, it is unknown, so set that col to 1
                    row[dic[(x,y)]] = 1
            
            # final column represents number of tile
            row[-1] = val

            # add the row to the matrix
            mat = np.vstack([mat,row])

    # return the matrix in rref form and the dictionary
    # rref: numpy mat -> sympy mat -> rref sympy mat -> rref numpy mat
    return np.array(sympy.Matrix(mat).rref()[0]).astype(np.float64), dic


def get_key(val, dic):
    # gets the loc in an x,y pair fron dic using the value
    for key, value in dic.items():
        if val == value:
            return key[0], key[1]
        
# takes ref matrix, board and dictionary to get mines from matrix, sets board values accordingly
def find_mines(mat, board, dic):
    """
    mat: RREF matrix
    board: 2D array of tiles
    dic: map of matrix column number to x,y position in the board
    gets the clear tiles from the matrix, and clicks on them
    """
    _, ncols = mat.shape

    # save clear tiles
    clear = []

    # logic from massaioli.wordpress.com/2013/01/12/solving-minesweeper-with-matricies/
    for row in mat:
        val = row[-1]
        maxv = 0
        minv = 0

        # figure out max and min vals for each row
        for i in range(ncols-1):
            if row[i] > 0: maxv += row[i]
            elif row[i] < 0: minv += row[i]

        if val == maxv:
            # all +ve numbers are mines, -ve numbers are not
            for i in range(ncols-1):
                if row[i] < 0: clear.append(i)

        elif val == minv:
            # all +ve numbers are not mines, -ve numbers are
            for i in range(ncols-1):
                if row[i] > 0: clear.append(i)


    # get pixel location of, and click all the clear squares
    clear = list(dict.fromkeys(clear))
    for i in clear:
        x,y = get_key(i, dic)
        tile = board[y][x]
        pyautogui.click(tile.loc.x,tile.loc.y)
