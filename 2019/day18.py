import sys
from collections import deque, defaultdict

D = [(-1,0), (0, 1), (1, 0), (0, -1)]
A = ord('A')
Z = ord('Z')
a = ord('a')
z = ord('z')

def find_keys(r, c, X, nrow, ncol, Key, Found):
    '''
    Find, from a given starting position, all possible keys and the minimum 
    number of steps required to get to them. Note that we only allow finding
    one key. When we find a key that was not already held, the search ends. In
    other words, we do not return paths that produce two consecutive keys.
    '''
    Start = (r, c)
    Step = {}
    Pos = {}
    Seen = set()
    Q = deque([(Start, 0)])
    while Q:
        (r, c), num_step = Q.popleft()
        step_next = num_step + 1
        for dr, dc in D:
            nr = r + dr
            nc = c + dc
            # check if the new move is valid
            if not 0 <= nr < nrow or not 0 <= nc < ncol or X[nr][nc] == '#':
                continue
            # check if we have picked up a key
            x = X[nr][nc]
            xx = ord(X[nr][nc])
            if a <= xx <= z and x not in Found:
                if x not in Step or Step[x] > step_next:
                    Step[x] = step_next
                    Pos[x] = (nr, nc)
                continue
            # if we have encountered a door, make sure we can pass it
            if A <= xx <= Z and chr(a + xx - A) not in Found:
                continue
            # check if we are on the shortest path
            State_Next = ( (nr, nc) )
            if State_Next in Seen:
                continue
            Seen.add(State_Next)
            # continue the search
            Q.append( ( (nr, nc), step_next ) )
    return Step, Pos

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
nrow = len(X)
ncol = len(X[0])
assert all(len(row) == ncol for row in X)
Key = set()
Start = []
for r in range(nrow):
    for c in range(ncol):
        if a <= ord(X[r][c]) <= z:
            Key.add(X[r][c])
        elif X[r][c] == '@':
            Start.append( (r, c) )
        else:
            assert X[r][c] == '#' or X[r][c] == '.' or A <= ord(X[r][c]) <= Z
assert len(Start) == 1
Start = Start.pop()

# part 1
min_step = None
Seen = set()
Q = deque([(Start, tuple(), 0)])
while Q:
    (r, c), Found, num_step = Q.popleft()
    if min_step is not None and num_step >= min_step:
        continue
    step_next = num_step + 1
    for dr, dc in D:
        nr = r + dr
        nc = c + dc
        # check if the new move is valid
        if not 0 <= nr < nrow or not 0 <= nc < ncol or X[nr][nc] == '#':
            continue
        # check if we have picked up a key
        x = X[nr][nc]
        xx = ord(X[nr][nc])
        if a <= xx <= z and x not in Found:
            Found_Next = tuple(sorted(list(Found) + [x]))
        else:
            Found_Next = tuple(Found)
        # if we have encountered a door, make sure we can pass it
        if A <= xx <= Z and chr(a + xx - A) not in Found_Next:
            continue
        # check if we are on the shortest path
        State_Next = ( (nr, nc), Found_Next )
        if State_Next in Seen:
            continue
        Seen.add(State_Next)
        # check if we have completed the search
        if len(Found_Next) == len(Key):
            if min_step is None or step_next < min_step:
                min_step = step_next
            continue
        # continue the search
        Q.append( ( (nr, nc), Found_Next, step_next ) )
ans1 = min_step
print(ans1)

# part 2

# update the grid
sr, sc = Start
assert X[sr][sc] == '@' and X[sr-1][sc] == '.' and X[sr+1][sc] == '.' and \
X[sr][sc+1] == '.' and X[sr][sc-1] == '.' and X[sr-1][sc-1] == '.' and \
X[sr-1][sc+1] == '.' and X[sr+1][sc-1] == '.' and X[sr+1][sc+1] == '.'
X[sr][sc] = '#'
X[sr-1][sc] = '#'
X[sr+1][sc] = '#'
X[sr][sc+1] = '#'
X[sr][sc-1] = '#'
X[sr-1][sc-1] = '@'
X[sr-1][sc+1] = '@'
X[sr+1][sc-1] = '@'
X[sr+1][sc+1] = '@'

# solve
Rob = ( (sr-1, sc+1), (sr-1, sc-1), (sr+1, sc-1), (sr+1, sc+1) )
min_step = None
Seen = {}
Q = deque([(tuple(Rob), tuple(), 0)])
while Q:
    Rob, Found, num_step = Q.popleft()
    if min_step is not None and num_step >= min_step:
        continue
    for ix, (r, c) in enumerate(Rob):
        Step, Pos = find_keys(r, c, X, nrow, ncol, Key, Found)
        for key, step_key in Step.items():
            step_next = num_step + step_key
            Rob_Next = list(Rob)
            Rob_Next[ix] = Pos[key]
            Rob_Next = tuple(Rob_Next)
            if key not in Found:
                Found_Next = tuple(sorted(list(Found) + [key]))
            else:
                Found_Next = tuple(Found)
            # check if we are on the shortest path
            State_Next = (Rob_Next, Found_Next)
            if State_Next in Seen and Seen[State_Next] <= step_next:
                continue
            Seen[State_Next] = step_next
            # check if we have completed the search
            if len(Found_Next) == len(Key):
                if min_step is None or step_next < min_step:
                    min_step = step_next
                continue
            # continue the search
            Q.append( ( Rob_Next, Found_Next, step_next ) )
print(min_step)
