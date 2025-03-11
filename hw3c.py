import typing
from typing import List

b = [['x', '-', 'x'],
     ['o', 'x', 'x'],
     ['o', 'x', 'o']]

def tic_tac_toe_checker(board: List[List]) -> str:
    for i in board:
        if i[0] ==  i[1] ==  i[2] and i[0] != '-':
            print(i[0]+ ' wins')

    for col in range(2):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '-':
            return f"{board[0][col]} wins!"

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '-':
        return f"{board[0][0]} wins!"

    if board[0][2] == board[1][1] == board[2][0] and board[2][0] != '-':
        return f"{board[0][2]} wins!"

    for i in board:
        if '-' in i:
            print("unfinished")
            break
        else:
            print("draw")
            break

tic_tac_toe_checker(b)

