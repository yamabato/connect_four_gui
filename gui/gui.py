import os
import json
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import filedialog
import subprocess
import time

import timeout_decorator
from league import *

from board import ConnectFour

def resign():
    end(1 if board.turn%2 else 2)

def send(msg, file_path):
    try:
        #print("SEND",msg.replace("\n","\\"), "->", file_path)
        output = subprocess.run([file_path],input=msg,stdout=subprocess.PIPE,text=True).stdout
        #print("GET", file_path, "->", output.replace("\n","\\"))
        return output
    except:
        print("ERROR",output)
        return -1

def register():
    file_path = filedialog.askopenfilename(initialdir = os.path.abspath(os.path.dirname(__file__)))
    
    try:
        name = get_engine_name(file_path)
    except:
        messagebox.showerror("コネクトフォーGUI", f"エンジンの登録に失敗しました\nファイル:{file_path}")
        return

    with open("engine.json",mode="r") as f:
        engines = json.load(f)

    engines[name] = file_path

    with open("engine.json",mode="w") as f:
        json.dump(engines,f)

    com_players[name] = file_path
    player1_combo["values"] = list(com_players.keys())
    player2_combo["values"] = list(com_players.keys())

    messagebox.showinfo("コネクトフォーGUI", f"エンジンの登録に成功しました\n\nエンジン名:{name}\nファイル:{file_path}")

def load_engins():
    with open("engine.json", mode="r") as f:
        engines = json.load(f)

    for engine in engines:
        file_path = engines[engine]
        try:
            name = get_engine_name(file_path)
            com_players[name] = file_path
        except:
            pass

@timeout_decorator.timeout(5)
def get_engine_name(file_path):
    if send("connectFour\n",file_path).replace("\n","")== "OK,ENGINE":
        name = send("engine\n",file_path).replace("\n","")
        if name == -1:
            raise
        return name
    else:
        raise

def edit_text(pos,text):
    text_area.configure(state="normal")
    text_area.insert(pos,text)
    text_area.configure(state="disable")

def delete_text():
    text_area.configure(state="normal")
    text_area.delete("1.0","end")
    text_area.configure(state="disable")

def com(player):
    output = send("kifu "+"".join(map(str,board.kifu))+("+" if board.turn%2==0 else "-"),player).split("\n")
    
    delete_text()
    for n,text in enumerate(output):
        if text[:3] == "msg":
            edit_text("end", text[4:]+"\n")
        elif text[:4] == "drop":
            x = text[-1]
            if x=="" or x not in "0123456":
                return -1
            else:
                return int(x)
    return -1

def start():
    global first,first_is_human,first_name,last,last_is_human,last_name

    delete_text()

    first = player1_combo.get()
    last = player2_combo.get()

    first_is_human = True
    last_is_human = True

    first_name = first
    last_name = last

    if first in com_players:
        first_is_human = False
        first = com_players[first]
    if last in com_players:
        last_is_human = False
        last = com_players[last]
    
    player_label.configure(text=f"{first_name}({'HUMAN' if first_is_human else 'COM'}) vs {last_name}({'HUMAN' if last_is_human else 'COM'})")

    player1_combo.configure(state="disable")
    player2_combo.configure(state="disable")
    
    board.__init__()
    show()

    if not first_is_human:
        move(com(first))

def end(winner):
    global win_player
    win_player = winner

    msg = "引き分け"
    if winner == 1:
        msg = "先手の勝利"
    elif winner == 2:
        msg = "後手の勝利"
    elif winner == -2:
        msg ="後手の勝利" if board.turn % 2 == 0 else "先手の勝利"

    turn_label.configure(text=msg)
    if popup:
        messagebox.showinfo("コネクトフォーGUI", msg)

    player1_combo.configure(state="normal")
    player2_combo.configure(state="normal")

def end_game():
    if messagebox.askyesno("コネクトフォーGUI", "ゲームを終了しますか?"):
        quit()
    else:
        messagebox.showinfo("コネクトフォーGUI", "中断しました")


def move(x):
    if x not in range(7):
        end(-2)

    board.drop(x)
    show()
    result = board.judge()

    if result != 0:
        end(result)
        return
    else:
        if board.turn == 42:
            end(-1)
            return
        else:
            pass

    if board.turn % 2 == 0 and not first_is_human:
        move(com(first))
    elif board.turn % 2 == 1 and not last_is_human:
        move(com(last))
    
def click(x):
    if x >= 0 and x <= 6:
        move(x)

def motion(x):
    if x < 0 or x > 6:
        return

    global mouse_x_id

    if mouse_x_id:
        canvas.delete(mouse_x_id)

    if (board.turn % 2 == 0 and first_is_human) or (board.turn % 2 == 1 and last_is_human):
        y = board.board[x].count(0) - 1 
        
        clr = "#b0c4de" if board.turn%2==0 else "#ffa07a"
        mouse_x_id = canvas.create_oval(x*50+5,y*50+5,x*50+45,y*50+45,fill=clr,width=0)

def leave():
    if mouse_x_id:
        canvas.delete(mouse_x_id)

def show():
    for y in range(6):
        for x in range(7):
            clr = "#f3f3f2"

            stone = board.board[x][y]

            gap = 0 if stone == 0 else 3

            if stone == 1:
                clr = "blue"
            elif stone == 2:
                clr = "red"
           
            canvas.create_oval(x*50+gap,y*50+gap,x*50+50-gap,y*50+50-gap,fill=clr,width=0)

    turn_label.configure(text=(f"先手({first_name})思考中..." if board.turn%2==0 else f"後手({last_name})思考中..."))
    tk.update()

def league_games():
    global game_N

    game_N = 1

    league_tk = Tk()
    league_tk.title("コネクトフォー リーグ")
    league_tk.geometry("200x300")

    choice_player = Listbox(league_tk,selectmode=MULTIPLE,width=100)
    choice_player.place(x=0,y=0)
    
    players_list = list(com_players.keys())
    for player in players_list:
        choice_player.insert("end",player)
    
    scroll = Scrollbar(league_tk,orient=VERTICAL)
    scroll.place(x=190,y=0)

    start_league_btn = Button(league_tk,text="リーグ開始",bg="blue",highlightbackground="blue",font=("",20),
        command=lambda :[start_league(league_tk,[players_list[i] for i in choice_player.curselection()])]
        )

    start_league_btn.place(x=0,y=175)

    game_N_entry = Entry(league_tk)
    game_N_entry.place(x=0,y=200)

    game_N_btn = Button(league_tk,text="設定",bg="cyan",highlightbackground="cyan",font=("",20),command=lambda:set_game_N(game_N_entry.get()))
    game_N_btn.place(x=0,y=230)

def set_game_N(inp):
    global game_N
    inp = inp.replace(" ","")

    if inp.isdigit():
        game_N = int(inp)



def start_league(league_tk,joined_players):
    global win_player,popup
    
    popup = False

    league_tk.destroy()

    if len(joined_players) < 2:
        return

    league_result_tk = Tk()
    league_result_tk.geometry("500x200")
    league_result_tk.title("コネクトフォーリーグ 結果")
   
    result = Text(league_result_tk,width=80,height=10,borderwidth=0,highlightthickness=0,font=("",15))
    result.pack(side=LEFT)
    result.configure(state="disable")

    scroll = Scrollbar(league_result_tk, orient=VERTICAL, command=result.yview)
    scroll.pack(side=RIGHT, fill=Y)

    result["yscrollcommand"] = scroll.set
    
    games = league(joined_players)
    games = sorted(games*game_N)
    
    win_count = {p:[0,0,0] for p in joined_players}

    d_l = len(str(len(games) // len(joined_players)))

    result.configure(state="normal")
    result.insert("end",f"対局数 1 / {len(games)}\n")
    result.insert("end",f"現在の対局 {games[0][0]} vs {games[0][1]} \n次の対局  {games[1][0]} vs {games[1][1]}\n\n")
    result.insert("end","\n".join([p+"(W:0,L:0,D:0,W-L:0,W-r:0%)" for p in joined_players]))
    result.configure(state="disable")

    for n,game in enumerate(games):
        player1_combo.set(game[0])
        player2_combo.set(game[1])
        start()
        
        if win_player == 1:
            win_count[game[0]][0] += 1
            win_count[game[1]][1] += 1
        elif win_player == 2:
            win_count[game[0]][1] += 1
            win_count[game[1]][0] += 1
        elif win_player == -1:
            win_count[game[0]][2] += 1
            win_count[game[1]][2] += 1
        win_player = 0
    
        result.configure(state="normal")
        result.delete("1.0","end")
        result.insert("end",f"対局数 {n+2 if n+1<len(games) else '-'} / {len(games)}\n")
        result.insert("end", f"現在の対局 {f'{games[n+1][0]} vs {games[n+1][1]}' if n<len(games)-1 else '-'}\n"+f"次の対局 {f'{games[n+2][0]} vs {games[n+2][1]}' if n<len(games)-2 else '-'}\n\n")
        result.insert("end","\n".join([p+ \
                f"(W:{str(win_count[p][0]).rjust(d_l)},L:{str(win_count[p][1]).rjust(d_l)},D:{str(win_count[p][2]).rjust(d_l)},W-L:{str(win_count[p][0]-win_count[p][1]).rjust(d_l+1)},W-r:{' 0.0'  if sum(win_count[p]) == 0 else str(round(win_count[p][0]/sum(win_count[p])*100,2)).rjust(4)}%)" 
                for p in sorted(joined_players,key=lambda x:-1 if sum(win_count[x]) == 0 else win_count[x][0]/sum(win_count[x]),reverse=True)]))
        result.configure(state="disable")

    popup = True

board = ConnectFour()
win_player = -1
popup = True
game_N = 1

tk = Tk()
tk.geometry("750x700")
tk.title("コネクトフォーGUI")
tk.resizable(0,0)

canvas = Canvas(tk,width=350,height=300,bg="#dddcd6")
canvas.place(x=75,y=100)

canvas.bind("<Button>",lambda e:click(e.x//50))
canvas.bind("<Motion>",lambda e:motion(e.x//50))
canvas.bind("<Leave>",lambda e:leave())
mouse_x_id = False

for y in range(6):
    for x in range(7):
        canvas.create_oval(x*50,y*50,x*50+50,y*50+50,fill="#f3f3f2",width=0)

situation_bar = ttk.Progressbar(tk,length=200)
situation_bar.place(x=150,y=80)
situation_bar.configure(value=50)

win_first_lbl = Label(tk,text="-%")
win_first_lbl.place(x=120,y=80)

win_last_lbl = Label(tk,text="-%")
win_last_lbl.place(x=355,y=80)

player_label = Label(tk,text="...",font=("",30))
player_label.place(x=0,y=0)

turn_label = Label(tk,text="先手番",font=("",30))
turn_label.place(x=75,y=40)

start_btn = Button(tk,text="対局開始",bg="blue",highlightbackground="blue",font=("",30),command=start)
start_btn.place(x=430,y=100)

resign_btn = Button(tk,text="投了",bg="green",highlightbackground="green",font=("",30),command=resign)
resign_btn.place(x=430,y=200)

quit_btn = Button(tk,text="終了",bg="red",highlightbackground="red",font=("",30),command=end_game)
quit_btn.place(x=600,y=370)


register_btn = Button(tk,text="エンジン登録", bg="purple",highlightbackground="purple",font=("",20),command=register)
register_btn.place(x=430,y=370)

league_btn = Button(tk,text="リーグ",bg="#ffa500",highlightbackground="#ffa500",font=("",30),command=league_games)
league_btn.place(x=430,y=250)

text_frame = Frame(tk,width=300,height=200,borderwidth=0,highlightthickness=0)
text_frame.place(x=75,y=400)

text_area = Text(text_frame,width=50,height=10,borderwidth=0,highlightthickness=0,font=("",20))
text_area.pack(side=LEFT)
text_area.configure(state="disable")

scroll = Scrollbar(text_frame, orient=VERTICAL, command=text_area.yview)
scroll.pack(side=RIGHT, fill="y")

text_area["yscrollcommand"] = scroll.set

com_players = {}
load_engins()

first = ""
last = ""

first_name = ""
last_name = ""

first_is_human = True
last_is_human = True

player1_combo = ttk.Combobox(tk, state="normal", width=20)
player1_combo["values"] = list(com_players.keys())
player1_combo.place(x=430, y=130)

player2_combo = ttk.Combobox(tk, state="normal", width=20)
player2_combo["values"] = list(com_players.keys())
player2_combo.place(x=430, y=160)

show()

tk.mainloop()
