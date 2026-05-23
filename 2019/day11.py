import sys
import math
from collections import defaultdict
import copy

D = [(-1, 0), (0, 1), (1, 0), (0, -1)]

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

def intcode(P, ii, max_out, pnt, base):
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
        if len(Out) >= max_out:
            break
    return P, Out, pnt, base

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))
Inst = defaultdict(int)
for ix, x in enumerate(X):
    Inst[ix] = x

# part 1
P = copy.copy(Inst)
Color = defaultdict(int)
Painted = set()
r, c = (0, 0)
di = 0
pnt = 0
base = 0
while True:
    color = Color[(r, c)]
    P, Out, pnt, base = intcode(P, color, 2, pnt, base)
    if len(Out) == 2:
        paint, turn = Out
        Color[(r, c)] = paint
        Painted.add( (r,c) )
        if turn == 0:
            di = (di - 1) % len(D)
        elif turn == 1:
            di = (di + 1) % len(D)
        else:
            assert False
        dr, dc = D[di]
        r += dr
        c += dc
    else:
        break
ans1 = len(Color)
print(ans1)

# part 2
P = copy.copy(Inst)
Color = defaultdict(int)
Painted = set()
r, c = (0, 0)
Color[(r,c)] = 1
di = 0
pnt = 0
base = 0
while True:
    color = Color[(r, c)]
    P, Out, pnt, base = intcode(P, color, 2, pnt, base)
    if len(Out) == 2:
        paint, turn = Out
        Color[(r, c)] = paint
        Painted.add( (r,c) )
        if turn == 0:
            di = (di - 1) % len(D)
        elif turn == 1:
            di = (di + 1) % len(D)
        else:
            assert False
        dr, dc = D[di]
        r += dr
        c += dc
    else:
        break
r_min = min(r for (r,c) in Color)
r_max = max(r for (r,c) in Color)
c_min = min(c for (r,c) in Color)
c_max = max(c for (r,c) in Color)
Grid = [[' '] * (c_max - c_min + 1) for r in range(r_min, r_max + 1)]
for r in range(r_min, r_max + 1):
    r_grid = r - r_min
    for c in range(c_min, c_max + 1):
        c_grid = c - c_min
        if Color[(r, c)] == 1:
            Grid[r_grid][c_grid] = '\u25AC'
ans2 = '\n'.join([''.join(row) for row in Grid])
print(ans2)
