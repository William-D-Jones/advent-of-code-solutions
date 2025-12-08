import sys
import itertools

# parsing
X = [tuple(map(int,l.strip().split(','))) for l in open(sys.argv[1], 'r')]

# parts 1 and 2
# sort pairs of coordinates based on the Euclidian distance
Dist = []
for (j0x,j0y,j0z), (j1x,j1y,j1z) in itertools.combinations(X, 2):
    dsq = (j0x-j1x)**2 + (j0y-j1y)**2 + (j0z-j1z)**2
    Dist.append( (dsq, (j0x,j0y,j0z), (j1x,j1y,j1z)) )
Q = sorted(Dist)[::-1]
J = set(X)
# make connections
Circuit = []
ix = 0
while J or len(Circuit) != 1:
    ix += 1
    dsq, J0, J1 = Q.pop()
    if J0 in J:
        J.remove(J0)
    if J1 in J:
        J.remove(J1)
    cnx = [i for i,C in enumerate(Circuit) if J0 in C or J1 in C]
    if len(cnx) == 0:
        Circuit.append( set([J0,J1]) )
    elif len(cnx) == 1:       
        Circuit[cnx[0]] |= set([J0,J1])
    elif len(cnx) == 2:
        Circuit[cnx[0]] |= set([J0,J1]) | Circuit.pop(cnx[1])
    else:
        assert False
    # check if part 1 has been completed
    if ix == 1000:
        L = sorted([len(C) for C in Circuit])
# calculate final answers
ans1 = L[-1] * L[-2] * L[-3]
print(ans1)
ans2 = J0[0] * J1[0]
print(ans2)

