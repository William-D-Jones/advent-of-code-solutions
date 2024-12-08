import sys
from collections import defaultdict

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
dict_ant = defaultdict(list)
for i in range(len(X)):
    for j in range(len(X[0])):
        if X[i][j].isalnum():
            dict_ant[ X[i][j] ].append((i, j))
mapX = len(X)
mapY = len(X[0])

# parts 1 and 2
anod1 = set()
anod2 = set()
for freq in dict_ant.keys():
    for i,coord1 in enumerate(dict_ant[freq]):
        for j,coord2 in enumerate(dict_ant[freq][i+1:], start = i+1):
            stepX = coord2[0] - coord1[0]
            stepY = coord2[1] - coord1[1]
            ix_step = [0, 0]
            while not all(ix is None for ix in ix_step):
                if ix_step[0] is not None:
                    coorda1 = (coord1[0] - ix_step[0] * stepX, \
                    coord1[1] - ix_step[0] * stepY)
                    if 0 <= coorda1[0] < mapX and 0 <= coorda1[1] < mapY:
                        if ix_step[0] == 1:
                            anod1.add(coorda1)
                        anod2.add(coorda1)
                        ix_step[0] += 1
                    else:
                        ix_step[0] = None
                if ix_step[1] is not None:
                    coorda2 = (coord2[0] + ix_step[1] * stepX, \
                    coord2[1] + ix_step[1] * stepY)
                    if 0 <= coorda2[0] < mapX and 0 <= coorda2[1] < mapY:
                        if ix_step[1] == 1:
                            anod1.add(coorda2)
                        anod2.add(coorda2)
                        ix_step[1] += 1
                    else:
                        ix_step[1] = None
print(len(anod1))
print(len(anod2))

