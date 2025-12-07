import sys
from collections import Counter

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
nrow = len(X)
ncol = len(X[0])
assert all(len(row)==ncol for row in X)
S = [(r,c) for r in range(nrow) for c in range(ncol) if X[r][c] == 'S']
assert len(S) == 1
S = S.pop()

# parts 1 and 2
ans1 = 0
ans2 = 0
T = [(tuple(S), 1)]
while T:
    n_path = len(T)
    C = Counter()
    while T:
        (r,c), n = T.pop()
        if r+1 >= nrow:
            ans2 += n
            continue
        if X[r+1][c] == '.':
            C[(r+1,c)] += n
        elif X[r+1][c] == '^':
            if C[(r+1,c-1)] == 0 or C[(r+1,c+1)] == 0:
                ans1 += 1
            C[(r+1,c-1)] += n
            C[(r+1,c+1)] += n
    T = [((r,c),n) for (r,c),n in C.items() if n>0]
print(ans1)
print(ans2)

