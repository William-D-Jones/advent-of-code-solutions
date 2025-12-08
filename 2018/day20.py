import sys
from collections import deque

D = {'N': (-1,0), 'E': (0,1), 'S': (1,0), 'W': (0,-1)}

# parsing
X = list(open(sys.argv[1], 'r').read().strip())
assert X[0]=='^'
assert X[-1]=='$'

# part 1
# identify the rooms and doors
r,c = 0,0
Mem = []
Door = set()
Room = set( (r,c) )
for i in range(1,len(X)-1):
    if X[i] in D:
        dr,dc = D[ X[i] ]
        nr = r+dr
        nc = c+dc
        door = tuple(sorted([(r,c), (nr,nc)]))
        Door.add(door)
        r,c = nr,nc
        Room.add( (r,c) )
    elif X[i]=='(':
        Mem.append( (r,c) )
        pass
    elif X[i]=='|':
        r,c = Mem[-1]
    elif X[i]==')':
        Mem.pop()
    else:
        assert False
# find the shortest path from the start to each room
Step = {}
Q = deque([(0, (0,0))])
while Q:
    step, (r,c) = Q.popleft()
    for dr,dc in D.values():
        nr = r+dr
        nc = c+dc
        door = tuple(sorted([(r,c), (nr,nc)]))
        if door not in Door:
            continue
        step_next = step+1
        if (nr,nc) in Step and Step[(nr,nc)] <= step_next:
            continue
        Step[(nr,nc)] = step_next
        Q.append( (step_next, (nr,nc)) )
ans1 = max(Step.values())
print(ans1)

# part 2
ans2 = sum(1 for (r,c),step in Step.items() if step>=1000)
print(ans2)

