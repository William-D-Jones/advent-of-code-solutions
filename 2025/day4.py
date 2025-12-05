import sys

D = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
nrow = len(X)
ncol = len(X[0])
assert all( len(row)==ncol for row in X )

# part 1
ans1 = 0
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] != '@':
            continue
        num_adj = 0
        for dr,dc in D:
            nr = r+dr
            nc = c+dc
            if 0<=nr<nrow and 0<=nc<ncol and X[nr][nc] == '@':
                num_adj += 1
        if num_adj < 4:
            ans1 += 1
print(ans1)

# part 2
ans2 = 0
T = list(X)
r = 0
c = 0
while r < nrow:
    while c < ncol:
        if T[r][c] != '@':
            c += 1
            continue
        num_adj = 0
        for dr,dc in D:
            nr = r+dr
            nc = c+dc
            if 0<=nr<nrow and 0<=nc<ncol and T[nr][nc] == '@':
                num_adj += 1
        if num_adj < 4:
            T[r][c] = '.'
            c = max(0, c-1)
            r = max(0, r-1)
            ans2 += 1
        else:
            c += 1
    r += 1
    c = 0
print(ans2)

