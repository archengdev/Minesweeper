from utils import *
import cProfile
import time

pyautogui.alert("Click OK to start")
pyautogui.click(1300,800)
time.sleep(0.3)

# def foo():
#     board = init_board()
#     board = scan(board)

# cProfile.run('foo()')
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

for i in range(50):
    # pyautogui.screenshot(str(i) + '.png')
    board = init_board()
    board = scan(board)
    # print_board(board)
    roe, mat, dic = create_mat(board)
    find_mines(mat, board, dic)
    pyautogui.moveTo(30,30)
    time.sleep(0.3)


#TODO: cut off complete squares, include regular echelon matrix for some situations?