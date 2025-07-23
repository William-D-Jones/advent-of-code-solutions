import sys
from collections import deque

D = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
iD = { value: key for key, value in D.items() }
M1 = [1]
M2 = [-1, 1]

def energize(X, Beam):
    Seen = set()
    Eng = set()
    while len(Beam) > 0:

        # collect the current beam
        beam = Beam.popleft()
        if beam in Seen:
            continue
        else:
            Seen.add( beam )
        char = X[ beam[0] ][ beam[1] ]
        d = D[ beam[2] ]
        Eng.add( beam[0:2] )

        # determine the new direction for the beam
        if char == '.':
            sp = False
        elif char == '/':
            d = [ -d[1], -d[0] ]
            sp = False
        elif char == '\\':
            d = [ d[1], d[0] ]
            sp = False
        elif char == '-':
            if d[0] != 0:
                d = [ d[1], d[0] ]
                sp = True
            else:
                sp = False
        elif char == '|':
            if d[1] != 0:
                d = [ d[1], d[0] ]
                sp = True
            else:
                sp = False
        else:
            assert False

        # move the beams
        M = M2 if sp else M1
        for m in M:
            newr = beam[0] + m * d[0]
            newc = beam[1] + m * d[1]
            newd = iD[tuple(m * x for x in d)]
            if newr >= 0 and newr < nrow and newc >=0 and newc < ncol:
                Beam.append( (newr, newc, newd) )
    return len(Eng)

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# part 1
Beam = deque( [(0, 0, '>')] )
ans1 = energize(X, Beam)
print(ans1)

# part 2
Eng = []
for xr in range(nrow):
    for m in M2:
        if m == -1:
            xc = ncol -1
        elif m == 1:
            xc = 0
        else:
            assert False
        Beam = deque( [ (xr, xc, iD[(0, m)]) ] )
        Eng.append( energize(X, Beam) )
for xc in range(ncol):
    for m in M2:
        if m == -1:
            xr = nrow -1
        elif m == 1:
            xr = 0
        else:
            assert False
        Beam = deque( [ (xr, xc, iD[(m, 0)]) ] )
        Eng.append( energize(X, Beam) )
ans2 = max(Eng)
print(ans2)

