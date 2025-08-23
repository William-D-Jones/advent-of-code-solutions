import sys

def run(Inst):
    Reg = {'X': 1}
    Hist = []
    cyc = 0
    for inst in Inst:
        if inst[0] == 'addx':
            for i in range(2):
                cyc += 1
                Hist.append(Reg['X'])
            Reg['X'] += inst[1]
        elif inst[0] == 'noop':
            for i in range(1):
                cyc += 1
                Hist.append(Reg['X'])
        else:
            assert False
    return Hist

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    xs = x.split()
    if len(xs)==1:
        Inst.append(tuple(xs))
    elif len(xs)>1:
        Inst.append( (xs[0], int(xs[1])) )

# part 1
Hist = run(Inst)
ans1 = 0
for i in (20,60,100,140,180,220):
    ans1 += Hist[i-1] * i
print(ans1)

# part 2
nrow = 6
ncol = 40
Pic = [['.' for c in range(ncol)] for r in range(nrow)]
assert len(Hist) == nrow*ncol
for i in range(nrow*ncol):
    r = i // ncol
    c = i % ncol
    for s in range(-1, 2):
        if Hist[i]+s == c:
            Pic[r][c] = '#'
print('\n'.join([''.join(row) for row in Pic]))
        
