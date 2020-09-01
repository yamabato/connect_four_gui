from random_player import random_alpha

if __name__ == "__main__":
    line = input()


    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("randomAlpha")
    elif line[:4] == "kifu":
        from board import ConnectFour

        kifu = line[5:-1]
        hand = 0 if line[-1]=="+" else 1

        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))
            print("msg " + str(x))
        print("drop",random_alpha(board,hand))
