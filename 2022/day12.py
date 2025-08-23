import sys
from collections import deque

A = ord('a')
Z = ord('z')
D = [ (-1,0), (0,1), (1,0), (0,-1) ]

def min_walk(X, S, E, max_step = None):
    Pos = deque([S])
    Step = deque([0])
    Seen = {}
    min_step = None
    while Pos:
        r,c = Pos.popleft()
        step = Step.popleft()
        if max_step is not None and step+1>max_step:
            return False
        if min_step is not None and step+1>=min_step:
            continue
        for dr,dc in D:
            nr,nc = r+dr,c+dc
            if not(0<=nr<nrow and 0<=nc<ncol) or \
            ord(X[nr][nc]) - ord(X[r][c]) > 1 or \
            ((nr,nc) in Seen.keys() and Seen[ (nr,nc) ] >= step+1):
                continue
            Seen[ (nr,nc) ] = step+1
            if (nr,nc) == E:
                if min_step is None or min_step > step+1:
                    min_step = step+1
                continue
            Pos.append( (nr,nc) )
            Step.append( step+1 )
    return min_step

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == 'S':
            S = (r,c)
            X[r][c] = 'a'
        elif X[r][c] == 'E':
            E = (r,c)
            X[r][c] = 'z'

# part 1
ans1 = min_walk(X, S, E)
print(ans1)

# part 2
min_step = None
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] != 'a':
            continue
        step = min_walk(X, (r,c), E, min_step)
        if step and (min_step is None or step < min_step):
            min_step = step
ans2 = min_step
print(ans2)
        
