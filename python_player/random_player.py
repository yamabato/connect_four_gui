import random
import sys
import os

from check import check

def random_player(board):
    return random.choice(board.legal_x())

def random_alpha(board,hand):
    x, option = check(board,hand)

    if x != -1:
        return x

    if option:
        return random.choice(option)
    else:
        legal = board.legal_x()

        if legal:
            return random.choice(legal)
        else:
            return -1

if __name__ == "__main__":
    line = input()


    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("randomPlayer")
    elif line[:4] == "kifu":
        from board import ConnectFour

        kifu = line[5:-1]

        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))
            print("msg " + str(x))
        print("drop",random_player(board))
