import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    xs = x.split(' ')
    if xs[0] == 'rect':
        inst = ( 'rect', *map(int, xs[1].split('x')) )
    elif xs[0] == 'rotate':
        inst = ( 'rotate', xs[1], int((xs[2].split('='))[1]), int(xs[4]) )
    else:
        assert False
    Inst.append(inst)

# setup the screen
nrow = 6
ncol = 50
#nrow = 3
#ncol = 7
Screen = [ ['.' for c in range(ncol)] for r in range(nrow) ]

# part 1
for inst in Inst:
    if inst[0] == 'rect':
        for c in range(inst[1]):
            for r in range(inst[2]):
                Screen[r][c] = '#'
    elif inst[0] == 'rotate':
        if inst[1] == 'row':
            old = Screen[inst[2]]
            new = old[ -(inst[3] % ncol) : ] + old[ : -(inst[3] % ncol) ]
            Screen[inst[2]] = new
        elif inst[1] == 'column':
            old = [Screen[r][inst[2]] for r in range(nrow)]
            new = old[ -(inst[3] % nrow) : ] + old[ : -(inst[3] % nrow) ]
            for r in range(nrow):
                Screen[r][inst[2]] = new[r]
        else:
            assert False
    else:       
        assert False
ans1 = sum([1 for r in range(nrow) for c in range(ncol) if Screen[r][c] == '#'])
print(ans1)

# part 2
print('\n'.join([''.join(row) for row in Screen]))

