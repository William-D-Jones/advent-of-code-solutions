import sys

def run(Inst, Reg = {'a': 0, 'b': 0}):
    i = 0
    while i < len(Inst):
        inst = Inst[i]
        if inst[0] == 'hlf':
            Reg[inst[1]] //= 2
            i += 1
        elif inst[0] == 'tpl':
            Reg[inst[1]] *= 3
            i += 1
        elif inst[0] == 'inc':
            Reg[inst[1]] += 1
            i += 1
        elif inst[0] == 'jmp':
            i += inst[1]
        elif inst[0] == 'jie':
            if Reg[inst[1]] % 2 == 0:
                i += inst[2]
            else:
                i += 1
        elif inst[0] == 'jio':
            if Reg[inst[1]] == 1:
                i += inst[2]
            else:
                i += 1
        else:
            assert False
    return Reg

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    inst = []
    xs = (' '.join(x.split(', '))).split(' ')
    for i in range(len(xs)):
        try:
            xs[i] = int(xs[i])
        except:
            pass
    Inst.append(xs)

# part 1
Reg = run(Inst)
ans1 = Reg['b']
print(ans1)

# part 1
Reg = run(Inst, {'a': 1, 'b': 0})
ans2 = Reg['b']
print(ans2)

