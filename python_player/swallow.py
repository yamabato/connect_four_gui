import random
import copy

from board import ConnectFour
from check import check
from random_player import random_player,random_alpha


def swallow_engine(board, hand,f,trials,do_check,print_info):
    if do_check:
        check_x, option = check(board, hand)
        if not option:
            return board.legal_x()[0]
    else:
        check_x = -1
        option = board.legal_x()

    legal = option
    original_board = copy.deepcopy(board.board)

    wins = {k:0 for k in legal}

    player = f

    for x in legal:
        for i in range(trials):
            board.board = copy.deepcopy(original_board)
            board.turn = hand

            board.drop(x)

            while True:
                if all(map(all,board.board)):
                    break

                board.drop(player(board,board.turn%2))

                result = board.judge()
                if result == 1:
                    if hand == 0:
                        wins[x] += 1
                    break
                elif result == 2:
                    if hand == 1:
                        wins[x] += 1
                    break

    board.board = original_board
    board.turn = hand

    choiced = [-1,[]]

    for x in wins.keys():
        value = wins[x]
        if choiced[0] < value:
            choiced = [value,[x]]
        elif choiced[0] == value:
            choiced[1].append(x)

    choiced_x = -1

    if check_x != -1:
        choiced_x = check_x
    elif choiced[1]:
        choiced_x = random.choice(choiced[1])
    else:
        if legal:
            choiced_x = random.choice(legal)
        else:
            return -1

    #情報表示部
    if print_info:
        print("msg",("先手番" if hand == 0 else "後手番"))
        [print("msg ",str(k+1)+": "+str(round(float(wins[k]) / float(trials) * 100,2))+"%\n") for k in wins.keys()]
        print("msg","選択:",choiced_x+1)
        print("msg","想定勝率:", round((float(wins[choiced_x])/float(trials))*100,2),"%\n")

    return choiced_x


def swallow(line):
    if line == "connectFour":
        print("OK,ENGINE")
    elif line == "engine":
        print("swallow")
    elif line[:4] == "kifu":

        kifu = line[5:-1]
        hand = 0 if line[-1] == "+" else 1
        board = ConnectFour()

        for x in kifu:
            board.drop(int(x))

        print("drop",swallow_engine(board,hand,random_alpha,100,True,True))

if __name__ == "__main__":
    line = input()
    swallow(line)
