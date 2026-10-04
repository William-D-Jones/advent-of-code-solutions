import sys
import math
from collections import defaultdict, deque
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

def intcode(P, II, max_out, pnt, base):
    Out = []
    consume_input = False
    II = copy.copy(II)
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
                ii = II.pop(0)
                P[P[pnt+1]] = ii
            elif Mode[-1] == 2:
                ii = II.pop(0)
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
    return P, Out, pnt, base, consume_input, II

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))
Inst = defaultdict(int)
for ix, x in enumerate(X):
    Inst[ix] = x

# return the beam state for a given row and column, with caches
BEAM = {} # cache of all beam states accessed
def get_beam(r, c):
    if (r, c) in BEAM:
        return BEAM[(r, c)]
    P, Out, pnt, base, consume_input, II = \
    intcode(copy.copy(Inst), [c, r], 1, 0, 0)
    if Out:
        assert len(Out) == 1
        out = int(Out.pop())
        assert out == 0 or out == 1
        BEAM[(r, c)] = out
        return out
    else:
        assert False

# part 1
r = 0
c = 0
r1 = 50
c1 = 50
ans1 = 0
for r in range(r1):
    for c in range(c1):
        out = get_beam(r, c)
        if out == 1:
            ans1 += 1
print(ans1)

# part 2

# Based on the problem statement and the example, the beam spreads out from the
# emitter, and once the beam becomes sufficiently wide, there should be no
# discontinuities in the beam. However, before the beam becomes sufficiently
# wide, there may be gaps. Fortunately, in part 1 we have recorded the path of
# the beam, and we assume that we have identified the beam.
assert ans1 > 0
# Since we have identified the beam, we can now test if we have a sufficiently
# large region from which to begin the search. Rank the points by proximity to
# the emitter, and do a flow-fill from each point. To solve the problem, there
# must be at least one point within the beam from which a flow-fill leads to
# the bottom edge or right edge of the board.
Q = set((r, c) for (r, c), out in BEAM.items() if out == 1)
QR = deque((r, c) for dist, (r,c) in sorted((r+c, (r, c)) for (r, c) in Q))
D = [(0, 1), (1, 0), (0, -1), (-1, 0)]
Reg = {}
while QR:
    sr, sc = QR.popleft()
    if (sr, sc) not in Q:
        continue
    reg = 1
    F = deque([(sr, sc)])
    Q.remove( (sr, sc) )
    overflow = False
    while F:
        r, c = F.popleft()
        for dr, dc in D:
            nr = r + dr
            nc = c + dc
            if nr >= r1 or nc >= c1:
                overflow = True
            if (nr, nc) not in Q:
                continue
            F.append( (nr, nc) )
            Q.remove( (nr, nc) )
            reg += 1
    Reg[(sr, sc)] = (reg, overflow)
Start = [(r, c) for (r, c), (sz, overflow) in Reg.items() if overflow]
assert len(Start) == 1
sr, sc = Start.pop()

# having found the starting position, identify the desired region
sz_r = 100
sz_c = 100
r = sr - 1
c_min = sc
found = False
while not found:
    # find the highest valid row with sufficient room to the right
    valid_row = False
    while not valid_row:
        r += 1
        while get_beam(r, c_min) == 0:
            c_min += 1
        valid_row = \
        all(get_beam(r, tc) == 1 for tc in range(c_min, c_min + sz_c))
    # find the size of that row
    sz_valid_row = sz_c
    while get_beam(r, c_min + sz_valid_row) == 1:
        sz_valid_row += 1
    # find the left-most valid column with sufficient room below
    c = c_min
    while c_min <= c < c_min + sz_valid_row - sz_c + 1:
        if all(get_beam(tr, c) == 1 for tr in range(r, r + sz_r)):
            found = True
            break
        c += 1
ans2 = 10000 * c + r
print(ans2)
