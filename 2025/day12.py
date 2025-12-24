import sys

# parsing
X = open(sys.argv[1], 'r').read().strip().split('\n\n')
Pres = {}
sz = 3
for x in X[:-1]:
    xs = x.split('\n')
    ix = int(xs[0][:-1])
    nrow = len(xs[1:])
    ncol = len(xs[1:][0])
    assert all(len(xs[1:][i])==ncol for i in range(0,nrow))
    assert nrow == ncol == sz
    pres = []
    for r in range(nrow):
        for c in range(ncol):
            char = xs[1:][r][c:c+1]
            if char == '.':
                continue
            elif char == '#':
                pres.append( (r,c) )
            else:
                assert False
    Pres[ix] = tuple(sorted(pres))
Reg = []
for x in X[-1].split('\n'):
    dim, pres = x.split(': ')
    Reg.append( \
    (tuple(map(int,dim.split('x'))), tuple(map(int,pres.split(' ')))) )

# part 1
ans1 = 0
for dim, pres in Reg:
    # determine the free area
    A = dim[0] * dim[1]
    # determine the area consumed by the presents
    P = sum(len(Pres[ix]) * n for ix,n in enumerate(pres))
    # determine the number of presents that can be accommodated without overlap
    n_adj = (dim[0] // sz) * (dim[1] // sz)
    if P > A:
        continue
    elif n_adj >= sum(n for ix,n in enumerate(pres)):
        ans1 += 1
    else:
        assert False
print(ans1)

