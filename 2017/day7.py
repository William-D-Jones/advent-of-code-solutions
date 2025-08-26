import sys
from collections import deque

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Weight = {}
Con = {}
for x in X:
    xs = x.split(' -> ')
    src, weight = xs[0].split()
    Weight[src] = int(weight[1:-1])
    if src not in Con.keys():
        Con[src] = []
    if len(xs) > 1:
        Tar = xs[1].split(', ')
        for tar in Tar:
            Con[src].append(tar)
iCon = {}
for src,Tar in Con.items():
    for tar in Tar:
        iCon[tar] = src

# identify the terminal leaves of the tree
Term = [tower for tower in Con.keys() if len(Con[tower]) == 0]

# part 1
point = Term[0]
while point in iCon.keys():
    point = iCon[point]
ans1 = point
print(ans1)

# part 2
# find the weight of each of the sub-towers that comprise a tower
Weight_Tot = {}
Q_Tower = deque([tower for tower in Con.keys()])
while Q_Tower:
    tower = Q_Tower.popleft()
    Sub = Con[tower]
    Weight_Sub = []
    for sub in Sub:
        if sub in Term:
            Weight_Sub.append(Weight[sub])
        elif sub in Weight_Tot.keys():
            Weight_Sub.append(sum(Weight_Tot[sub]) + Weight[sub])
        else:
            Q_Tower.append(tower)
            break
    if len(Weight_Sub) == len(Sub):
        Weight_Tot[tower] = tuple(Weight_Sub)
# the tower with the wrong weight should have all its children balanced, but
# the parent of this tower will not have all its children balanced
Unbal = []
Dist = []
for tower in Weight_Tot.keys():
    Weight_Sub = Weight_Tot[tower]
    Weight_Par = Weight_Tot[iCon[tower]] if tower in iCon.keys() else []
    if (len(Weight_Sub) == 0 or all(w == Weight_Sub[0] for w in Weight_Sub)) \
    and any(w != Weight_Par[0] for w in Weight_Par):
        Unbal.append(tower)
        # get the distance of this tower from the root node
        T = [ans1]
        dist = 0
        while tower not in T:
            T_next = []
            for t in T:
                T_next += Con[t]
            T = T_next
            dist += 1
        Dist.append(dist)
# the tower with the wrong weight will be the furthest possible from the root
i = 0
while i < len(Dist):
    if Dist[i] != max(Dist):
        Unbal.pop(i)
        Dist.pop(i)
    else:
        i += 1
# find the parent of the candidate unbalanced towers
par_unbal = set([iCon[tower] for tower in Unbal])
assert len(par_unbal) == 1
par_unbal = par_unbal.pop()
# determine the weight change needed
w_unbal = Weight_Tot[par_unbal]
w_wrong = [w for w in w_unbal if w_unbal.count(w) == 1]
w_right = set([w for w in w_unbal if w_unbal.count(w) > 1])
assert len(w_wrong) == 1 and len(w_right) == 1
w_wrong = w_wrong.pop()
w_right = w_right.pop()
# identify the incorrect sub-tower
t_wrong = Con[par_unbal][w_unbal.index(w_wrong)]
ans2 = Weight[t_wrong] + (w_right-w_wrong)
print(ans2)

