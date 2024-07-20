from utils import *
import cProfile
import time

# help(init_board)
# time.sleep(0.5)
# def foo():
#     board = init_board()
#     board = scan(board)

# cProfile.run('foo()')
def ffind_mines(row):
    # nrows, ncols = mat.shape
    # print(nrows)
    ncols = len(row)

    mines = []
    clear = []

    # for row in mat:
    val = row[-1]
    maxv = 0
    minv = 0
    for i in range(ncols-1):
        if row[i] > 0: maxv += row[i]
        elif row[i] < 0: minv += row[i]
    if val == maxv:
        # all +ve numbers are mines, -ve numbers are not
        for i in range(ncols-1):
            if row[i] > 0: mines.append(i)
            elif row[i] < 0: clear.append(i)
    elif val == minv:
        # all +ve numbers are not mines, -ve numbers are
        for i in range(ncols-1):
            if row[i] > 0: clear.append(i)
            elif row[i] < 0: mines.append(i)
    
    print(mines)
    print(clear)

# board = init_board()
# board = scan(board)
# mat, dic = create_mat(board)
# print(mat)
# print(dic)
# for i in mat:
#     if i[46] != 0: 
#         print(i)
#         # ffind_mines(i)
#         pass

# print(dic[(1,5)])
# find_mines(mat, board, dic)

for i in range(25):
    # pyautogui.screenshot(str(i) + '.png')
    board = init_board()
    board = scan(board)
    print_board(board)
    mat, dic = create_mat(board)
    find_mines(mat, board, dic)
    pyautogui.moveTo(30,30)
    time.sleep(0.3)


#TODO: cut off complete squares, include regular echelon matrix for some situations?