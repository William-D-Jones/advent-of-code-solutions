import sys
from copy import deepcopy

def get_height(grid):
    Height = []
    for row in grid:
        for col,char in enumerate(row):
            if len(Height) <= col:
                Height.append(-1)
            if char == '#':
                Height[col] += 1
    return Height

# parsing
X = open(sys.argv[1], 'r').read().strip()
LK = []
for x in X.split('\n\n'):
    LK.append([list(l) for l in x.split('\n')])
L = []
K = []
nrow = len(LK[0])
ncol = len(LK[0][0])
for item in LK:
    if item[-1] == list('#' * ncol):
        K.append(item)
    elif item[0] == list('#' * ncol):
        L.append(item)
    else:
        assert False

# part 1
Height_Lock = [get_height(lock) for lock in L]
Height_Key = [get_height(key) for key in K]
ans1 = 0
for i,lock in enumerate(Height_Lock):
    for key in Height_Key:
        if all(key[i] + lock[i] <= 5 for i in range(ncol)):
            ans1 += 1
print(ans1) 
        
