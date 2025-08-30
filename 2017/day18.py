import sys
from collections import Counter

def run(Inst, Reg = Counter(), i = 0, Rcv = [], p2 = False):
    Snd = []
    while i < len(Inst):
        inst = Inst[i]
        if inst[0] == 'snd':
            if inst[1] in Reg.keys():
                Snd.append(Reg[inst[1]])
            else:
                Snd.append(inst[1])
            i += 1
        elif inst[0] == 'set':
            if inst[2] in Reg.keys():
                Reg[inst[1]] = Reg[inst[2]]
            else:
                Reg[inst[1]] = inst[2]
            i += 1
        elif inst[0] == 'add':
            if inst[2] in Reg.keys():
                Reg[inst[1]] += Reg[inst[2]]
            else:
                Reg[inst[1]] += inst[2]
            i += 1
        elif inst[0] == 'mul':
            if inst[2] in Reg.keys():
                Reg[inst[1]] *= Reg[inst[2]]
            else:
                Reg[inst[1]] *= inst[2]
            i += 1
        elif inst[0] == 'mod':
            if inst[2] in Reg.keys():
                Reg[inst[1]] %= Reg[inst[2]]
            else:
                Reg[inst[1]] %= inst[2]
            i += 1
        elif inst[0] == 'rcv':
            if not p2:
                return Reg, i, Rcv + Snd, 1
            else:
                if Rcv:
                    rcv = Rcv.pop(0)
                    Reg[inst[1]] = rcv
                else:
                    return Reg, i, Snd, 1
            i += 1
        elif inst[0] == 'jgz':
            if (inst[1] in Reg.keys() and Reg[inst[1]] > 0) or \
            (inst[1] not in Reg.keys() and inst[1] > 0):
                if inst[2] in Reg.keys():
                    i += Reg[inst[2]]
                else:
                    i += inst[2]
            else:
                i += 1
        else:
            assert False
    return Reg, i, Snd, 0

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    inst = []
    for xs in x.split():
        try:
            inst.append(int(xs))
        except:
            inst.append(xs)
    Inst.append(tuple(inst))

# part 1
Reg = Counter()
i = -1
Rcv = []
while i == -1 or Reg[ Inst[i][1] ] == 0:
    Reg, i, Rcv, status = run(Inst, Reg, i+1, Rcv)
ans1 = Rcv[-1]
print(ans1)

# part 2
Prog = {0: (Counter(p=0), 0, 1), 1: (Counter(p=1), 0, 1)}
Rcv = []
p = 0
ans2 = 0
while any(status == 1 for Reg, i, status in Prog.values()):
    Reg, i, status = Prog[p]
    if status == 0:
        continue
    Reg, i, Rcv, status = run(Inst, Reg, i, Rcv, True)
    if p == 1:
        ans2 += len(Rcv)
    Prog[p] = (Reg, i, status)
    p = (p+1) % len(Prog)
    if len(Rcv) == 0:
        break
print(ans2)    

