import sys
import math
# from copy import deepcopy
# from collections import defaultdict
# import re

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

Time = [int(x) for x in X[0].split()[1:]]
Distance = [int(x) for x in X[1].split()[1:]]

Wins = []
for i,time in enumerate(Time):
    wins = 0
    for j in range(time):
        travel = (time - j) * j
        if travel > Distance[i]:
            wins += 1
    Wins.append(wins)
ans = 1
for win in Wins:
    ans = ans * win
print(ans)

time = int(''.join(X[0].split()[1:]))
distance = int(''.join(X[1].split()[1:]))
root1 = math.sqrt(-distance + (time / 2) ** 2) + (time / 2)
root2 = -math.sqrt(-distance + (time / 2) ** 2) + (time / 2)
tmin = math.ceil(min(root1, root2))
tmax = math.floor(max(root1, root2))
print(tmax - tmin + 1)

