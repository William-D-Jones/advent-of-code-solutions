import sys

# parsing
X = list(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
nrow = 40
ncol = len(X)
Grid = [X]
for r in range(1, nrow):
    row = []
    for i in range(ncol):
        left = Grid[r-1][i-1] if i-1>=0 else '.'
        right = Grid[r-1][i+1] if i+1<ncol else '.'
        center = Grid[r-1][i]
        if (left == '^' and center == '^' and right == '.') or \
        (center == '^' and right == '^' and left == '.') or \
        (left == '^' and center == '.' and right == '.') or \
        (right == '^' and center == '.' and left == '.'):
            row.append('^')
        else:
            row.append('.')
    Grid.append(row)
ans1 = \
sum( 1 if Grid[r][c] == '.' else 0 for r in range(nrow) for c in range(ncol) )
print(ans1)

# part 2
nrow = 400000
ncol = len(X)
Grid = [X]
for r in range(1, nrow):
    row = []
    for i in range(ncol):
        left = Grid[r-1][i-1] if i-1>=0 else '.'
        right = Grid[r-1][i+1] if i+1<ncol else '.'
        center = Grid[r-1][i]
        if (left == '^' and center == '^' and right == '.') or \
        (center == '^' and right == '^' and left == '.') or \
        (left == '^' and center == '.' and right == '.') or \
        (right == '^' and center == '.' and left == '.'):
            row.append('^')
        else:
            row.append('.')
    Grid.append(row)
ans2 = \
sum( 1 if Grid[r][c] == '.' else 0 for r in range(nrow) for c in range(ncol) )
print(ans2)

