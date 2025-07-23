import sys

D = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
D2 = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

def extract_points(Inst):
    """
    Convert digging instructions into points.
    """
    Ver = []
    Di = []
    pos = (0,0)
    for x in Inst:
        xr, xc = pos
        dr, dc = D[ x[0] ]
        n = x[1]
        pos = (xr + n * dr, xc + n * dc)
        Ver.append(pos)
        Di.append( D[ x[0] ] )
    return Ver, Di

def get_area(Ver):
    """
    Use the Shoelace Formula and Pick's Theorem to calculate the area of a
    region enclosed by and including a dug border.
    """
    # The (row, column) coordinate of each point corresponds to an (x,y)
    # Cartesian coordinate (where x = column and y = row) at the center of
    # the point.

    A = 0 # the area enclosed by the (x,y) coordinates
    P = 0 # the perimeter of the shape

    for i in range(len(Ver)):
        if i < len(Ver)-1:
            j = i + 1
        else:
            j = 0
        # use the Shoelace Formula to calculate the area
        A += Ver[i][1] * Ver[j][0] - Ver[i][0] * Ver[j][1]
        # keep a running total of the perimeter
        P += abs(Ver[j][1] - Ver[i][1]) + abs(Ver[j][0] - Ver[i][0])

    # now, calculate the dug area using Pick's Theorem
    DA = abs(A // 2) + 1 - P // 2 + P
    return DA
    
# parsing
X0 = [ l.strip() for l in open(sys.argv[1], 'r') ]
X1 = []
X2 = []
for x in X0:
    d, n, c = x.split()
    X1.append( (d, int(n)) )
    d2 = D2[ int(c[-2:-1]) ]
    n2 = int(c[2:-2], 16)
    X2.append( (d2, n2) )

# part 1
Ver, Di = extract_points(X1)
ans1 = get_area(Ver)
print(ans1)

# part 2
Ver, Di = extract_points(X2)
ans2 = get_area(Ver)
print(ans2)

