from board import ConnectFour
from hawk_engine import hawkC_engine

def hawkC(line):
    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("hawkC")
    elif line[:4] == "kifu":

        kifu = line[5:-1]
        hand = 0 if line[-1] == "+" else 1
        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))

        print("drop",hawkC_engine(board,hand))

if __name__ == "__main__":
    line = input()
    hawkC(line)
