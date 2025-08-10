import sys
from collections import deque
from copy import deepcopy

OPS = set(['AND','OR','LSHIFT','RSHIFT','NOT'])

def run_wires(Wires, Inst, skip = set()):
    while Inst:
        inst, out = Inst.popleft()
        if out in skip:
            continue
        inst_parse = list(inst)
        for i in range(len(inst_parse)):
            try:
                inst_parse[i] = int(inst_parse[i])
            except:
                if inst_parse[i] in OPS:
                    next
                elif inst_parse[i] in Wires.keys():
                    inst_parse[i] = Wires[inst_parse[i]]
                else:
                    inst_parse[i] = None
        if any(item is None for item in inst_parse):
            Inst.append((inst, out))
            continue
        if len(inst_parse) == 1:
            Wires[out] = inst_parse[0]
        elif inst_parse[1] == 'AND':
            Wires[out] = inst_parse[0] & inst_parse[2]
        elif inst[1] == 'OR':
            Wires[out] = inst_parse[0] | inst_parse[2]
        elif inst[1] == 'LSHIFT':
            Wires[out] = (inst_parse[0] << inst_parse[2]) % 2**16
        elif inst[1] == 'RSHIFT':
            Wires[out] = inst_parse[0] >> inst_parse[2]
        elif inst[0] == 'NOT':
            Wires[out] = (~ inst_parse[1]) + 2 ** 16
        else:
            assert False
    return Wires

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = deque()
for x in X:
    IN, OUT = x.split(' -> ')
    INS = IN.split(' ')
    Inst.append( (tuple(INS), OUT) )
        
# part 1
Wires = {}
Wires = run_wires(Wires, deepcopy(Inst))
ans1 = Wires['a']
print(ans1)

# part 2
Wires = {'b': ans1}
Wires = run_wires(Wires, deepcopy(Inst), skip = set(['b']))
ans2 = Wires['a']
print(ans2)

