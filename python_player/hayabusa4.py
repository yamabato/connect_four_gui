from board import ConnectFour
from hayabusa4_engine import hayabusa4_engine

def hayabusa(line):
    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("HAYABUSA")
    elif line[:4] == "kifu":

        kifu = line[5:-1]
        hand = 0 if line[-1] == "+" else 1
        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))

        print("drop",hayabusa4_engine(board,hand,5))

if __name__ == "__main__":
    line = input()
    hayabusa(line)
