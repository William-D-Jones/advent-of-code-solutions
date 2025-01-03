import sys
import math
from collections import defaultdict
from copy import deepcopy

# parsing
X = list(map(int, open(sys.argv[1], 'r').read().strip().split()))
dict_X = defaultdict(int)
for x in X:
    dict_X[x] += 1

# parts 1 and 2
for blink in range(75):
    dict_blink = defaultdict(int)
    for val in dict_X.keys():
        n_digit = math.floor(math.log(val, 10)) + 1 if val > 0 else 1
        if val == 0:
            dict_blink[1] += dict_X[val]
        elif n_digit % 2 == 0:
            base = 10 ** (n_digit // 2)
            val1 = math.floor(val / base)
            val2 = val - val1 * base
            dict_blink[val1] += dict_X[val]
            dict_blink[val2] += dict_X[val]
        else:
            dict_blink[2024*val] += dict_X[val]
    dict_X = deepcopy(dict_blink)
    if blink == 24:
        dict_X1 = deepcopy(dict_X)
print(sum(dict_X1.values()))
print(sum(dict_X.values()))

