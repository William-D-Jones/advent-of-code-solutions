import sys
import itertools
from collections import Counter, deque

DD = [ (-1,0), (0,1), (1,0), (0,-1) ]

# parsing
X = [ tuple(map(int, l.strip().split(', '))) for l in open(sys.argv[1], 'r') ]
xmin = min(x[0] for x in X)
xmax = max(x[0] for x in X)
ymin = min(x[1] for x in X)
ymax = max(x[1] for x in X)

# part 1
dmax = 10000
S = set()
A = Counter()
for x,y in itertools.product( range(xmin,xmax+1), range(ymin,ymax+1) ):
    D = [abs(x-xi)+abs(y-yi) for xi,yi in X]
    d = min(D)
    if D.count(d) == 1:
        ix = D.index(d)
        if A[ix] != -1:
            A[ix] += 1
        if not xmin<x<xmax or not ymin<y<ymax:
            A[ix] = -1
    if sum(D) < dmax:
        S.add( (x,y) )
ans1 = max(A.values())
print(ans1)

# part 2
Q = deque(S)
while Q:
    x,y = Q.popleft()
    for dx,dy in DD:
        nx = x+dx
        ny = y+dy
        if (nx,ny) not in S:
            D = [abs(nx-xi)+abs(ny-yi) for xi,yi in X]
            if sum(D) < dmax:
                S.add( (nx,ny) )
                Q.append( (nx,ny) )
ans2 = len(S)
print(ans2)

