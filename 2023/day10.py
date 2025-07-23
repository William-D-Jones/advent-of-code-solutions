import sys

def get_connections(coord, grid):
    op = grid[ coord[0] ][ coord[1] ]
    if op == '|':
        D = [ (-1,0), (1,0) ]
    elif op == '-':
        D = [ (0,-1), (0,1) ]
    elif op == 'L':
        D = [ (-1,0), (0,1) ]
    elif op == 'J':
        D = [ (-1,0), (0,-1) ]
    elif op == '7':
        D = [ (1,0), (0,-1) ]
    elif op == 'F':
        D = [ (1,0), (0,1) ]
    elif op == '.':
        D = []
    elif op == 'S':
        D = [ (-1,0), (1,0), (0,-1), (0,1) ]
    else:
        assert False
    Cxn = []
    for dr,dc in D:
        if 0<=coord[0]<len(grid) and 0<=coord[1]<len(grid[0]):
            Cxn.append( ( coord[0]+dr, coord[1]+dc ) )
    return Cxn

# parsing
X = [ list( l.strip() ) for l in open(sys.argv[1], 'r') ]

# find the start position
nrow = len(X)
ncol = len(X[0])
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == 'S':
            start = (r,c)
            break

# part 1 
Path = [ [start] ]
loop = False
while not loop:
    Path_Next = []
    for path in Path:
        Coord_Next = get_connections(path[-1], X)
        for coord in Coord_Next:
            if coord == (path[-2] if len(path)>=2 else None):
                continue
            # check if the next coordinate is connected to the current one
            if path[-1] in get_connections(coord, X):
                # check if we have completed a loop
                if coord not in path:
                    Path_Next.append( path+[coord] )
                elif coord == start:
                    loop = True
                    Loop = path
                    break
        if loop:
            break
    Path = Path_Next
ans1 = len(Loop)//2
print(ans1)

# part 2
set_loop = set(Loop)
set_out = set()
set_in = set()
# we will walk through the loop
# at each coordinate, look to the left or right of the coordinate
# if one side leads to the border, we know that is outside
walk = 0 # walking through the loop, our current index
walk_start = None # the index where we first identified out/inside
out = 0 # the direction leading to outside (-1 for left, 1 for right)
while walk != walk_start:
    # determine the direction to be taken to the next coordinate in the loop
    loop_now = Loop[walk]
    loop_next = Loop[walk+1] if walk<len(Loop)-1 else start
    dr = loop_next[0] - loop_now[0]
    dc = loop_next[1] - loop_now[1]
    # compute the right-hand direction relative to the current direction
    dp = ( dc , -dr )
    Step_Start = [ loop_now ]
    if X[loop_now[0]][loop_now[1]] != X[loop_next[0]][loop_next[1]]:
        Step_Start.append(loop_next)
    for step_start in Step_Start:
        # step in the perpendicular directions
        set_left = set()
        set_right = set()
        step_left = True
        step_right = True
        num_step = 1
        while step_left or step_right:
            if step_left:
                # compute the left step
                left = \
                ( step_start[0] - num_step*dp[0] , \
                step_start[1] - num_step*dp[1] )
                if left[0]<0 or left[0]>=nrow or left[1]<0 or left[1]>=ncol:
                    # the left step has reached the border
                    if out==0:
                        out = -1
                        walk_start = walk
                    step_left = False
                    set_out |= set_left
                elif left in set_loop:
                    # the left step has reached the loop
                    step_left = False
                    if out==-1:
                        set_out |= set_left
                    elif out==1:
                        set_in |= set_left
                else:
                    # we should step further left
                    set_left.add(left)
            if step_right:
                # compute the right step
                right = \
                ( step_start[0] + num_step*dp[0] , \
                step_start[1] + num_step*dp[1] )
                if right[0]<0 or right[0]>=nrow or right[1]<0 or right[1]>=ncol:
                    # the right step has reached the border
                    if out==0:
                        out = 1
                        walk_start = walk
                    step_right = False
                    set_out |= set_right
                elif right in set_loop:
                    # the right step has reached the loop
                    step_right = False
                    if out==-1:
                        set_in |= set_right
                    elif out==1:
                        set_out |= set_right
                else:
                    # we should step further right
                    set_right.add(right)
            num_step+=1
    if walk < len(Loop)-2:
        walk += 1
    else:
        walk = 0
ans2 = len(set_in)
print(ans2)
