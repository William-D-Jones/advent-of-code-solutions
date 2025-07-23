import sys

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# find the empty rows and columns
erow = set()
for r in range(nrow):
    if all(X[r][c] == '.' for c in range(ncol)):
        erow.add(r)
ecol = set()
for c in range(ncol):
    if all(X[r][c] == '.' for r in range(nrow)):
        ecol.add(c)

# find the galaxies
Gal = []
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == '#':
            Gal.append( (r,c) )

# part 1
ans1 = 0
ans2 = 0
for i in range(len(Gal)):
    for j in range(i+1,len(Gal)):
        gal1 = Gal[i]
        gal2 = Gal[j]
        minr = min(gal1[0], gal2[0])
        maxr = max(gal1[0], gal2[0])
        minc = min(gal1[1], gal2[1])
        maxc = max(gal1[1], gal2[1])
        dr = gal2[0] - gal1[0]
        dc = gal2[1] - gal1[1]
        addr = 0
        for r in erow:
            if minr<r<maxr:
                addr += 1
        addc = 0
        for c in ecol:
            if minc<c<maxc:
                addc += 1
        ans1 += abs(dr)+abs(dc)+addr+addc
        ans2 += abs(dr)+abs(dc)+(addr+addc)*999999
print(ans1)
print(ans2)
