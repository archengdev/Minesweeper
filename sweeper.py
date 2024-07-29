from utils import *
import keyboard

time.sleep(0.7)

while True:
    # create board, then scan board, then make and use matrix to clear board
    board = init_board()
    scan(board)
    mat, dic = create_mat(board)
    find_mines(mat, board, dic)

    # pause to let animations finish
    time.sleep(0.7)
    if keyboard.is_pressed('q'):
        break