import sys
from collections import Counter

D = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]

def run_minute(G, L, T):
    G_Next = list(G)
    L_Next = Counter(L)
    T_Next = Counter(T)
    for r in range(nrow):
        for c in range(ncol):
            if G[r][c] == '.' and T[(r,c)] >= 3:
                G_Next[r][c] = '|'
                for dr,dc in D:
                    nr = r+dr
                    nc = c+dc
                    if not 0<=nr<nrow or not 0<=nc<ncol:
                        continue
                    T_Next[(nr,nc)] += 1
            elif G[r][c] == '|' and L[(r,c)] >= 3:
                G_Next[r][c] = '#'
                for dr,dc in D:
                    nr = r+dr
                    nc = c+dc
                    if not 0<=nr<nrow or not 0<=nc<ncol:
                        continue
                    T_Next[(nr,nc)] -= 1
                    L_Next[(nr,nc)] += 1
            elif G[r][c] == '#' and (T[(r,c)] < 1 or L[(r,c)] < 1):
                G_Next[r][c] = '.'
                for dr,dc in D:
                    nr = r+dr
                    nc = c+dc
                    if not 0<=nr<nrow or not 0<=nc<ncol:
                        continue
                    L_Next[(nr,nc)] -= 1
    return G_Next, L_Next, T_Next

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])
assert all( len(row)==ncol for row in X )

# parts 1 and 2
n1 = 10
n2 = 1000000000
# get the number of adjacent trees and lumberyards at each position in the grid
T = Counter()
L = Counter()
for r in range(nrow):
    for c in range(ncol):
        for dr,dc in D:
            nr = r+dr
            nc = c+dc
            if not 0<=nr<nrow or not 0<=nc<ncol:
                continue
            if X[r][c] == '|':
                T[(nr,nc)] += 1
            elif X[r][c] == '#':
                L[(nr,nc)] += 1
            else:
                pass
# simulate the changes until we find a repeat
G = list(X)
Hist = [tuple(tuple(row) for row in G)]
for ix in range( max(n1,n2) ):
    G, L, T = run_minute(G, L, T)
    State = tuple(tuple(row) for row in G)
    if State in Hist:
        break
    Hist.append( State )
# count the totals for part 1, which can be looked up in history
G1 = Hist[n1]
ans1 = \
sum(1 for r in range(nrow) for c in range(ncol) if G1[r][c] == '#') * \
sum(1 for r in range(nrow) for c in range(ncol) if G1[r][c] == '|')
print(ans1)
# for part 2, evaluate the repeated portion of the history
ix_rep = Hist.index(State)
len_rep = ix+1-ix_rep
n2_rep = (n2-ix_rep) // len_rep
ix2 = n2 - n2_rep * len_rep
# count the totals for part 2
G2 = Hist[ix2]
ans2 = \
sum(1 for r in range(nrow) for c in range(ncol) if G2[r][c] == '#') * \
sum(1 for r in range(nrow) for c in range(ncol) if G2[r][c] == '|')
print(ans2)

