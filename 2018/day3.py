import sys
import re
import itertools

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
C = []
for x in X:
    M = re.match('^#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)$', x)
    C.append( tuple(int(M.group(i)) for i in range(1, 6)) )

# parts 1 and 2
# find overlapping claims
Ov = []
ixov = set()
for c1,c2 in itertools.combinations(C, 2):
    ovxmin = max(c1[1], c2[1])
    ovxmax = min(c1[1]+c1[3], c2[1]+c2[3])
    ovymin = max(c1[2], c2[2])
    ovymax = min(c1[2]+c1[4], c2[2]+c2[4])
    if ovxmax-ovxmin >= 1 and ovymax-ovymin >= 1:
        Ov.append( (ovxmin, ovxmax, ovymin, ovymax) )
        ixov.add(c1[0])
        ixov.add(c2[0])
# merge overlapping claims
S = set()
for ovxmin,ovxmax,ovymin,ovymax in Ov:
    for x,y in itertools.product( range(ovxmin,ovxmax), range(ovymin,ovymax) ):
        S.add( (x,y) )
ans1 = len(S)
print(ans1)
# find the claim that does not overlap
nov = set(c[0] for c in C) - ixov
assert len(nov) == 1
ans2 = nov.pop()
print(ans2)

