import sys
import math
from collections import defaultdict, deque
import copy

D = {1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}

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

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))
Inst = defaultdict(int)
for ix, x in enumerate(X):
    Inst[ix] = x

# part 1
Grid = defaultdict(int)
Q = deque([((0, 0), 0, copy.copy(Inst))])
Seen = {(0, 0): 0}
Wall = set()
min_step = None
while Q:
    (r, c), num_step, P = Q.popleft()
    for com, (dr, dc) in D.items():
        nr = r + dr
        nc = c + dc
        if (nr, nc) in Wall:
            continue
        if (nr, nc) in Seen and Seen[(nr, nc)] <= num_step + 1:
            continue
        P_Next, Out, pnt, base, consume_input = \
            intcode(copy.copy(P), com, 1, 0, 0)
        assert base == 0
        assert len(Out) == 1
        out = Out.pop()
        if out == 0:
            Wall.add( (nr, nc) )
            continue
        elif out == 1:
            Q.append( ((nr, nc), num_step + 1, P_Next) )
            Seen[(nr, nc)] = num_step + 1
        elif out == 2:
            if min_step is None or num_step < min_step:
                min_step = num_step + 1
            oxr, oxc = nr, nc
            continue
        else:
            assert False
ans1 = min_step
print(ans1)

# part 2
Q = deque([((oxr, oxc), 0)])
Fill = {(oxr, oxc): 0}
while Q:
    (r, c), num_step = Q.popleft()
    for dr, dc in D.values():
        nr = r + dr
        nc = c + dc
        if (nr, nc) in Wall:
            continue
        if (nr, nc) in Fill and Fill[(nr, nc)] <= num_step + 1:
            continue
        Fill[(nr, nc)] = num_step + 1
        Q.append( ((nr, nc), num_step + 1) )
ans2 = max(Fill.values())
print(ans2)