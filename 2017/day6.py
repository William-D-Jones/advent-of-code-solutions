import sys

# parsing
X = \
list(map(int, ''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split()))

# part 1
Seen = set()
cyc = 0
while tuple(X) not in Seen:
    Seen.add(tuple(X))
    cyc += 1
    ix = X.index(max(X))
    n = X[ix]
    X[ix] = 0
    for i in range(n):
        ix_next = (ix+i+1)%len(X)
        X[ix_next] += 1
ans1 = cyc
print(ans1)

# part 2
Loop = tuple(X)
cyc = 0
while cyc == 0 or tuple(X) != Loop:
    cyc += 1
    ix = X.index(max(X))
    n = X[ix]
    X[ix] = 0
    for i in range(n):
        ix_next = (ix+i+1)%len(X)
        X[ix_next] += 1
ans2 = cyc
print(ans2)

