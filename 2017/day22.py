import sys

D = [ (-1,0), (0,1), (1,0), (0,-1) ]

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# part 1
r,c = nrow//2,ncol//2
dx = 0
n = 10000
ans1 = 0
Inf = set((r,c) for r in range(nrow) for c in range(ncol) if X[r][c] == '#')
for _ in range(n):
    if (r,c) in Inf:
        dx = (dx+1)%len(D)
        Inf.remove( (r,c) )
    else:
        dx = (dx-1)%len(D)
        Inf.add( (r,c) )
        ans1 += 1
    dr,dc = D[dx]
    r += dr
    c += dc
print(ans1)

# part 2
r,c = nrow//2,ncol//2
dx = 0
n = 10000000
ans2 = 0
Inf = set((r,c) for r in range(nrow) for c in range(ncol) if X[r][c] == '#')
Weak = set()
Flag = set()
for _ in range(n):
    if (r,c) in Inf:
        dx = (dx+1)%len(D)
        Inf.remove( (r,c) )
        Flag.add( (r,c) )
    elif (r,c) in Weak:
        Weak.remove( (r,c) )
        Inf.add( (r,c) )
        ans2 += 1
    elif (r,c) in Flag:
        dx = (dx+2)%len(D)
        Flag.remove( (r,c) )
    else:
        dx = (dx-1)%len(D)
        Weak.add( (r,c) )
    dr,dc = D[dx]
    r += dr
    c += dc
print(ans2)

