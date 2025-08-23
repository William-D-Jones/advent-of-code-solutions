import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

d_win = { 'R': 'P', 'P': 'S', 'S': 'R' }
d_lose = { 'R': 'S', 'P': 'R', 'S': 'P' }
d_1 = { 'A': 'R', 'B': 'P', 'C': 'S' }
d_2 = { 'X': 'R', 'Y': 'P', 'Z': 'S' }
d_sc_shape = { 'R': 1, 'P': 2, 'S': 3 }

W = []
for p in X:
    G = p.split(' ')
    move1 = d_1[G[0]]
    move2 = d_2[G[1]]
    w = 0
    w += d_sc_shape[move2]
    if d_win[move1] == move2:
        w += 6
    elif move1 == move2:
        w += 3
    W.append(w)

print(sum(W))

W = []
for p in X:
    G = p.split(' ')
    move1 = d_1[G[0]]
    w = 0
    if G[1] == 'X':
        move2 = d_lose[move1]
    elif G[1] == 'Y':
        move2 = move1
        w += 3
    elif G[1] == 'Z':
        move2 = d_win[move1]
        w += 6
    w += d_sc_shape[move2]
    W.append(w)

print(sum(W))
