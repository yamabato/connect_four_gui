import random

def make_tournament(players):
    tournament = players

    l = len(tournament)
    if l == 2:
        return tournament

    return make_tournament([tournament[i:i+2] for i in range(0,l,2)])

