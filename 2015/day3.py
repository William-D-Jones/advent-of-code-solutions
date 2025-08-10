import sys

D = {'>': (0,1), 'v': (1,0), '<': (0,-1), '^': (-1,0)}

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
r = 0
c = 0
Seen1 = set( [(r,c)] )
for d in X:
    dr, dc = D[d]
    r += dr
    c += dc
    Seen1.add( (r,c) )
ans1 = len(Seen1)
print(ans1)

# part 2
r_santa = 0
c_santa = 0
r_robo = 0
c_robo = 0
Seen2 = set( [(0,0)] )
for i,d in enumerate(X):
    dr, dc = D[d]
    if i % 2 == 0: # santa moves
        r_santa += dr
        c_santa += dc
        Seen2.add( (r_santa,c_santa) )
    else: # robo-santa moves
        r_robo += dr
        c_robo += dc
        Seen2.add( (r_robo,c_robo) )
ans2 = len(Seen2)
print(ans2)
