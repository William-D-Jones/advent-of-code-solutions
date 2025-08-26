import sys
import re
from collections import defaultdict

def run(Inst):
    Reg = defaultdict(int)
    max_val = 0
    for inst in Inst:
        tar = None
        if inst[4] == '>':
            if Reg[inst[3]] > inst[5]:
                tar = inst[0]
        elif inst[4] == '<':
            if Reg[inst[3]] < inst[5]:
                tar = inst[0]
        elif inst[4] == '>=':
            if Reg[inst[3]] >= inst[5]:
                tar = inst[0]
        elif inst[4] == '<=':
            if Reg[inst[3]] <= inst[5]:
                tar = inst[0]
        elif inst[4] == '==':
            if Reg[inst[3]] == inst[5]:
                tar = inst[0]
        elif inst[4] == '!=':
            if Reg[inst[3]] != inst[5]:
                tar = inst[0]
        else:
            assert False
        if tar is not None:
            if inst[1] == 'inc':
                Reg[tar] += inst[2]
            elif inst[1] == 'dec':
                Reg[tar] -= inst[2]
            else:
                assert False
            if Reg[tar] > max_val:
                max_val = Reg[tar]
    return Reg, max_val

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    M = re.match('^([a-zA-Z]+) (inc|dec) ([0-9\\-]+) if '+\
    '([a-zA-Z]+) (>|<|>=|<=|==|!=) ([0-9\\-]+)$', x)
    Inst.append( (M.group(1), M.group(2), int(M.group(3)), M.group(4), \
    M.group(5), int(M.group(6))) )

# parts 1 and 2
Reg, ans2 = run(Inst)
ans1 = max(Reg.values())
print(ans1)
print(ans2)

