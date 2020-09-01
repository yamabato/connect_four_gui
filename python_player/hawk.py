from board import ConnectFour
from hawk_engine import hawk_engine

def hawk(line):
    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("HAWK")
    elif line[:4] == "kifu":

        kifu = line[5:-1]
        hand = 0 if line[-1] == "+" else 1
        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))

        print("drop",hawk_engine(board,hand))

if __name__ == "__main__":
    line = input()
    hawk(line)
