from board import ConnectFour
from swallow import swallow_engine
from random_player import random_player,random_alpha

def swallow_light(line):
    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("swallowLight")
    elif line[:4] == "kifu":

        kifu = line[5:-1]
        hand = 0 if line[-1] == "+" else 1
        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))

        print("drop",swallow_engine(board,hand,random_alpha,20,False,True))

if __name__ == "__main__":
    line = input()
    swallow_light(line)
