import sys
import math
from copy import deepcopy
from collections import defaultdict
import re

# parsing
X = open(sys.argv[1], 'r').read().strip()

# part 1
ans = 0
re_mul = re.compile("^mul\(([0-9]{1,3}),([0-9]{1,3})\)")
for i in range(len(X)):
    match_mul = re_mul.search(X[i:])
    if match_mul is not None:
        ans += int(match_mul[1]) * int(match_mul[2])
print(ans)

# part 2
ans = 0
re_mul = re.compile("^mul\(([0-9]{1,3}),([0-9]{1,3})\)")
re_do = re.compile("^do\(\)")
re_dont = re.compile("^don't\(\)")
ins = True
for i in range(len(X)):
    match_do = re_do.search(X[i:])
    match_dont = re_dont.search(X[i:])
    if match_do is not None:
        ins = True
    elif match_dont is not None:
        ins = False
    elif ins:
        match_mul = re_mul.search(X[i:])
        if match_mul is not None:
            ans += int(match_mul[1]) * int(match_mul[2])
print(ans)

