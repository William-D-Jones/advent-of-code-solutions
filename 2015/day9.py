import sys
from collections import deque

# parsing
Dist = {}
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Loc = set()
for x in X:
    xs = x.split(' ')
    start = xs[0]
    end = xs[2]
    Loc.add(start)
    Loc.add(end)
    dist = int(xs[4])
    Dist[ tuple(sorted([start,end])) ] = dist

# part 1
Path = deque(Loc)
Seen = deque([set([loc]) for loc in Loc])
Steps = deque([0 for loc in Loc])
shortest = -1
while Path:
    path = Path.popleft()
    seen = Seen.popleft()
    steps = Steps.popleft()
    for loc1,loc2 in Dist.keys():
        if (loc1 == path or loc2 == path) and \
        (loc1 not in seen or loc2 not in seen):
            steps_next = Dist[(loc1,loc2)]
            if shortest != -1 and shortest < steps + steps_next:
                continue
            if len(seen) == len(Loc) - 1:
                if shortest == -1:
                    shortest = steps + steps_next
                else:
                    shortest = min(shortest, steps + steps_next)
                continue
            dest = loc1 if loc1 != path else loc2
            Path.append(dest)
            Seen.append(seen | set([dest]))
            Steps.append(steps + steps_next)
ans1 = shortest
print(ans1)

# part 2
Path = deque(Loc)
Seen = deque([set([loc]) for loc in Loc])
Steps = deque([0 for loc in Loc])
Longest = []
while Path:
    path = Path.popleft()
    seen = Seen.popleft()
    steps = Steps.popleft()
    for loc1,loc2 in Dist.keys():
        if (loc1 == path or loc2 == path) and \
        (loc1 not in seen or loc2 not in seen):
            steps_next = Dist[(loc1,loc2)]
            if len(seen) == len(Loc) - 1:
                Longest.append(steps + steps_next)
                continue
            dest = loc1 if loc1 != path else loc2
            Path.append(dest)
            Seen.append(seen | set([dest]))
            Steps.append(steps + steps_next)
ans2 = max(Longest)
print(ans2)

