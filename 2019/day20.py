import sys
from collections import defaultdict, deque

D = [(-1, 0), (0, 1), (1, 0), (0, -1)]
A = ord('A')
Z = ord('Z')

# parsing
X = [list(l.strip('\n')) for l in open(sys.argv[1], 'r')]
Grid = defaultdict(str)
Portal = set()
nrow = len(X)
ncol = len(X[0])
Start = []
End = []
assert all(len(row) == ncol for row in X)
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == '.':
            Grid[(r, c)] = X[r][c]
            # parse a possible portal
            for dr, dc in D:
                P = []
                n = 1
                while 0 <= r+dr*n < nrow and 0 <= c+dc*n < ncol and \
                A <= ord(X[r+dr*n][c+dc*n]) <= Z:
                    P.append( X[r+dr*n][c+dc*n] )
                    n += 1
                if len(P) > 0:
                    if (dr == 1 and dc == 0) or (dr == 0 and dc == 1):
                        portal = ''.join(P)
                        Grid[(r+dr, c+dc)] = portal
                    elif (dr == -1 and dc == 0) or (dr == 0 and dc == -1):
                        portal = ''.join(reversed(P))
                        Grid[(r+dr, c+dc)] = portal
                    else:
                        assert False
                    if portal == 'AA':
                        Start.append( (r+dr, c+dc) )
                    elif portal == 'ZZ':
                        End.append( (r+dr, c+dc) )
                    Portal.add(portal)
        elif X[r][c] == '#':
            Grid[(r, c)] = X[r][c]
        else:
            assert X[r][c] == ' ' or A <= ord(X[r][c]) <= Z
# identify start and end
assert len(Start) == 1
Start = Start.pop()
assert len(End) == 1
End = End.pop()
# identify portal destinations
Jump = {}
for portal in Portal:
    Pos = []
    for r in range(nrow):
        for c in range(ncol):
            if Grid[(r, c)] == portal:
                Pos.append( (r, c) )
    assert len(Pos) == 1 or len(Pos) == 2
    for i, pos in enumerate(Pos):
        Key = (portal, pos)
        if len(Pos) == 1:
            Jump[Key] = pos
        elif len(Pos) == 2:
            Jump[Key] = Pos[ (i+1) % 2 ]
        else:
            assert False

# part 1
Seen = {Start: -1}
Q = deque([ (-1, tuple(Start)) ])
min_step = None
while Q:
    step, (r, c) = Q.popleft()
    if min_step is not None and step >= min_step:
        continue
    for dr, dc in D:
        nr = r + dr
        nc = c + dc
        # check if the new coordinate is valid
        if not (0 <= nr < nrow) or not (0 <= nc < ncol) or \
        Grid[(nr, nc)] == '' or Grid[(nr, nc)] == '#':
            continue
        step_next = step + 1
        # check if the new coordinate is a portal
        if not Grid[(nr, nc)] == '.':
            portal = Grid[(nr, nc)]
            Key = (portal, (nr, nc))
            assert Key in Jump
            nr, nc = Jump[Key]
            step_next -= 1
        if (nr, nc) in Seen and Seen[(nr, nc)] <= step_next:
            continue
        Seen[(nr, nc)] = step_next
        # check if we have completed the search
        if (nr, nc) == End:
            if min_step is None or step_next < min_step:
                min_step = step_next
            continue
        # continue the search
        Q.append( (step_next, (nr, nc)) )
ans1 = min_step
print(ans1)

# part 2
# categorize the portals as inner and outer
Inner = set()
Outer = set()
for portal, (r, c) in Jump:
    if r == 1 or r == nrow - 2 or c == 1 or c == ncol - 2:
        Outer.add( (portal, (r, c)) )
    else:
        Inner.add( (portal, (r, c)) )
# solve
Seen = {(0, Start): -1}
Q = deque([ (0, -1, tuple(Start)) ])
min_step = None
while Q:
    level, step, (r, c) = Q.popleft()
    if min_step is not None and step >= min_step:
        continue
    if Grid[(r, c)] != '.':
        step_next = step
    else:
        step_next = step + 1
    for dr, dc in D:
        nr = r + dr
        nc = c + dc
        # check if the new coordinate is valid
        if not (0 <= nr < nrow) or not (0 <= nc < ncol) or \
        Grid[(nr, nc)] == '' or Grid[(nr, nc)] == '#':
            continue
        # check if the new coordinate is a portal
        if not Grid[(nr, nc)] == '.':
            portal = Grid[(nr, nc)]
            Key = (portal, (nr, nc))
            assert Key in Jump
            if portal in ('AA', 'ZZ'):
                if level > 0:
                    continue
                level_next = level
            else:
                if level == 0 and Key in Outer:
                    continue
                elif Key in Inner:
                    level_next = level + 1
                elif Key in Outer:
                    level_next = level - 1
                    assert level_next >= 0
                else:
                    assert False
            nr, nc = Jump[Key]
        else:
            level_next = level
        if (level_next, (nr, nc)) in Seen and \
        Seen[(level_next, (nr, nc))] <= step_next:
            continue
        Seen[(level_next, (nr, nc))] = step_next
        # check if we have completed the search
        if (nr, nc) == End and level_next == 0:
            if min_step is None or step_next < min_step:
                min_step = step_next
            continue
        # continue the search
        Q.append( (level_next, step_next, (nr, nc)) )
ans2 = min_step
print(ans2)
