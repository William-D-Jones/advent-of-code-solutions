import sys
from collections import deque

D = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]

def explore_grid(X, S, loop = False, nstep = 0):
    """
    Explore a grid X starting at position S. We can step to positions in the 
    grid marked ., but not those marked #.

    X:  a grid
    S:  a tuple giving the starting position in the format (row, column)

    Returns a dictionary of positions. Each key is a position (r,c) that gives
    the number of steps required to walk from S to (r,c).
    """

    nrow = len(X) # number of rows in the garden
    ncol = len(X[0]) # number of columns in the garden
    # the Steps_Dict object records the positions (r,c) that succeed
    # each position (r,c) gives the number of steps required to walk to (r,c)
    Steps_Dict = {}
    Pos = deque([S]) # the current coordinates of our walks
    Steps = deque([0]) # the current number of steps on our walks

    # walk through the garden
    while Pos:
        pos = Pos.popleft()
        steps = Steps.popleft()
        steps += 1
        for dr, dc in D:
            rnext = pos[0] + dr
            cnext = pos[1] + dc
            rrem = rnext % nrow if loop else rnext
            crem = cnext % ncol if loop else cnext
            if 0 <= rrem < nrow and 0 <= crem < ncol and \
            X[ rrem ][ crem ] == '.' and \
            (rnext, cnext) not in Steps_Dict.keys():
                if steps % 2 == nstep % 2:
                    Steps_Dict[ (rnext, cnext) ] = steps
                if steps <= nstep:
                    Pos.append( (rnext, cnext) )
                    Steps.append( steps)

    return Steps_Dict

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == 'S':
            S = (r, c)
            X[r][c] = '.'

# part 1
nstep1 = 64
Steps_Dict_1 = explore_grid(X, S, loop = False, nstep = nstep1)
ans1 = len(Steps_Dict_1)
print(ans1)

# part 2

# I made the following observations about the grid:

# (1) The top, bottom, left, and right edges of the grid are free
assert( all(char == '.' for char in X[0]) )
assert( all(char == '.' for char in X[nrow - 1]) )
assert( all(X[r][0] == '.' for r in range(nrow)) )
assert( all(X[r][ncol-1] == '.' for r in range(nrow)) )

# (2) The middle row and middle column of the grid are free, and S is center
assert( all(char == '.' for char in X[nrow//2]) )
assert( all(X[r][ncol//2] for r in range(nrow)) )
assert( S == (nrow//2, ncol//2) )

# (3) The grid is square. Therefore, if we define the starting grid as (0,0)
# and go to a midpoint of that grid, the number of steps required to go to the
# same midpoint of grid (gr,gc) is given by |gr|*|gc|*k where k is the side
# length of a grid.
assert( nrow==ncol )

nstep2 = 26501365
# after leaving the starting grid, how many steps remain?
nleave = max( 0, nstep2 - (nrow//2+1) )
# after leaving the starting grid, how many additional edges can we travel?
nedge = max( 0, nleave // nrow )
# after traveling this number of edges, how many steps remain?
nrem = max( 0, nstep2 - (nrow//2+1) - nrow*nedge )

# run a simulation describing the behavior of the elf if nedge were 1
# this fully describes what any explored region, of any size, will look like
Steps_Dict_Sim_1 = \
explore_grid( X, S, loop = True, nstep = nrem + (nrow//2+1) + nrow * 1)
# divide the simulation into grids, collecting the plots in each grid
Plots_Dict_Sim_1 = {}
for gr in range(-2, 3):
    for gc in range(-2, 3):
        nplot = \
        len([(r,c) for (r,c) in Steps_Dict_Sim_1.keys() if \
        gr*nrow<=r<(gr+1)*nrow and gc*ncol<=c<(gc+1)*ncol])
        Plots_Dict_Sim_1[ (gr,gc) ] = nplot

# collect the interior grids
ngrid_even_row_S = ( 2*nedge + 1 + (nedge+1)%2 ) // 2
ngrid_odd_row_S = ( 2 * nedge + 1 ) - ngrid_even_row_S
ngrid_full_even = (ngrid_even_row_S-1) * (ngrid_even_row_S) + ngrid_even_row_S
ngrid_full_odd  = (ngrid_odd_row_S-1) * (ngrid_odd_row_S) + ngrid_odd_row_S

# add up the plots visited
ans2 = 0
ans2 += Plots_Dict_Sim_1[(0,0)] * ngrid_full_even # even-numbered interior grids
ans2 += Plots_Dict_Sim_1[(0,1)] * ngrid_full_odd # odd-numbered interior grids
ans2 += Plots_Dict_Sim_1[(2,0)] # top edge grid
ans2 += Plots_Dict_Sim_1[(0,2)] # right edge grid
ans2 += Plots_Dict_Sim_1[(-2,0)] # bottom edge grid
ans2 += Plots_Dict_Sim_1[(0,-2)] # left edge grid
ans2 += Plots_Dict_Sim_1[(-1,2)] * (nedge+1) # top right outer edge
ans2 += Plots_Dict_Sim_1[(-1,1)] * nedge # top right inner edge
ans2 += Plots_Dict_Sim_1[(1,2)] * (nedge+1) # bottom right outer edge
ans2 += Plots_Dict_Sim_1[(1,1)] * nedge # bottom right inner edge
ans2 += Plots_Dict_Sim_1[(2,-1)] * (nedge+1) # bottom left outer edge
ans2 += Plots_Dict_Sim_1[(1,-1)] * nedge # bottom right inner edge
ans2 += Plots_Dict_Sim_1[(-2,-1)] * (nedge+1) # top left outer edge
ans2 += Plots_Dict_Sim_1[(-1,-1)] * nedge # top left inner edge
print(ans2)

