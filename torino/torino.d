import std.stdio;
import std.conv;
import std.random;

import game;

void torino_engine(byte[6][7] board,byte game_turn,ulong N){
    byte[] legal = legal_x(board);
    byte[] board_legal;
    byte x;
    byte result;
    ulong[byte] win;
    byte[6][7] game_board;


    for (byte i;i<legal.length;i++){
        for (ulong n;n<N;n++){

            game_board = board;
            drop(legal[i],game_board,game_turn);

            byte turn = game_turn == 1 ? 2 : 1;


            while (true){
                board_legal = legal_x(game_board);
                auto rnd = Random(unpredictableSeed);
                x = board_legal[uniform(0, board_legal.length, rnd)];

                drop(x,game_board,turn);

                result = judge(game_board);

                if (result==game_turn){
                    win[legal[i]]++;
                }

                if (result != 0){
                    break;
                }

                turn = turn == 1 ? 2:1;
            }
        }
    }

    ulong win_count = 0;
    byte[] choiced;
    ulong w;

    for (byte i;i<legal.length;i++){
        x = legal[i];
        w = win[x];
        
        if (w==win_count){
            choiced.length++;
            choiced[$-1] = x;
        }
        if(w>win_count){
            win_count = w;
            choiced = [x];
        }
    }

    auto rnd = Random(unpredictableSeed);
    byte choiced_x = choiced[uniform(0, choiced.length, rnd)];
    
    ulong win_c;
    for (x=0;x<7;x++){
        win_c = x in win ? win[x] : 0;
        writeln("msg ", x,": ", cast(float)win_c/cast(float)N*100,"%");
    }
    writeln("msg 選択: ",choiced_x);
    writeln("msg 予測勝率: ",cast(float)win[choiced_x]/cast(float)N*100,"%");
    writeln("drop ",choiced_x);
}

// 0:empty 1:BLACK 2:WHITE
// -1 DRAW
void torino(string input)
{
    if (input == "engine\n"){
        writeln("torino");
    }else if(input == "connectFour\n"){
        writeln("OK,ENGINE");
    }else if(input[0..4] == "kifu"){
        byte game_turn = input[$-2] == '+' ? 1 : 2;

        string kifu = input[5..$-1];
        byte[6][7] board;

        byte turn = 1;

        for (byte i;i<kifu.length;i++){
            byte x = cast(byte)(to!byte(kifu[i]) - 48);
            drop(x,board,turn);

            if (turn==1){
                turn = 2;
            }else{
                turn = 1;
            }
        }
        
        const ulong N = 500;
        torino_engine(board,game_turn,N);
    }
}

void main(){
    const string input = readln;

    torino(input);
}
