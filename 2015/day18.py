import sys
from copy import deepcopy

NEIGH = [ (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1) ]

def update_lights(X, corner = False):
    nrow = len(X)
    ncol = len(X[0])
    Out = [['' for r in range(nrow)] for c in range(ncol)]
    for r in range(nrow):
        for c in range(ncol):
            on = 0
            off = 0
            for dr, dc in NEIGH:
                nr = r + dr
                nc = c + dc
                if not (0<=nr<nrow and 0<=nc<ncol):
                    off += 1
                elif X[nr][nc] == '.':
                    off += 1
                elif X[nr][nc] == '#':
                    on += 1
                else:
                    assert False
            assert off + on == len(NEIGH)
            if X[r][c] == '#':
                if on == 2 or on == 3:
                    Out[r][c] = '#'
                else:
                    Out[r][c] = '.'
            elif X[r][c] == '.':
                if on == 3:
                    Out[r][c] = '#'
                else:
                    Out[r][c] = '.'
            else:
                assert False
            if corner and (r == 0 or r == nrow-1) and (c == 0 or c == ncol-1):
                Out[r][c] = '#'

    return Out

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]

# part 1
nrow = len(X)
ncol = len(X[0])
Out = deepcopy(X)
for _ in range(100):
    Out = update_lights(Out, corner = False)
ans1 = 0
for r in range(nrow):
    for c in range(ncol):
        if Out[r][c] == '#':
            ans1 += 1
print(ans1)

# part 2
nrow = len(X)
ncol = len(X[0])
Out = deepcopy(X)
Out[0][0] = '#'
Out[0][ncol-1] = '#'
Out[nrow-1][0] = '#'
Out[nrow-1][ncol-1] = '#'
for _ in range(100):
    Out = update_lights(Out, corner = True)
ans2 = 0
for r in range(nrow):
    for c in range(ncol):
        if Out[r][c] == '#':
            ans2 += 1
print(ans2)

