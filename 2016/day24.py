import sys
from collections import deque
import itertools

D = [ (1,0), (0,-1), (-1,0), (0,1) ]

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])
Loc = {}
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] in '0123456789':
            Loc[ X[r][c] ] = (r,c)
Num = set(Loc.keys())

# parts 1 and 2
# determine the minimum number of steps between each pair of numbers
Min_Step = {}
for num_start, num_end in itertools.combinations(Num, 2):
    Pos = deque([ Loc[num_start] ])
    Step = deque([ 0 ])
    Seen = set([Loc[num_start]])
    min_step = None
    while Pos:
        r,c = Pos.popleft()
        step = Step.popleft()
        if min_step is not None and step+1>=min_step:
            continue
        for dr,dc in D:
            nr,nc = r+dr,c+dc
            if 0<=nr<nrow and 0<=nc<ncol and X[nr][nc] != '#' and \
            (nr,nc) not in Seen:
                pos_next = (nr,nc)
                step_next = step+1
                Seen.add(pos_next)
                if pos_next == Loc[num_end]:
                    if min_step is None or step_next < min_step:
                        min_step = step_next
                    continue
                Pos.append(pos_next)
                Step.append(step_next)
    Min_Step[ (num_start, num_end) ] = min_step
# consider all possible orderings of the points, and find the shortest path
ans1 = None
ans2 = None
for Path in itertools.permutations(Num):
    Path = list(Path)
    Path.append('0')
    if Path[0] != '0':
        continue
    L1 = 0
    L2 = 0
    for i in range(1, len(Path)):
        num_start = Path[i-1]
        num_end = Path[i]
        if (num_start, num_end) in Min_Step.keys():
            step = Min_Step[ (num_start, num_end) ]
        elif (num_end, num_start) in Min_Step.keys():
            step = Min_Step[ (num_end, num_start) ]
        else:
            assert False
        if i < len(Path)-1:
            L1 += step
        L2 += step
    if ans1 is None or L1 < ans1:
        ans1 = L1
    if ans2 is None or L2 < ans2:
        ans2 = L2
print(ans1)
print(ans2)

