import sys
import re
import itertools
from collections import defaultdict

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Par = {}
for i,x in enumerate(X):
    M = re.match('^p=<([\\-0-9,]+)>, v=<([\\-0-9,]+)>, a=<([\\-0-9,]+)>$', x)
    P = list(map(int, M.group(1).split(',')))
    V = list(map(int, M.group(2).split(',')))
    A = list(map(int, M.group(3).split(',')))
    Par[i] = (P, V, A)

# part 1
# simply find the particle with the lowest acceleration
min_a = None
ix_min_a = None
for i,(P,V,A) in Par.items():
    a = (A[0]**2 + A[1]**2 + A[2]**2)**0.5
    if min_a is None or min_a > a:
        min_a = a
        ix_min_a = i
ans1 = ix_min_a
print(ans1)

# part 2

# Let ai be the acceleration of the ith particle.
# Then the velocity of the ith particle at time t is vit = vi0 + t*ai.
# Then the position of the ith particle at time t is:
# pit = pi0 + \sum_{m=1}^{t}(vi0+m*ai) = pi0 + t*vi0 + t(t+1)/2 * ai
# Rearranging and simplifying:
# pit = pi0 + t*vi0 + ai/2 * (t**2 + t) = pi0 + (vi0+ai/2)*t + (ai/2)*t**2

# identify all collisions
Coll = defaultdict(list)
for combo in itertools.combinations(Par.keys(), 2):
    Pi, Vi, Ai = Par[combo[0]]
    Pj, Vj, Aj = Par[combo[1]]
    # get the candidate collision times
    R = set()
    for ix in range(3):
        a = (Ai[ix]-Aj[ix])/2
        b = Vi[ix]-Vj[ix]+Ai[ix]/2-Aj[ix]/2
        c = Pi[ix]-Pj[ix] 
        try:
            r = (-b + (b**2 - 4*a*c)**0.5) // (2*a)
            R.add(r)
        except:
            pass
        try:
            r = (-b - (b**2 - 4*a*c)**0.5) // (2*a)
            R.add(r)
        except:
            pass
    # check the candidate collision times
    T = set()
    for r in R:
        if r <= 0:
            continue
        if all( \
        (Ai[ix]-Aj[ix])/2 * r**2 + (Vi[ix]-Vj[ix]+Ai[ix]/2-Aj[ix]/2) * r + \
        (Pi[ix]-Pj[ix]) == 0 for ix in range(3) ):
            T.add(r)
    if T:
        assert len(T) == 1
        Coll[T.pop()] += list(combo)
Lost = set()
# parse the collisions
for t in sorted(Coll.keys()):
    P_tot = set(Coll[t])
    P_coll = P_tot-Lost
    if len(P_coll) > 1:
        Lost |= P_coll
Surv = set(Par.keys()) - Lost
ans2 = len(Surv)
print(ans2)

