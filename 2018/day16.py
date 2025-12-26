import sys
import re
from collections import deque

CODE = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori', \
'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

def ex(Op, Reg):
    op, A, B, C = Op
    if op == 'addr':
        Reg[C] = Reg[A] + Reg[B]
    elif op == 'addi':
        Reg[C] = Reg[A] + B
    elif op == 'mulr':
        Reg[C] = Reg[A] * Reg[B]
    elif op == 'muli':
        Reg[C] = Reg[A] * B
    elif op == 'banr':
        Reg[C] = Reg[A] & Reg[B]
    elif op == 'bani':
        Reg[C] = Reg[A] & B
    elif op == 'borr':
        Reg[C] = Reg[A] | Reg[B]
    elif op == 'bori':
        Reg[C] = Reg[A] | B
    elif op == 'setr':
        Reg[C] = Reg[A]
    elif op == 'seti':
        Reg[C] = A
    elif op == 'gtir':
        Reg[C] = 1 if A > Reg[B] else 0
    elif op == 'gtri':
        Reg[C] = 1 if Reg[A] > B else 0 
    elif op == 'gtrr':
        Reg[C] = 1 if Reg[A] > Reg[B] else 0
    elif op == 'eqir':
        Reg[C] = 1 if A == Reg[B] else 0
    elif op == 'eqri':
        Reg[C] = 1 if Reg[A] == B else 0
    elif op == 'eqrr':
        Reg[C] = 1 if Reg[A] == Reg[B] else 0
    else:
        assert False
    return Reg

# parsing
X = '\n'.join([ l.strip() for l in open(sys.argv[1], 'r') ])
X1, X2, = X.split('\n\n\n\n')
Test = []
for x1 in X1.split('\n\n'):
    xb, xo, xa = x1.split('\n')
    lb = list(map(int, \
    re.match('^(Before|After):( +)\\[([0-9, ]+)\\]$', xb).group(3).split(', ')\
    ))
    lo = list(map(int, xo.split()))
    la = list(map(int, \
    re.match('^(Before|After):( +)\\[([0-9, ]+)\\]$', xa).group(3).split(', ')\
    ))
    Reg0 = {i: val for i,val in enumerate(lb)}
    Reg1 = {i: val for i,val in enumerate(la)}
    Test.append([Reg0, lo, Reg1])
Inst = []
for x2 in X2.split('\n'):
    Inst.append(list(map(int, x2.split())))

# part 1
ans1 = 0
Num = {}
for Reg0, Op, Reg1 in Test:
    n = 0
    num, A, B, C = Op
    if num not in Num.keys():
        Num[num] = set(CODE)
    for op in CODE:
        Reg = ex([op, A, B, C], dict(Reg0))
        if Reg == Reg1:
            n += 1
        else:
            Num[num] -= set([op])
    if n >= 3:
        ans1 += 1
print(ans1)

# part 2
# match operations to numbers
O2N = {op: -1 for op in CODE}
Q = deque(CODE)
while Q:
    op = Q.popleft()
    for num,Op in Num.items():
        if op in Op and len(Op) == 1:
            O2N[op] = num
        Num[num] -= set([op for op,num in O2N.items() if num != -1])
    if O2N[op] == -1:
        Q.append(op)
N2O = {num: op for op,num in O2N.items()}
# execute the program
Reg = {0: 0, 1: 0, 2: 0, 3: 0}
for num, A, B, C in Inst:
    Reg = ex([N2O[num], A, B, C], Reg)
ans2 = Reg[0]
print(ans2)

