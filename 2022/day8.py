import sys

D = [ (1,0), (0,-1), (-1,0), (0,1) ]

# parsing
X = [ list(map(int, list(l.strip()))) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# part 1
Vis = set()
for r in range(nrow):
    for c in range(ncol):
        h = X[r][c]
        if all(h>t for t in X[r][c+1:]) or all(h>t for t in X[r][:c]) or \
        all(h>X[tr][c] for tr in range(0,r)) or \
        all(h>X[tr][c] for tr in range(r+1,nrow)):
            Vis.add( (r,c) )
ans1 = len(Vis)
print(ans1)

# part 2
Scenic = {}
for r in range(nrow):
    for c in range(ncol):
        h = X[r][c]
        score_t = r - max([0] + [tr for tr in range(0,r) if X[tr][c] >= h])
        score_b = \
        min([nrow-1] + [tr for tr in range(r+1,nrow) if X[tr][c] >= h]) - r
        score_l = c - max([0] + [tc for tc in range(0,c) if X[r][tc] >= h])
        score_r = \
        min([ncol-1] + [tc for tc in range(c+1,ncol) if X[r][tc] >= h]) - c
        Scenic[ (r,c) ] = score_t * score_b * score_l * score_r
ans2 = max(Scenic.values())
print(ans2)

