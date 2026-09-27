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

def intcode(P, ii, max_out, pnt, base):
    Out = []
    consume_input = False
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
            consume_input = True
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
    return P, Out, pnt, base, consume_input

def print_screen(Screen):
    r_min = min(r for (r,c) in Screen)
    r_max = max(r for (r,c) in Screen)
    c_min = min(c for (r,c) in Screen)
    c_max = max(c for (r,c) in Screen)
    Disp = [['.'] * (c_max - c_min + 1) for r in range(r_min, r_max + 1)]
    for (r, c), tile in Screen.items():
        if tile == 0:
            pass
        elif tile == 1:
            Disp[r-r_min][c-c_min] = '#'
        elif tile == 2:
            Disp[r-r_min][c-c_min] = 'O'
        elif tile == 3:
            Disp[r-r_min][c-c_min] = 'X'
        elif tile == 4:
            Disp[r-r_min][c-c_min] = '^'
    print('\n'.join(''.join(row) for row in Disp))
    return

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))
Inst = defaultdict(int)
for ix, x in enumerate(X):
    Inst[ix] = x

# part 1
P = copy.copy(Inst)
Screen = defaultdict(int)
pnt = 0
base = 0
while True:
    P, Out, pnt, base, consume_input = intcode(P, None, 3, pnt, base)
    if len(Out) == 3:
        c, r, tile = Out
        Screen[(r, c)] = tile
    else:
        break
ans1 = sum(1 for (r,c) in Screen if Screen[(r,c)] == 2)
print(ans1)

# part 2
P = copy.copy(Inst)
P[0] = 2
Screen = defaultdict(int)
pnt = 0
base = 0
ii = None
score = None
while True:
    P, Out, pnt, base, consume_input = intcode(P, ii, 3, pnt, base)
    if consume_input:
        #print_screen(Screen)
        pass
    if len(Out) == 3:
        c, r, tile = Out
        if c == -1 and r == 0:
            score = tile
        else:
            Screen[(r, c)] = tile
            Ball = [(r,c) for (r,c), tile in Screen.items() if tile == 4]
            assert 0 <= len(Ball) <= 1
            Paddle = [(r,c) for (r,c), tile in Screen.items() if tile == 3]
            assert 0 <= len(Paddle) <= 1
            if len(Ball) == 1 and len(Paddle) == 1:
                if Ball[0][1] > Paddle[0][1]:
                    ii = 1
                elif Ball[0][1] < Paddle[0][1]:
                    ii = -1
                else:
                    ii = 0
    else:
        break
ans2 = score
print(score)