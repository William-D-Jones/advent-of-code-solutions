import sys
import itertools

D = {'^': (-1,0), '>': (0,1), 'v': (1,0), '<': (0,-1)}
dd = list(D.values())

# parsing
X = [ list(l) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])
assert all(len(X[i]) == ncol for i in range(nrow))
Q0 = []
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] in D.keys():
            dr,dc = D[X[r][c]]
            Q0.append( (r,c,dr,dc,0) )
            if X[r][c] == '^' or X[r][c] == 'v':
                X[r][c] == '|'
            elif X[r][c] == '<' or X[r][c] == '>':
                X[r][c] == '-'
            else:
                assert False
Q0 = sorted(Q0)

# part 1
Q = list(Q0)
i = 0
while all(not(ri==rj and ci==cj) for \
(ri,ci,dri,dci,trni),(rj,cj,drj,dcj,trnj) in itertools.combinations(Q,2)):
    r,c,dr,dc,trn = Q.pop(0)
    r,c = r+dr,c+dc
    if X[r][c] == '\\':
        dr,dc = dc,dr
    elif X[r][c] == '/':
        dr,dc = -dc,-dr
    elif X[r][c] == '+':
        if trn == 0:
            dr,dc = dd[(dd.index( (dr,dc) )-1)%len(dd)]
        elif trn == 1:
            pass
        elif trn == 2:
            dr,dc = dd[(dd.index( (dr,dc) )+1)%len(dd)]
        trn = (trn+1)%3
    Q.append( (r,c,dr,dc,trn) )
    if i == len(Q)-1:
        Q = sorted(Q)
        i = 0
    else:
        i += 1
Pos = [(r,c) for r,c,dr,dc,trn in Q]
Coll = set()
for r,c in Pos:
    if Pos.count( (r,c) ) > 1:
        Coll.add( (r,c) )
assert len(Coll) == 1
ans1 = ','.join(map(str, Coll.pop()[::-1]))
print(ans1)

# part 2
Q = list(Q0)
i = 0
n = len(Q)
while len(Q) > 1 or i != 0:
    r,c,dr,dc,trn = Q.pop(0)
    r,c = r+dr,c+dc
    if X[r][c] == '\\':
        dr,dc = dc,dr
    elif X[r][c] == '/':
        dr,dc = -dc,-dr
    elif X[r][c] == '+':
        if trn == 0:
            dr,dc = dd[(dd.index( (dr,dc) )-1)%len(dd)]
        elif trn == 1:
            pass
        elif trn == 2:
            dr,dc = dd[(dd.index( (dr,dc) )+1)%len(dd)]
        trn = (trn+1)%3
    coll = False
    j = 0
    while j < len(Q):
        rj,cj,drj,dcj,trnj = Q[j]
        if r==rj and c==cj:
            coll = True
            Q.pop(j)
            if j <= (n-2-i):
                i += 1
        else:
            j += 1
    if not coll:
        Q.append( (r,c,dr,dc,trn) )
    if i >= n-1:
        Q = sorted(Q)
        n = len(Q)
        i = 0
    else:
        i += 1
ans2 = ','.join(map(str, Q.pop()[0:2][::-1]))
print(ans2)

