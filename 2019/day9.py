import sys
import math
from collections import defaultdict
import copy

def get_mode(inst, jmp):
    Mode = []
    for ix in range(jmp-1):
        mode = inst - (inst // 10) * 10
        inst //= 10
        Mode.append(mode)
    return Mode

def get_parameters(P, pnt, base, Mode):
    Param = []
    for ix, mode in enumerate(Mode):
        if mode == 0:
            param = P[P[pnt+ix+1]]
        elif mode == 1:
            param = P[pnt+ix+1]
        elif mode == 2:
            param = P[base + P[pnt+ix+1]]
        else:
            assert False
        Param.append(param)
    return Param

def intcode(P, ii):
    pnt = 0
    base = 0
    Out = []
    while True:
        # get the instruction
        inst = P[pnt]
        # parse the instruction
        op = inst - (inst // 100) * 100
        inst //= 100
        # execute the instruction
        if op == 1: # addition
            jmp = 4
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Mode[-1] == 0:
                P[P[pnt+jmp-1]] = sum(Param[:-1])
            elif Mode[-1] == 2:
                P[base + P[pnt+jmp-1]] = sum(Param[:-1])
            else:
                assert False
        elif op == 2: # multiplication
            jmp = 4
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Mode[-1] == 0:
                P[P[pnt+jmp-1]] = math.prod(Param[:-1])
            elif Mode[-1] == 2:
                P[base + P[pnt+jmp-1]] = math.prod(Param[:-1])
            else:
                assert False
        elif op == 3: # input
            jmp = 2
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Mode[-1] == 0:
                P[P[pnt+1]] = ii
            elif Mode[-1] == 2:
                P[base + P[pnt+1]] = ii
            else:
                assert False
        elif op == 4: # output
            jmp = 2
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            Out.append(Param[-1])
        elif op == 5: # jump if true
            jmp = 3
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Param[0] != 0:
                pnt = Param[1]
                jmp = 0
            else:
                pass
        elif op == 6: # jump if false
            jmp = 3
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Param[0] == 0:
                pnt = Param[1]
                jmp = 0
            else:
                pass
        elif op == 7: # is less than
            jmp = 4
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Mode[-1] == 0:
                P[P[pnt+jmp-1]] = 1 * (Param[0] < Param[1])
            elif Mode[-1] == 2:
                P[base + P[pnt+jmp-1]] = 1 * (Param[0] < Param[1])
            else:
                assert False
        elif op == 8: # is equal to
            jmp = 4
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            if Mode[-1] == 0:
                P[P[pnt+jmp-1]] = 1 * (Param[0] == Param[1])
            elif Mode[-1] == 2:
                P[base + P[pnt+jmp-1]] = 1 * (Param[0] == Param[1])
            else:
                assert False
        elif op == 9: # relative base offset
            jmp = 2
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            base += Param[-1]
        elif op == 99: # halt
            jmp = 1
            Mode = get_mode(inst, jmp)
            Param = get_parameters(P, pnt, base, Mode)
            break
        else:
            assert False
        pnt += jmp
    return P, Out

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))
D = defaultdict(int)
for ix, x in enumerate(X):
    D[ix] = x

# part 1
P = copy.copy(D)
P, Out = intcode(P, 1)
assert len(Out) == 1
ans1 = Out[-1]
print(ans1)

# part 2
P = copy.copy(D)
P, Out = intcode(P, 2)
assert len(Out) == 1
ans2 = Out[-1]
print(ans2)
