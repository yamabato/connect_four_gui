import copy

def delete(l,e):
    copied_l = copy.deepcopy(l)
    copied_l.remove(e)
    return copied_l

def league(players):
    games = sum([[(p1,p2) for p2 in delete(players,p1)] for p1 in players],[])
    
    return games




