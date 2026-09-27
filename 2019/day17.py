import sys
import math
from collections import defaultdict, deque
import copy

Mark = ['^', '>', 'v', '<']
D = [(-1, 0), (0, 1), (1, 0), (0, -1)]
Fun_Letter = {0: 'A', 1: 'B', 2: 'C'}

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

# part 1
pnt = 0
base = 0
P = copy.copy(Inst)
Txt = ''
while True:
    P, Out, pnt, base, consume_input, II = intcode(P, [None], 1, pnt, base)
    if Out:
        assert len(Out) == 1
        out = Out.pop()
        Txt += chr(out)
    else:
        break
read = False
Grid = []
for row in Txt.split('\n'):
    if read:
        if row:
            Grid.append(list(row))
        else:
            break
    else:
        if row:
            read = True
            Grid.append(list(row))
        else:
            continue
nrow = len(Grid)
ncol = len(Grid[0])
assert all(len(row) == ncol for row in Grid)
ans1 = 0
Robot = []
for r in range(1, nrow-1):
    for c in range(1, ncol-1):
        if Grid[r][c] == '#' or Grid[r][c] in Mark:
            if (Grid[r-1][c] == '#' or Grid[r-1][c] in Mark) and \
            (Grid[r+1][c] == '#' or Grid[r+1][c] in Mark) and \
            (Grid[r][c-1] == '#' or Grid[r][c-1] in Mark) and \
            (Grid[r][c+1] == '#' or Grid[r][c+1] in Mark):
                ans1 += r*c
            if Grid[r][c] in Mark:
                Robot.append( (Grid[r][c], (r, c)) )
print(ans1)

# part 2

# We make the following observations regarding the problem:
# (i) There is exactly one robot in the puzzle.
assert len(Robot) == 1
sd, (sr, sc) = Robot[0]
# (ii) We can use at most 20 characters for the routine and for each function.
# (iii) We have 3 functions--A, B, and C--which must be comma-separated. Thus,
# the main routine can have at most 10 function calls.
# (iv) A turn consists of one character--L or R. A step count consists of one
# or two characters. We know that a three-character step count must not exist
# as this would exceed the size of the grid.
assert r <= 100 and c <= 100
# (v) For the minimum function size, step counts must be separated by turns,
# both within and between functions. Therefore, assuming a one-character step 
# count, a function can contain at most 5 step counts (5 step + 4 turn + 
# 8 comma <= 20), and in this case it would begin and end in a step.
# (vi) The grid contains only 2 termini (squares with only one possible
# direction of movement). We start on one of these termini.
Term = []
for r in range(nrow):
    for c in range(ncol):
        if Grid[r][c] == '#' or Grid[r][c] in Mark:
            mv = sum([1 for dr, dc in D if 0 <= r+dr < nrow and \
            0 <= c+dc < ncol and \
            (Grid[r+dr][c+dc] == '#' or Grid[r+dr][c+dc] in Mark)])
            if mv == 1:
                Term.append( (r, c) )
assert (sr, sc) in Term
# (vii) While we do not need to find the shortest possible path, certain
# operations that unnecessarily lengthen the path can be safely avoided. For
# example, unnecessary turns or breaking up step counts do not contribute to
# finding an accceptable path.
# (viii) The setup of the grid is all that guarantees a solution to the problem.
# By examining the grid visually, it is clear that
# one possible path is to walk in the current direction until we cannot walk
# anymore, and then turn in the only possible direction.
# print('\n'.join([''.join(row) for row in Grid]))

# produce the final set of commands
r, c = sr, sc
Path = [(r, c)]
Grid[sr][sc] = '#'
di = Mark.index(sd)
dr, dc = D[di]
step = 0
Com = []
# step forward as long as possible
while True:
    if 0 <= r+dr < nrow and 0 <= c+dc < ncol and Grid[r+dr][c+dc] == '#':
        # step forward
        step += 1
        r = r+dr
        c = c+dc
        Path.append( (r, c) )
    else:
        # turn left or right
        nd_left = (di - 1) % len(D)
        dr_left, dc_left = D[nd_left]
        nd_right = (di + 1) % len(D)
        dr_right, dc_right = D[nd_right]
        if 0 <= r+dr_left < nrow and 0 <= c+dc_left < ncol and \
        Grid[r+dr_left][c+dc_left] == '#':
            # turn left
            di = nd_left
            dr, dc = D[di]
            if step > 0:
                Com.append(str(step))
            Com.append('L')
            step = 0
        elif 0 <= r+dr_right < nrow and 0 <= c+dc_right < ncol and \
        Grid[r+dr_right][c+dc_right] == '#':
            # turn right
            di = nd_right
            dr, dc = D[di]
            if step > 0:
                Com.append(str(step))
            Com.append('R')
            step = 0
        else:
            # the grid is complete
            if step > 0:
                Com.append(str(step))
            break
# produce the routine and functions
Fun_Call = {} # start_index: function_index
Fun_Def = []
ix_start = 0
len_fun = 1
Q = set(range(0, len(Com)))
while Q:
    ix_start = min(Q)
    Fun = Com[ix_start : ix_start + len_fun]
    # check if the function exists anywhere else in commands
    found = False
    for ix_check in range(ix_start + len_fun, len(Com) - len_fun + 1):
        if ix_check in Fun_Call:
            ix_check += len(Fun_Def[Fun_Call[ix_check]])
            continue
        if Com[ix_check : ix_check + len_fun] == Fun:
            if not found:
                Found_Ix = [ix_start]
                Found_Fun = list(Fun)
                found = True
            Found_Ix.append(ix_check)
            ix_check += len_fun
    # check if the longest possible function has been found
    if found:
        len_fun += 1
        if ix_start + len_fun - 1 not in Q:
            found = False
    if not found:
        Fun_Def.append(Found_Fun)
        for found_ix in Found_Ix:
            Fun_Call[found_ix] = len(Fun_Def) - 1
            for q in range(found_ix, found_ix + len(Found_Fun)):
                Q.remove(q)
        len_fun = 1
# construct the routine
Routine = []
for ix_fun in sorted(Fun_Call.keys()):
    Routine.append(Fun_Letter[Fun_Call[ix_fun]])
In_Char = [','.join(Routine) + '\n']
for Fun in Fun_Def:
    In_Char.append(','.join(Fun) + '\n')
In_Char.append('n\n')
In_Num = []
for char in ''.join(In_Char):
    In_Num.append(ord(char))

# run the program
pnt = 0
base = 0
P = copy.copy(Inst)
P[0] = 2
II = copy.copy(In_Num)
while True:
    P, Out, pnt, base, consume_input, II = \
    intcode(P, II, 1, pnt, base)
    try:
        print(''.join([chr(out) for out in Out]), end = '')
    except:
        ans2 = Out[0]
        break
print(ans2)
