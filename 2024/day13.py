import sys
from collections import defaultdict

# parsing
X = open(sys.argv[1], 'r').read().strip()
X = [x.split('\n') for x in X.split('\n\n')]
Machine = []
for x in X:
    machine = defaultdict(int)
    As = x[0].split()
    Bs = x[1].split()
    Ps = x[2].split()
    machine['Ax'] = int(As[2][2:-1])
    machine['Ay'] = int(As[3][2:])
    machine['Bx'] = int(Bs[2][2:-1])
    machine['By'] = int(Bs[3][2:])
    machine['Px'] = int(Ps[1][2:-1])
    machine['Py'] = int(Ps[2][2:])
    Machine.append(machine)

# part 1
ans1 = 0
for machine in Machine:
    nbf = ( machine['Px'] * machine['Ay'] - machine['Py'] * machine['Ax'] ) /\
    ( machine['Bx'] * machine['Ay'] - machine['By'] * machine['Ax'] )
    naf = ( machine['Px'] - nbf * machine['Bx'] ) / machine['Ax']
    nb = int(nbf)
    na = int(naf)
    if na == naf and nb == nbf and 0 <= na <= 100 and 0 <= nb <= 100:
        tokens = na * 3 + nb * 1
        ans1 += tokens
print(ans1)

# part 2
ans2 = 0
add = 10000000000000
for machine in Machine:
    nbf = ( (machine['Px']+add) * machine['Ay'] - \
    (machine['Py']+add) * machine['Ax'] ) /\
    ( machine['Bx'] * machine['Ay'] - machine['By'] * machine['Ax'] )
    naf = ( (machine['Px']+add) - nbf * machine['Bx'] ) / machine['Ax']
    nb = int(nbf)
    na = int(naf)
    if na == naf and nb == nbf and 0 <= na and 0 <= nb:
        tokens = na * 3 + nb * 1
        ans2 += tokens
print(ans2)
