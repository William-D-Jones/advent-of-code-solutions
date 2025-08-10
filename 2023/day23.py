import sys
from collections import deque, defaultdict

D = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
Dv = list(D.values())

def walk_path(X, J, Start, End, use_slopes = True):
    Path = deque([Start])
    Step = deque([0])
    Last_Dir = deque([(1,0)])
    Seen = deque([set([Start])])
    Finished = set()
    while Path:
        r, c = Path.popleft()
        step = Step.popleft()
        last_dir = Last_Dir.popleft()
        seen = Seen.popleft()
        for dx in D.keys():
            # check if we are obligated to go in a particular direction
            if use_slopes and X[r][c] != '.' and X[r][c] != dx:
                continue
            # get the new direction
            dr, dc = D[dx]
            # make sure that we are not doubling back
            if (dr,dc) == Dv[ (Dv.index(last_dir)+2) % 4 ]:
                continue
            # check the new coordinates
            nr = r+dr
            nc = c+dc
            npos = (nr,nc)
            if 0 <= nr < nrow and 0 <= nc < ncol and \
            X[nr][nc] != '#' and npos not in seen:
                if npos == End:
                    Finished.add(step + 1)
                else:
                    Path.append(npos)
                    Step.append(step + 1)
                    Last_Dir.append( (dr,dc) )
                    if npos in J:
                        Seen.append(seen | set([npos]))
                    else:
                        Seen.append(seen | set([]))
    return Finished

def walk2junction(X, J, Start, End):
    Path = deque([Start])
    Step = deque([0])
    Last_Dir = deque([None])
    Finished = {}
    while Path:
        r, c = Path.popleft()
        step = Step.popleft()
        last_dir = Last_Dir.popleft()
        for dx in D.keys():
            # get the new direction
            dr, dc = D[dx]
            # make sure that we are not doubling back
            if last_dir is not None and \
            (dr,dc) == Dv[ (Dv.index(last_dir)+2) % 4 ]:
                continue
            # check the new coordinates
            nr = r+dr
            nc = c+dc
            npos = (nr,nc)
            if 0 <= nr < nrow and 0 <= nc < ncol and \
            X[nr][nc] != '#':
                if npos in J or npos == End:
                    Finished[npos] = step + 1
                else:
                    Path.append(npos)
                    Step.append(step + 1)
                    Last_Dir.append( (dr,dc) )
    return Finished

def jwalk(X, J2J, Start, End):
    Path = deque([Start])
    Step = deque([0])
    Seen = deque([set([Start])])
    Finished = set()
    while Path:
        j = Path.popleft()
        step = Step.popleft()
        seen = Seen.popleft()
        for jnext in J2J[j].keys():
            if jnext in seen:
                continue
            if jnext == End:
                Finished.add(step + J2J[j][jnext])
                continue
            Path.append(jnext)
            Step.append(step + J2J[j][jnext])
            Seen.append(seen | set([jnext]))
    return Finished

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]

# find the starting and ending coordinates
nrow = len(X)
ncol = len(X[0])
for c in range(ncol):
    if X[0][c] == '.':
        Start = (0,c)
    if X[nrow-1][c] == '.':
        End = (nrow-1,c)

# find the junctions
J = set()
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == '.':
            Flank = []
            for (dr,dc) in D.values():
                if not 0<=r+dr<nrow or not 0<=c+dc<ncol:
                    continue
                flank = X[r+dr][c+dc]
                if flank != '#':
                    Flank.append(flank)
            if len(Flank) > 2:
                J.add( (r,c) )

# part 1
ans1 = max(walk_path(X, J, Start, End, use_slopes = True))
print(ans1)

# part 2

# find the number of steps between each junction
J2J = {}
for j in J:
    J2J[j] = walk2junction(X, J, j, End)
J2J[Start] = walk2junction(X, J, Start, End)

# walk between junctions
ans2 = max(jwalk(X, J2J, Start, End))
print(ans2)

