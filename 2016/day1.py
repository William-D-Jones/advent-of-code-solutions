import sys

D = [ (1, 0), (0, -1), (-1, 0), (0, 1) ]

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split(', ')

# parts 1 and 2
r, c = (0, 0)
dr, dc = D[0]
Seen = set( (r,c) )
Pos2 = None
for x in X:
    dx = x[0]
    num = int(x[1:])
    if dx == 'L':
        dr, dc = D[ (D.index( (dr,dc) ) - 1) % len(D) ]
    elif dx == 'R':
        dr, dc = D[ (D.index( (dr,dc) ) + 1) % len(D) ]
    else:
        assert False
    for i in range(num):
        r += dr
        c += dc
        if (r,c) in Seen and Pos2 is None:
            Pos2 = (r,c)
        else:
            Seen.add( (r,c) )
ans1 = abs(r) + abs(c)
print(ans1)
ans2 = abs(Pos2[0]) + abs(Pos2[1])
print(ans2)

