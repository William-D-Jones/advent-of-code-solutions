import sys
from collections import defaultdict, deque

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = deque([])
for x in X:
    xs = x.split()
    if xs[0] == 'value':
        val = int(xs[1])
        dest = int(xs[5])
        Inst.append( (val, dest) )
    elif xs[0] == 'bot':
        assert xs[3] == 'low' and xs[8] == 'high'
        source = int(xs[1])
        dest_low = int(xs[6])
        dest_high = int(xs[11])
        Inst.append( (source, xs[5], dest_low, xs[10], dest_high) )
    else:
        assert False

# part 1
Bot = defaultdict(set)
Out = defaultdict(set)
while Inst:
    inst = Inst.popleft()
    if len(inst) == 2:
        Bot[inst[1]].add(inst[0])
    elif len(inst) == 5:
        source, name_low, dest_low, name_high, dest_high = inst
        if len(Bot[source]) < 2:
            Inst.append(inst)
            continue
        chip_low = min(Bot[source])
        chip_high = max(Bot[source])
        Bot[source].remove(chip_low)
        Bot[source].remove(chip_high)
        if chip_low == 17 and chip_high == 61:
            ans1 = source
        if name_low == 'bot':
            Bot[dest_low].add(chip_low)
        elif name_low == 'output':
            Out[dest_low].add(chip_low)
        else:
            assert False
        if name_high == 'bot':
            Bot[dest_high].add(chip_high)
        elif name_high == 'output':
            Out[dest_high].add(chip_high)
        else:
            assert False
    else:
        assert False
print(ans1)

# part 2
ans2 = Out[0].pop() * Out[1].pop() * Out[2].pop()
print(ans2)

