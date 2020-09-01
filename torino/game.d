import std.stdio;

bool drop(byte x,ref byte[6][7] board,byte turn){
    if ((x < 0) || (x > 6)){
        return false;
    }

    byte y = -1;
    
    for (byte i;i<6;i++){

        if (board[x][i] != 0){
            break;
        }else{
            y = i;
        }
    }

    if (y==-1){
        return false;
    }

    board[x][y] = turn;

    return true;
}

byte judge(byte[6][7] board){
    byte[4][69] lines = [
        [0, 8, 16, 24], 
        [8, 16, 24, 32], 
        [16, 24, 32, 40],
        [1, 9, 17, 25], 
        [9, 17, 25, 33], 
        [17, 25, 33, 41],
        [2, 10, 18, 26], 
        [10, 18, 26, 34], 
        [3, 11, 19, 27], 
        [7, 15, 23, 31], 
        [15, 23, 31, 39], 
        [14, 22, 30, 38], 
        [3, 9, 15, 21], 
        [4, 10, 16, 22], 
        [10, 16, 22, 28], 
        [5, 11, 17, 23], 
        [11, 17, 23, 29], 
        [17, 23, 29, 35], 
        [6, 12, 18, 24], 
        [12, 18, 24, 30], 
        [18, 24, 30, 36], 
        [13, 19, 25, 31], 
        [19, 25, 31, 37], 
        [20, 26, 32, 38], 
        [0, 1, 2, 3], 
        [1, 2, 3, 4], 
        [2, 3, 4, 5], 
        [3, 4, 5, 6],
        [7, 8, 9, 10], 
        [8, 9, 10, 11], 
        [9, 10, 11, 12], 
        [10, 11, 12, 13], 
        [14, 15, 16, 17], 
        [15, 16, 17, 18], 
        [16, 17, 18, 19], 
        [17, 18, 19, 20], 
        [21, 22, 23, 24], 
        [22, 23, 24, 25], 
        [23, 24, 25, 26], 
        [24, 25, 26, 27],
        [28, 29, 30, 31], 
        [29, 30, 31, 32], 
        [30, 31, 32, 33], 
        [31, 32, 33, 34], 
        [35, 36, 37, 38], 
        [36, 37, 38, 39], 
        [37, 38, 39, 40], 
        [38, 39, 40, 41], 
        [0, 7, 14, 21], 
        [7, 14, 21, 28], 
        [14, 21, 28, 35], 
        [1, 8, 15, 22], 
        [8, 15, 22, 29], 
        [15, 22, 29, 36], 
        [2, 9, 16, 23], 
        [9, 16, 23, 30], 
        [16, 23, 30, 37], 
        [3, 10, 17, 24], 
        [10, 17, 24, 31], 
        [17, 24, 31, 38], 
        [4, 11, 18, 25], 
        [11, 18, 25, 32], 
        [18, 25, 32, 39], 
        [5, 12, 19, 26], 
        [12, 19, 26, 33], 
        [19, 26, 33, 40], 
        [6, 13, 20, 27], 
        [13, 20, 27, 34], 
        [20, 27, 34, 41], 
    ];
    byte[42] flat_board;
    byte[4] line;

    bool empty = false;

    for (byte x;x<7;x++){
        for (byte y;y<6;y++){
            flat_board[x*6+y] = board[x][y];

            if (board[x][y] == 0){
                empty = true;
            }
        }
    }

    for (byte i;i<lines.length;i++){
        for (byte j;j<4;j++){
            line[j] = flat_board[lines[i][j]];
        }

        if (line == [1,1,1,1]){
            return 1;
        }else if (line == [2,2,2,2]){
            return 2;
        }
    }
    
    if (empty){
        return 0;
    }else{
        return -1;
    }

}

byte[] legal_x(byte[6][7] board){
    byte[] legal;

    for (byte x;x<7;x++){
        if (board[x][0] == 0){
            legal.length++;
            legal[legal.length-1] = x;
        }
    }

    return legal;

}
