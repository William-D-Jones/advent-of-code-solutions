import sys

def hex_dist(r,c):
    r_diag = abs(r * 2)
    c_diag = abs(c)
    n_diag = int( min(r_diag, c_diag) )
    r_rem = int( (abs(r)-n_diag / 2) * 2 )
    c_rem = abs(c)-n_diag
    dist = n_diag + max(r_rem, c_rem)
    return dist

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split(',')

# Impose an (x,y) coordinate system on the hexagons, where we track the center
# of each hexagon.

# parts 1 and 2
r, c = 0, 0
Dist = []
for x in X:
    if x == 'n':
        r -= 1
    elif x == 'ne':
        r -= 0.5
        c += 1
    elif x == 'se':
        r += 0.5
        c += 1
    elif x == 's':
        r += 1
    elif x == 'sw':
        r += 0.5
        c -= 1
    elif x == 'nw':
        r -= 0.5
        c -= 1
    else:
        assert False
    Dist.append(hex_dist(r,c))
ans1 = hex_dist(r,c)
print(ans1)
ans2 = max(Dist)
print(ans2)

