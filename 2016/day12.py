import sys

def run(Inst, Reg):
    point = 0
    while point < len(Inst):
        inst = Inst[point]
        if inst[0] == 'cpy':
            if inst[1] in Reg.keys():
                Reg[ inst[2] ] = Reg[ inst[1] ]
            else:
                Reg[ inst[2] ] = inst[1]
            point += 1
        elif inst[0] == 'inc':
            Reg[ inst[1] ] += 1
            point += 1
        elif inst[0] == 'dec':
            Reg[ inst[1] ] -= 1
            point += 1
        elif inst[0] == 'jnz':
            if (inst[1] in Reg.keys() and Reg[ inst[1] ] != 0) or \
            (inst[1] not in Reg.keys() and inst[1] != 0):
                point += inst[2]
            else:
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
Reg1 = run(Inst, {'a': 0, 'b': 0, 'c': 0, 'd': 0})
ans1 = Reg1['a']
print(ans1)

# part 2
Reg2 = run(Inst, {'a': 0, 'b': 0, 'c': 1, 'd': 0})
ans2 = Reg2['a']
print(ans2)

