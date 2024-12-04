import sys
import math
from copy import deepcopy
from collections import defaultdict
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
ans = 0
for x in range(len(X)):
    for y in range(len(X[x])):
        if X[x][y:y+1] == 'X':
            if X[x][y:y+4] == 'XMAS':
                ans += 1
            if x <= len(X[x]) - 4 and X[x+1][y:y+1] == 'M' and X[x+2][y:y+1] == 'A' and X[x+3][y:y+1] == 'S':
                ans += 1
            if y >= 3 and X[x][y-3:y+1] == 'SAMX':
                ans += 1
            if x >= 3 and X[x-1][y:y+1] == 'M' and X[x-2][y:y+1] == 'A' and X[x-3][y:y+1] == 'S':
                ans += 1
            if x <= len(X[x]) - 4 and X[x+1][y+1:y+2] == 'M' and X[x+2][y+2:y+3] == 'A' and X[x+3][y+3:y+4] == 'S':
                ans += 1
            if x <= len(X[x]) - 4 and y >= 3 and X[x+1][y-1:y] == 'M' and X[x+2][y-2:y-1] == 'A' and X[x+3][y-3:y-2] == 'S':
                ans += 1
            if x >= 3 and X[x-1][y+1:y+2] == 'M' and X[x-2][y+2:y+3] == 'A' and X[x-3][y+3:y+4] == 'S':
                ans += 1
            if x >= 3 and y >= 3 and X[x-1][y-1:y] == 'M' and X[x-2][y-2:y-1] == 'A' and X[x-3][y-3:y-2] == 'S':
                ans += 1
print(ans)

# part 2
ans = 0
for x in range(len(X)):
    for y in range(len(X[x])):
        if X[x][y:y+1] == 'A':
            if not(x >= 1 and x <= len(X[x]) - 2 and y >= 1 and y <= len(X[x]) - 2):
                continue
            if ((X[x+1][y+1:y+2] == 'M' and X[x-1][y-1:y] == 'S') or ((X[x+1][y+1:y+2] == 'S' and X[x-1][y-1:y] == 'M'))) and ((X[x+1][y-1:y] == 'M' and X[x-1][y+1:y+2] == 'S') or ((X[x+1][y-1:y] == 'S' and X[x-1][y+1:y+2] == 'M'))):
                ans += 1
print(ans)
