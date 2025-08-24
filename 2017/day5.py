import sys
from copy import deepcopy

# parsing
X = [ int(l.strip()) for l in open(sys.argv[1], 'r') ]

# part 1
X1 = deepcopy(X)
point = 0
ans1 = 0
while 0<=point<len(X1):
    ans1 += 1
    jmp = X1[point]
    X1[point] += 1
    point += jmp
print(ans1)

# part 2
X2 = deepcopy(X)
point = 0
ans2 = 0
while 0<=point<len(X2):
    ans2 += 1
    jmp = X2[point]
    X2[point] += 1 if jmp < 3 else -1
    point += jmp
print(ans2)

