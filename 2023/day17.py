import sys
from collections import deque

D = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
iD = { value: key for key, value in D.items() }

def min_heat(X, min_consecutive, max_consecutive):
    Seen = {}
    Path = deque()
    Heat = deque()
    Step = deque()
    # setup the paths
    for d in D.values():
        # initialize the path
        pos = (0, 0)
        path = (pos, d)
        # initialize the trackers
        Seen[(pos, d, 0)] = 0
        Path.append(path)
        Heat.append(0)
        Step.append(0)
    minh = None
    # generate paths
    while len(Path) > 0:
        heat = Heat.popleft()
        path = Path.popleft()
        step = Step.popleft()
        for d in D.values():
            # determine if the direction is allowed, and count consecutive steps
            if d == tuple(-x for x in path[1]):
                # opposite direction
                continue
            elif d == path[1]:
                # same direction
                if step >= max_consecutive:
                    continue
                else:
                    step_next = step + 1
            else:
                # different direction
                if step < min_consecutive:
                    continue
                else:
                    step_next = 1
            # adjust the position, and confirm we are still inside the grid
            pos = ( path[0][0] + d[0], path[0][1] + d[1] )
            if pos[0] < 0 or pos[0] >= nrow or pos[1] < 0 or pos[1] >= ncol:
                continue
            # calculate the heat lost
            heat_next = heat + X[pos[0]][pos[1]]
            if minh is not None and heat_next >= minh:
                continue
            # determine if the position has been seen
            if (pos, d, step_next) in Seen.keys() and \
            Seen[(pos, d, step_next)] <= heat_next:
                continue
            else:
                Seen[(pos, d, step_next)] = heat_next
            # check if we have reached the end
            if pos == (nrow-1, ncol-1):
                if step_next >= min_consecutive and \
                (minh is None or minh > heat):
                    minh = heat_next
                continue
            # record the path for the next iteration
            path_next = (pos, d)
            Path.append(path_next)
            Heat.append(heat_next)
            Step.append(step_next)
    return(minh)

# parsing
X = [ list(map(int, list(l.strip()))) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# part 1
ans1 = min_heat(X, 1, 3)
print(ans1)

# part 2
ans2 = min_heat(X, 4, 10)
print(ans2)
