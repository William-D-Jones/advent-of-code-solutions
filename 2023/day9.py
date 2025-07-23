import sys
import math
from copy import deepcopy
from collections import defaultdict
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
S = [ x.split() for x in X ]
Si = []
for s in S:
    Si.append([int(v) for v in s])

def extrapolate(l, sign = 1):
    Diff = []
    for i in range(len(l) - 1):
        Diff.append(l[i+1] - l[i])
    if all(d == 0 for d in Diff):
        return l[0]
    else:
        lNew = []
        for i in range(len(Diff)):
            lNew.append(l[-1 if sign == 1 else 0] + sign * Diff[i])
        return extrapolate(lNew, sign = sign)

# part 1
ans = 0
for s in Si:
    ans += extrapolate(s)
print(ans)

# part 2
ans = 0
for s in Si:
    ans += extrapolate(s, sign = -1)
print(ans)

