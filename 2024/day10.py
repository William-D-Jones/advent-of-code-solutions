import sys
from collections import defaultdict
from copy import deepcopy

# parsing
X = [ list(map(int, list(l.strip()))) for l in open(sys.argv[1], 'r') ]
TH = set()
for i,R in enumerate(X):
    for j,C in enumerate(R):
        if C == 0:
            TH.add((i,j))

# parts 1 and 2
TT = dict()
for th in TH:
    Trail = defaultdict(int)
    Trail[th] = 1
    while not all(X[coord[0]][coord[1]] == 9 for coord in Trail.keys()):
        assert len(Trail) > 0
        Step = defaultdict(int)
        for coord in Trail.keys():
            height = X[coord[0]][coord[1]]
            if height == 9:
                continue
            # step up
            if 0 < coord[0] and X[coord[0]-1][coord[1]] == height+1:
                Step[ (coord[0]-1, coord[1]) ] += Trail[coord]
            # step down
            if coord[0] < len(X)-1 and \
            X[coord[0]+1][coord[1]] == height+1:
                Step[ (coord[0]+1, coord[1]) ] += Trail[coord]
            # step left
            if 0 < coord[1] and X[coord[0]][coord[1]-1] == height+1:
                Step[ (coord[0], coord[1]-1) ] += Trail[coord]
            # step right
            if coord[1] < len(X[0])-1 and \
            X[coord[0]][coord[1]+1] == height+1:
                Step[ (coord[0], coord[1]+1) ] += Trail[coord]
        Trail = deepcopy(Step)
    TT[th] = Trail
ans1 = 0
ans2 = 0
for th in TT.keys():
    ans1 += len(TT[th].keys())
    ans2 += sum(TT[th].values())
print(ans1)
print(ans2)


