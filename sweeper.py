from utils import *
import cProfile


# pyautogui.alert("Click OK to start")
# pyautogui.click(1300,800)
# time.sleep(0.3)

# def foo():
#     board = init_board()
#     board = scan(board)

# cProfile.run('foo()')

# board = init_board()
# board = scan(board)
# ref, mat, dic = create_mat(board)
# find_mines(ref, mat, board, dic)
# print(ref)



# print(mat)
# print(dic)
# for i in mat:
#     if i[46] != 0: 
#         print(i)
#         # ffind_mines(i)
#         pass

# print(dic[(1,5)])
# find_mines(mat, board, dic)
# board = init_board()

for i in range(50):
    # pyautogui.screenshot(str(i) + '.png')
    board = init_board()
    scan(board)
    # print()
    print_board(board)
    # print()
    mat, dic = create_mat(board)
    print(mat, dic)
    find_mines(mat, board, dic)
    pyautogui.moveTo(30,30)
    time.sleep(0.9)


#TODO: cut off complete squares, include regular echelon matrix for some situations?