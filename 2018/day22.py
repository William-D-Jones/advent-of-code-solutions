import sys
import re
import functools
import heapq

D = [(-1,0), (0,1), (1,0), (0,-1)]
E = ['T', 'C', 'N']
Mv = D + E

@functools.cache
def get_gi(r, c, tr, tc, depth):
    if r==0 and c==0:
        return 0
    elif r==tr and c==tc:
        return 0
    elif r==0:
        return 16807 * c
    elif c==0:
        return 48271 * r
    else:
        return get_er(r, c-1, tr, tc, depth) * get_er(r-1, c, tr, tc, depth)

@functools.cache
def get_er(r, c, tr, tc, depth):
    return ( get_gi(r, c, tr, tc, depth) + depth ) % 20183

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]
for x in X:
    M = re.match(r'(depth|target): ([0-9]+)(,[0-9]+)*', x)
    if M.group(1) == 'depth':
        depth = int(M.group(2))
    elif M.group(1) == 'target':
        tc,tr = int(M.group(2)), int(M.group(3)[1:])
    else:
        assert False

# part 1
ans1 = 0
for r in range(0, tr+1):
    for c in range(0, tc+1):
        er = get_er(r, c, tr, tc, depth)
        if er % 3 == 0:
            ans1 += 0
        elif er % 3 == 1:
            ans1 += 1
        elif er % 3 == 2:
            ans1 += 2
        else:
            assert False
print(ans1)

# part 2
Q = []
heapq.heappush( Q, (0, (0,0), 'T') )
step_min = None
Seen = {((0,0), 'T'): 0}
while Q:
    step, (r,c), e = heapq.heappop(Q)
    # check if we have reached the target
    if r==tr and c==tc and e=='T':
        if step_min is None or step_min > step:
            step_min = step
        continue
    # check if the path is too long
    if step_min is not None and step+1 >= step_min:
        continue
    # get the erosion level of the current region
    er = get_er(r, c, tr, tc, depth)
    for mv in Mv:
        # change equipment
        if len(mv) == 1:
            nr,nc = r,c
            e_next = mv
            if e_next == e:
                continue
            step_next = step + 7
            er_next = er
        # move to a new position
        elif len(mv) == 2:
            dr, dc = mv
            nr = r+dr
            nc = c+dc
            e_next = e
            step_next = step + 1
            if nr<0 or nc<0:
                continue
            er_next = get_er(nr, nc, tr, tc, depth)
        else:
            assert False
        # check if the equipment can be taken to the next position
        if (er_next % 3 == 0 and e_next == 'N') or \
        (er_next % 3 == 1 and e_next == 'T') or \
        (er_next % 3 == 2 and e_next == 'C'):
            continue
        # check if we have taken the minimum path to the next state
        State = ((nr,nc), e_next)
        if State in Seen and Seen[State] <= step_next:
            continue
        Seen[State] = step_next
        # continue the journey
        heapq.heappush( \
        Q, (step_next, (nr,nc), e_next) )
ans2 = step_min
print(ans2)

