

def check(board, hand):
    my_sign = "1" if hand == 0 else "2"
    enemy_sign = "2" if hand == 0 else "1"

    my_check = {
        "0" + my_sign * 3: 0,
        my_sign + "0" + my_sign * 2: 1,
        my_sign * 2 + "0" + my_sign: 2,
        my_sign * 3 + "0": 3,
    }

    enemy_check = {
        "0" + enemy_sign * 3: 0,
        enemy_sign + "0" + enemy_sign * 2: 1,
        enemy_sign * 2 + "0" + enemy_sign: 2,
        enemy_sign * 3 + "0": 3,
    }

    enemy_early_check = {
        "00" + enemy_sign * 2 + "0": 1,
        "0" + enemy_sign * 2 + "00": 3,
        "0" + enemy_sign + "0" + enemy_sign + "0": 0,
    }

    diagonal_lines = {
        (21, 15, 9, 3):          (0, 3, -1),
        (28, 22, 16, 10, 4):     (0, 4, -1),
        (35, 29, 23, 17, 11, 5): (0, 5, -1),
        (36, 30, 24, 18, 12, 6): (1, 5, -1),
        (37, 31, 25, 19, 13):    (2, 5, -1),
        (38, 32, 26, 20):        (3, 5, -1),

        (0, 8, 16, 24, 32, 40):  (0, 0, 1),
        (1, 9, 17, 25, 33, 41):  (1, 0, 1),
        (2, 10, 18, 26, 34):     (2, 0, 1),
        (3, 11, 19, 27):         (3, 0, 1),
        (7, 15, 23, 31, 39):     (0, 1, 1),
        (14, 22, 30, 38):        (0, 2, 1),
    }

    option = board.legal_x()

    board_flat = []

    for y in range(6):
        for x in range(7):
            board_flat.append(board.board[x][y])

    # 勝てる時打つ方
    for x in range(7):
        line = "".join(map(str, board.board[x]))
        if "0" + my_sign * 3 in line:
            return x, option

    for y in range(6):
        line = ""
        for x in range(7):
            line += str(board.board[x][y])

        for check in my_check:
            if line.find(check) >= 0:
                x = line.find(check) + my_check[check]
                if y == board.board[x].count(0) - 1:
                    return x, option

    for l in diagonal_lines:
        line = ""
        for n in l:
            line += str(board_flat[n])

        for check in my_check:
            if line.find(check) >= 0:
                x = diagonal_lines[l][0] + line.find(check) + my_check[check]
                y = diagonal_lines[l][
                    1] + (line.find(check) + my_check[check]) * diagonal_lines[l][2]
                if y == 5 or (y < 4 and board.board[x][y + 1] != 0):
                    return x, option

    # 敵を止める方

    for x in range(7):
        line = "".join(map(str, board.board[x]))
        if "0" + enemy_sign * 3 in line:
            return x, option

    for y in range(6):
        line = ""
        for x in range(7):
            line += str(board.board[x][y])

        for check in enemy_check:
            if line.find(check) >= 0:
                x = line.find(check) + enemy_check[check]

                if y < 4 and board.board[x][y + 1] == 0 and board.board[x][y + 2] != 0:
                    if x in option:
                        option.remove(x)
                elif y == 4 and board.board[x][y + 1] == 0:
                    if x in option:
                        option.remove(x)

                if x in option and y == board.board[x].count(0) - 1:
                    return x, option

    for l in diagonal_lines:
        line = ""
        for n in l:
            line += str(board_flat[n])

        for check in enemy_check:
            if line.find(check) >= 0:
                x = diagonal_lines[l][0] + \
                    line.find(check) + enemy_check[check]
                y = diagonal_lines[l][
                    1] + (line.find(check) + enemy_check[check]) * diagonal_lines[l][2]

                if y < 4 and board.board[x][y + 1] == 0 and board.board[x][y + 2] != 0:
                    if x in option:
                        option.remove(x)
                elif y == 4 and board.board[x][y + 1] == 0:
                    if x in option:
                        option.remove(x)

                elif x in option and y == 5 or (y < 5 and board.board[x][y + 1] != 0):
                    return x, option

    for l in diagonal_lines:
        line = ""
        for n in l:
            line += str(board_flat[n])

        for check in enemy_early_check:
            if line.find(check) >= 0:
                x = diagonal_lines[l][0] + \
                    line.find(check) + enemy_early_check[check]
                y = diagonal_lines[l][
                    1] + (line.find(check) + enemy_early_check[check]) * diagonal_lines[l][2]

                if y < 5 and board.board[x][y + 1] == 0:
                    if x in option:
                        option.remove(x)

                elif x in option and y == 5 or (y < 5 and board.board[x][y + 1] != 0):
                    return x, option

    for y in range(6):
        line = ""
        for x in range(7):
            line += str(board.board[x][y])

        for check in enemy_early_check:
            if line.find(check) >= 0:
                x = line.find(check) + enemy_early_check[check]

                if y < 4 and board.board[x][y + 1] == 0 and board.board[x][y + 2] != 0:
                    if x in option:
                        option.remove(x)

                if x in option and y == board.board[x].count(0) - 1:
                    return x, option

    return -1, option


