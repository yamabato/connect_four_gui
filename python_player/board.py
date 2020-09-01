# encoding:utf-8


class ConnectFour:

    def __init__(self):
        self.board = [[0 for j in range(6)] for i in range(7)]
        self.kifu = []
        self.turn = 0

        self.lines = [
            [0, 8, 16, 24, 32, 40],
            [1, 9, 17, 25, 33, 41],
            [2, 10, 18, 26, 34],
            [3, 11, 19, 27],
            [7, 15, 23, 31, 39],
            [14, 22, 30, 38],
            [3, 9, 15, 21],
            [4, 10, 16, 22, 28],
            [5, 11, 17, 23, 29, 35],
            [6, 12, 18, 24, 30, 36],
            [13, 19, 25, 31, 37],
            [20, 26, 32, 38],
            [0, 1, 2, 3, 4, 5, 6],
            [7, 8, 9, 10, 11, 12, 13],
            [14, 15, 16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25, 26, 27],
            [28, 29, 30, 31, 32, 33, 34],
            [35, 36, 37, 38, 39, 40, 41],
            [0, 7, 14, 21, 28, 35],
            [1, 8, 15, 22, 29, 36],
            [2, 9, 16, 23, 30, 37],
            [3, 10, 17, 24, 31, 38],
            [4, 11, 18, 25, 32, 39],
            [5, 12, 19, 26, 33, 40],
            [6, 13, 20, 27, 34, 41],
        ]

        self.sign = {0: "-", 1: "O", 2: "X"}
    
    def __repr__(self):
        self.show()
    def drop(self, x):
        if all(self.board[x]):
            return False

        self.board[x][self.board[x].count(0) - 1] = 2 if self.turn%2 else 1
        self.turn += 1
        self.kifu.append(x)

        return True

    def judge(self):
        board_flat = []
        for y in range(6):
            for x in range(7):
                board_flat.append(self.board[x][y])

        for l in self.lines:
            line = ""
            for n in l:
                line += str(board_flat[n])

            if "1111" in line:
                return 1
            elif "2222" in line:
                return 2
        return 0

    def legal_x(self):
        legal = filter(
                lambda n: n != -1,
                [-1 if all(self.board[x]) else x for x in range(7)])

        return list(legal)
