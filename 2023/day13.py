import sys

def count_differences(grid, line, direction):
    """
    Count the number of different entries in a grid across the line of
    reflection given by line.

    line:       the number of rows above a horizontal line or to the left of a 
                vertical line
    direction:  either "v" or "h" for vertical or horizontal
    """

    diff = 0
    nrow = len(grid)
    ncol = len(grid[0])
    if direction == "h":
        ref = min(line, nrow-line)
        for xr in range(ref):
            for xc in range(ncol):
                if grid[line-1-xr][xc] != grid[line+xr][xc]:
                    diff += 1
    elif direction == "v":
        ref = min(line, ncol-line)
        for xr in range(nrow):
            for xc in range(ref):
                if grid[xr][line-ref:line][xc] != \
                (grid[xr][line:line+ref])[::-1][xc]:
                    diff += 1
    else:
        assert False
    return diff

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Grid = []
for grid in ( '\n'.join(X) ).split('\n\n'):
    Grid.append([list(line) for line in grid.split('\n')])

# parts 1 and 2
Ref1 = []
Ref2 = []
for grid in Grid:
    nrow = len(grid)
    ncol = len(grid[0])
    for i in range(1, nrow):
        if count_differences(grid, i, "h") == 0:
            Ref1.append( ("h", i) )
        if count_differences(grid, i, "h") == 1:
            Ref2.append( ("h", i) )
    for i in range(1, ncol):
        if count_differences(grid, i, "v") == 0:
            Ref1.append( ("v", i) )
        if count_differences(grid, i, "v") == 1:
            Ref2.append( ("v", i) )
ans1 = 0
for ref in Ref1:
    if ref[0] == "v":
        ans1 += ref[1]
    elif ref[0] == "h":
        ans1 += 100 * ref[1]
    else:
        assert False
ans2 = 0
for ref in Ref2:
    if ref[0] == "v":
        ans2 += ref[1]
    elif ref[0] == "h":
        ans2 += 100 * ref[1]
    else:
        assert False
print(ans1)
print(ans2)
