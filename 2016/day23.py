import sys
from copy import deepcopy

def run(Inst, Reg):
    point = 0
    Hist = []
    Mul = []
    while point < len(Inst):
        inst = Inst[point]
        if inst[0] == 'cpy':
            if inst[2] in Reg.keys():
                if inst[1] in Reg.keys():
                    Reg[ inst[2] ] = Reg[ inst[1] ]
                else:
                    Reg[ inst[2] ] = inst[1]
                Hist.append( (point, inst, inst[2]) )
            else:
                Hist.append( (point, inst, None) )
            point += 1
        elif inst[0] == 'inc':
            if inst[1] in Reg.keys():
                Reg[ inst[1] ] += 1
                Hist.append( (point, inst, inst[1]) )
            else:
                Hist.append( (point, inst, None) )
            point += 1
        elif inst[0] == 'dec':
            if inst[1] in Reg.keys():
                Reg[ inst[1] ] -= 1
                Hist.append( (point, inst, inst[1]) )
            else:
                Hist.append( (point, inst, None) )
            point += 1
        elif inst[0] == 'jnz':
            if (inst[1] in Reg.keys() and Reg[ inst[1] ] != 0) or \
            (inst[1] not in Reg.keys() and inst[1] != 0):
                if inst[2] in Reg.keys():
                    jump = Reg[ inst[2] ]
                else:
                    jump = inst[2]
                Hist.append( (point, inst, jump) )
                # jump the pointer
                point += jump
                # check if history has repeated itself
                # we deal only with multiplication-like repeats
                if jump < 0:
                    # identify the repetitious sequence
                    rep_start = point
                    rep_end = point-jump+1
                    seq = Hist[-(-jump+1):]
                    if Inst[rep_start:rep_end] != [s[1] for s in seq] or \
                    any(s[1][0] not in ('inc', 'dec', 'jnz', 'cpy') and \
                    s[2] is not None for s in seq):
                        continue
                    # get the register which is serving as the counter
                    cnt = inst[1]
                    if ('dec', cnt) not in [s[1] for s in seq]:
                        continue
                    # get the number of times the counter will repeat
                    nrep = Reg[ cnt ]
                    assert nrep >= 0
                    # construct the operation
                    # [start, end, target, counters, sign, sequence]
                    Op = [rep_start, rep_end, None, [cnt], None, seq]
                    # check if the repeat contains another repeat
                    for i, Rep in enumerate(Mul):
                        if rep_start <= Rep[0] and rep_end >= Rep[1] and \
                        rep_end - rep_start > Rep[1] - Rep[0]:
                            Sub_Op = Mul.pop(i)
                            Op[2] = Sub_Op[2]
                            Op[3] += Sub_Op[3]
                            Op[4] = Sub_Op[4]
                            break
                    # if this is a new repeat, finish constructing the operation
                    if Op[2] is None:
                        inst_op = [s[1] for s in seq if s[1][1] != cnt]
                        assert len(inst_op) == 1
                        inst_op = inst_op[0]
                        if inst_op[0] == 'inc':
                            Op[4] = 1
                        elif inst_op[0] == 'dec':
                            Op[4] = -1
                        else:
                            assert False
                        Op[2] = inst_op[1]
                    # sometimes a counter will be reset by a cpy operation
                    for i, cnt in enumerate(Op[3]):
                        inst_cpy = [s for s in seq if \
                        s[1][0] == 'cpy' and s[1][2] == cnt]
                        assert len(inst_cpy) <= 1
                        if len(inst_cpy) == 1:
                            inst_cpy = inst_cpy[0]
                            cnt = inst_cpy[1][1]
                            Op[3][i] = cnt
                    # execute the repeat
                    mul = Op[4]
                    for src in Op[3]:
                        if src in Reg.keys():
                            mul *= Reg[src]
                        else:
                            mul *= src
                        if not any(s[1][0] == 'cpy' and s[1][1] == src and \
                        s[2] is not None for s in seq):
                            Reg[src] = 0
                    Reg[ Op[2] ] += mul
                    point = rep_end
                    # record the repeat
                    Mul.append(Op)
            else:
                Hist.append( (point, inst, None) )
                point += 1
        elif inst[0] == 'tgl':
            ix = point + \
            (inst[1] if inst[1] not in Reg.keys() else Reg[inst[1]])
            if 0<=ix<len(Inst):
                tgl = list(Inst[ix])
                if tgl[0] == 'inc':
                    tgl[0] = 'dec'
                elif len(tgl) == 2:
                    tgl[0] = 'inc'
                elif tgl[0] == 'jnz':
                    tgl[0] = 'cpy'
                elif len(tgl) == 3:
                    tgl[0] = 'jnz'
                else:
                    assert False
                Inst[ix] = tuple(tgl)
                Hist.append( (point, inst, ix) )
            else:
                Hist.append( (point, inst, None) )
            point += 1
        else:
            assert False
    return Reg

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    xp = []
    for el in x.split():
        try:
            xp.append(int(el))
        except:
            xp.append(el)
    Inst.append( tuple(xp) )

# part 1
Reg1 = run(deepcopy(Inst), {'a': 7, 'b': 0, 'c': 0, 'd': 0})
ans1 = Reg1['a']
print(ans1)

# part 2
Reg2 = run(deepcopy(Inst), {'a': 12, 'b': 0, 'c': 0, 'd': 0})
ans2 = Reg2['a']
print(ans2)

