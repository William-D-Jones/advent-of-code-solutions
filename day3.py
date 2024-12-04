import sys
import math
from copy import deepcopy
from collections import defaultdict
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
Ins = []
is_ins = False
ins = []
num = ''
for x in X:
    i = 0
    while i < len(x):
        c = x[i:i+1]
        c4 = x[i:i+4]
        if c == ',' and is_ins and len(ins) == 0 and num != '':
            ins.append(int(num))
            num = ''
        elif c == ')' and is_ins and len(ins) == 1:
            is_ins = False
            ins.append(int(num))
            Ins.append(ins)
        elif c4 == 'mul(':
            ins = []
            is_ins = True
            num = ''
            i += 3
        elif c in '0123456789' and is_ins:
            num = ''.join([num, c])
        else:
            is_ins = False
        i += 1
ans = 0
for ins in Ins:
    ans += ins[0] * ins[1]
print(ans)

# part 2
Ins = []
is_ins = False
ins = []
num = ''
en = True
for x in X:
    i = 0
    while i < len(x):
        c = x[i:i+1]
        c4 = x[i:i+4]
        if x[i:i+7] == "don't()":
            en = False
            is_ins = False
            i += 6
        elif x[i:i+4] == "do()":
            en = True
            i += 3
        elif c == ',' and is_ins and len(ins) == 0 and num != '':
            ins.append(int(num))
            num = ''
        elif c == ')' and is_ins and len(ins) == 1:
            is_ins = False
            ins.append(int(num))
            Ins.append(ins)
        elif c4 == 'mul(' and en:
            ins = []
            is_ins = True
            num = ''
            i += 3
        elif c in '0123456789' and is_ins:
            num = ''.join([num, c])
        else:
            is_ins = False
        i += 1
ans = 0
for ins in Ins:
    ans += ins[0] * ins[1]
print(ans)
