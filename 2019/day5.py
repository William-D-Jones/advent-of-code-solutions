import sys

def get_mode(inst, jmp):
    Mode = []
    for ix in range(jmp-1):
        mode = inst - (inst // 10) * 10
        inst //= 10
        Mode.append(mode)
    return Mode

def intcode(P, ii):
    pnt = 0
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
            res = 0
            Mode = get_mode(inst, jmp)
            assert Mode[-1] == 0
            for ix in range(jmp-2):
                mode = Mode[ix]
                if mode == 0:
                    res += P[P[pnt+ix+1]]
                elif mode == 1:
                    res += P[pnt+ix+1]
                else:
                    assert False
            P[P[pnt+jmp-1]] = res
        elif op == 2: # multiplication
            jmp = 4
            res = 1
            Mode = get_mode(inst, jmp)
            assert Mode[-1] == 0
            for ix in range(jmp-2):
                mode = Mode[ix]
                if mode == 0:
                    res *= P[P[pnt+ix+1]]
                elif mode == 1:
                    res *= P[pnt+ix+1]
                else:
                    assert False
            P[P[pnt+jmp-1]] = res
        elif op == 3: # input
            jmp = 2
            Mode = get_mode(inst, jmp)
            assert Mode[-1] == 0
            P[P[pnt+1]] = ii
        elif op == 4: # output
            jmp = 2
            Mode = get_mode(inst, jmp)
            mode = Mode[-1]
            if mode == 0:
                out = P[P[pnt+1]]
            elif mode == 1:
                out = P[pnt+1]
            else:
                assert False
            Out.append(out)
        elif op == 5: # jump if true
            jmp = 3
            Mode = get_mode(inst, jmp)
            if Mode[0] == 0:
                chk = P[P[pnt+1]]
            elif Mode[0] == 1:
                chk = P[pnt+1]
            else:
                assert False
            if chk != 0:
                if Mode[1] == 0:
                    pnt = P[P[pnt+2]]
                elif Mode[1] == 1:
                    pnt = P[pnt+2]
                else:
                    assert False
                jmp = 0
            else:
                pass
        elif op == 6: # jump if false
            jmp = 3
            Mode = get_mode(inst, jmp)
            if Mode[0] == 0:
                chk = P[P[pnt+1]]
            elif Mode[0] == 1:
                chk = P[pnt+1]
            else:
                assert False
            if chk == 0:
                if Mode[1] == 0:
                    pnt = P[P[pnt+2]]
                elif Mode[1] == 1:
                    pnt = P[pnt+2]
                else:
                    assert False
                jmp = 0
            else:
                pass
        elif op == 7: # is less than
            jmp = 4
            Mode = get_mode(inst, jmp)
            assert Mode[-1] == 0
            Chk = []
            for ix in range(jmp-2):
                mode = Mode[ix]
                if mode == 0:
                    Chk.append( P[P[pnt+ix+1]] )
                elif mode == 1:
                    Chk.append( P[pnt+ix+1] )
                else:
                    assert False
            P[P[pnt+jmp-1]] = 1 * (Chk[0] < Chk[1])
        elif op == 8: # is equal to
            jmp = 4
            Mode = get_mode(inst, jmp)
            assert Mode[-1] == 0
            Chk = []
            for ix in range(jmp-2):
                mode = Mode[ix]
                if mode == 0:
                    Chk.append( P[P[pnt+ix+1]] )
                elif mode == 1:
                    Chk.append( P[pnt+ix+1] )
                else:
                    assert False
            P[P[pnt+jmp-1]] = 1 * (Chk[0] == Chk[1])
        elif op == 99: # halt
            jmp = 1
            break
        else:
            assert False
        pnt += jmp
    return P, Out

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))

# part 1
P = list(X)
P, Out = intcode(P, 1)
assert all(out == 0 for out in Out[:-1])
ans1 = Out[-1]
print(ans1)

# part 2
P = list(X)
P, Out = intcode(P, 5)
assert len(Out)==1
ans2 = Out[-1]
print(ans2)

