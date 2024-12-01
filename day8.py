import sys
import math
# from copy import deepcopy
# from collections import defaultdict
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Ins = list(X[0])
D = {}
for i,x in enumerate(X):
    if i >= 2:
        x1, x2, x3, x4 = re.split('[\W=()]+', x)
        D[x1] = [x2, x3]

# part 1
steps = 0
xins = 0
junc = 'AAA'
while junc != 'ZZZ':
    path = D[junc]
    ins = Ins[xins]
    if ins == 'L':
        junc = path[0]
    elif ins == 'R':
        junc = path[1]
    else:
        assert False
    if xins == len(Ins) - 1:
        xins = 0
    else:
        xins += 1
    steps += 1
print(steps)

# part 2
def step2Z(junc):
    steps = 0
    xins = 0
    while not junc.endswith('Z'):
        path = D[junc]
        ins = Ins[xins]
        if ins == 'L':
            junc = path[0]
        elif ins == 'R':
            junc = path[1]
        else:
            assert False
        if xins == len(Ins) - 1:
            xins = 0
        else:
            xins += 1
        steps += 1
    return steps

Step2Z = []
Node = []
for node in D.keys():
    if node.endswith('A'):
        Node.append(node)
for node in Node:
    Step2Z.append(step2Z(node))
print(math.lcm(*Step2Z))

