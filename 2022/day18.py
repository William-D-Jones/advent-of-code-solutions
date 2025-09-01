import sys
from collections import deque
import itertools

# parsing
X = [ tuple(map(int, l.strip().split(','))) for l in open(sys.argv[1], 'r') ]

# part 1
Out = set()
ans1 = 0
for q in X:
    for ix,d in itertools.product( range(3), (-1,1) ):
        nxt = tuple(q[i]+d if i == ix else q[i] for i in range(3))
        if nxt not in X:
            Out.add(nxt)
            ans1 += 1
print(ans1)

# part 2
xmin = min(x[0] for x in X)
xmax = max(x[0] for x in X)
ymin = min(x[1] for x in X)
ymax = max(x[1] for x in X)
zmin = min(x[2] for x in X)
zmax = max(x[2] for x in X)
# group the empty spaces, looking for ones that are not bordered by lava
Pocket = set()
while Out:
    Grp = set([Out.pop()])
    Q = deque(Grp)
    is_pocket = True
    while is_pocket and Q:
        q = Q.popleft()
        for ix,d in itertools.product( range(3), (-1,1) ):
            nxt = tuple(q[i]+d if i == ix else q[i] for i in range(3))
            if nxt in Grp or nxt in X:
                continue
            elif nxt in Out:
                Out.remove(nxt)
            else:
                if not xmin<=nxt[0]<=xmax or not ymin<=nxt[1]<=ymax or \
                not zmin<=nxt[2]<=zmax:
                    is_pocket = False
                    break
            Grp.add(nxt)
            Q.append(nxt)
    if is_pocket:
        Pocket |= Grp
# calculate the remaining surface area
ans2 = 0
for q in X:
    for ix,d in itertools.product( range(3), (-1,1) ):
        nxt = tuple(q[i]+d if i == ix else q[i] for i in range(3))
        if nxt not in X and nxt not in Pocket:
            ans2 += 1
print(ans2)

