import sys
from collections import deque

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Con = {}
for x in X:
    xs = x.split(' <-> ')
    src = int(xs[0])
    Tar = list(map(int, xs[1].split(', ')))
    if src not in Con.keys():
        Con[src] = []
    Con[src] += Tar
    for tar in Tar:
        if tar not in Con.keys():
            Con[tar] = []
        Con[tar].append(src)
    
# parts 1 and 2
Grp = []
U = set(Con.keys())
while U:
    grp = set()
    Prog = deque([U.pop()])
    while Prog:
        src = Prog.popleft()
        if src in grp:
            continue
        grp.add(src)
        for tar in Con[src]:
            if tar not in grp and tar not in Prog:
                Prog.append(tar)
                U.remove(tar)
    Grp.append(grp)
    if 0 in grp:
        ans1 = len(grp)
print(ans1)
ans2 = len(Grp)
print(ans2)

