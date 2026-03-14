import sys
import re
from collections import deque, defaultdict

def solve_monkeys(Yell, Dep, Op):
    Q = deque(Yell.keys())
    while Q:
        mon_in = Q.pop()
        for mon_out in Dep[mon_in]:
            par0, op, par1 = Op[mon_out]
            if par0 in Yell and par1 in Yell:
                if op == '+':
                    Yell[mon_out] = Yell[par0] + Yell[par1]
                elif op == '*':
                    Yell[mon_out] = Yell[par0] * Yell[par1]
                elif op == '-':
                    Yell[mon_out] = Yell[par0] - Yell[par1]
                elif op == '/':
                    Yell[mon_out] = Yell[par0] // Yell[par1]
                else:
                    assert False
                Q.append(mon_out)
    return Yell

# parsing
X = [ line.strip().split(': ') for line in open(sys.argv[1], 'r') ]
Dep = defaultdict(list)
Yell = {}
Op = {}
for mon,x in X:
    eq = x.split(' ')
    if len(eq) == 1:
        Yell[mon] = int(eq[0])
    else:
        par0, op, par1 = eq
        Dep[par0].append(mon)
        Dep[par1].append(mon)
        Op[mon] = tuple(eq)

# part 1
Yell1 = solve_monkeys(dict(Yell), Dep.copy(), dict(Op))
ans1 = Yell1['root']
print(ans1)

# part 2
assert all(len(Dep[mon])==1 for mon in Dep)
if 'humn' in Op:
    Op.pop('humn')
if 'humn' in Dep:
    Dep.pop('humn')
if 'humn' in Yell:
    Yell.pop('humn')
Yell2 = solve_monkeys(dict(Yell), Dep.copy(), dict(Op))
par0, op, par1 = Op['root']
if par0 in Yell2:
    unk = par1
    res = Yell2[par0]
elif par1 in Yell2:
    unk = par0
    res = Yell2[par1]
else:
    assert False
Yell2[unk] = res
while unk != 'humn':
    par0, op, par1 = Op[unk]
    if par0 in Yell2:
        unk = par1
        kn = Yell2[par0]
    elif par1 in Yell2:
        unk = par0
        kn = Yell2[par1]
    else:
        assert False
    if op == '+':
        res -= kn
    elif op == '*':
        res //= kn
    elif op == '-':
        if par1 in Yell2:
            res += kn
        else:
            res = kn - res
    elif op == '/':
        if par1 in Yell2:
            res *= kn
        else:
            res = kn // res
    else:
        assert False
    Yell2[unk] = res
ans2 = Yell2['humn']
print(ans2)

