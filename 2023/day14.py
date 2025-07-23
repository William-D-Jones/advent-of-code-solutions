import sys
from copy import deepcopy

def tilt(grid, dxn):
    """
    Tilt the grid in the indicated direction.
    dxn: a string indicating the direction: N, W, S, E
    """

    # identify the direction of travel along rows and columns
    # we walk the opposite direction to identify free squares
    if dxn == "N":
        dr = 1
        dc = 1
    elif dxn == "S":
        dr = -1
        dc = 1
    elif dxn == "W":
        dr = 1
        dc = 1
    elif dxn == "E":
        dr = 1
        dc = -1
    else:
        assert False

    # set up a list of free squares
    # lower indices are filled first
    if dxn == "N" or dxn == "S":
        Free = [ [] for _ in range(ncol)]
    elif dxn == "E" or dxn == "W":
        Free = [ [] for _ in range(nrow)]

    # step along rows and columns looking for rounded stones
    for xr in list(range(nrow))[::dr]:
        for xc in list(range(ncol))[::dc]:
            if grid[xr][xc] == ".":
                if dxn == "N" or dxn == "S":
                    Free[xc].append(xr)
                elif dxn == "E" or dxn == "W":
                    Free[xr].append(xc)
            elif grid[xr][xc] == "#":
                if dxn == "N" or dxn == "S":
                    Free[xc] = []
                elif dxn == "E" or dxn == "W":
                    Free[xr] = []
            elif grid[xr][xc] == "O":
                if dxn == "N" or dxn == "S":
                    if len(Free[xc]) > 0:
                        grid[xr][xc] = "."
                        grid[ Free[xc].pop(0) ][xc] = "O"
                        Free[xc].append(xr)
                elif dxn == "E" or dxn == "W":
                    if len(Free[xr]) > 0:
                        grid[xr][xc] = "."
                        grid[xr][ Free[xr].pop(0) ] = "O"
                        Free[xr].append(xc)
                else:
                    assert False
            else:
                assert False
    return grid 

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# part 1
ans1 = 0
Xn = tilt(deepcopy(X), "N")
for xr in range(nrow):
    for xc in range(ncol):
        if Xn[xr][xc] == "O":
            ans1 += nrow-xr
print(ans1)

# part 2
Xc = deepcopy(X)
Xl = []
rep = -1
n = 1000000000
#n = 10
for i in range(n):
    Xc = tilt(Xc, "N")
    Xc = tilt(Xc, "W")
    Xc = tilt(Xc, "S")
    Xc = tilt(Xc, "E")
    # check if we are starting to repeat
    for j, x in enumerate(Xl):
        if x == Xc:
            rep = j
            break
    if rep == -1:
        Xl.append(deepcopy(Xc))
    else:
        break
# identify the correct pattern after n cycles
cyc = i - rep # the number of entries before recycling
X2 = Xl[rep + ( (n - 1 - rep) % cyc )]
# calculate the weight
ans2 = 0
for xr in range(nrow):
    for xc in range(ncol):
        if X2[xr][xc] == "O":
            ans2 += nrow-xr
print(ans2)

