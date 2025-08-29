import sys

a = ord('a')
p = ord('p')

def dance(Prog, Inst):
    for inst in Inst:
        if inst[0] == 's':
            Prog = Prog[len(Prog)-inst[1]:] + Prog[:len(Prog)-inst[1]]
        elif inst[0] == 'x':
            Prog[inst[1]], Prog[inst[2]] = Prog[inst[2]], Prog[inst[1]]
        elif inst[0] == 'p':
            i = Prog.index(inst[1])
            j = Prog.index(inst[2])
            Prog[i], Prog[j] = Prog[j], Prog[i]
        else:
            assert False
    return Prog

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split(',')
Inst = []
for x in X:
    t = x[0:1]
    xs = x[1:].split('/')
    assert len(xs) <= 2
    if t == 's':
        Inst.append( (t, int(xs[0])) )
    elif t == 'x':
        Inst.append( (t, int(xs[0]), int(xs[1])) )
    elif t == 'p':
        Inst.append( (t, xs[0], xs[1]) )
    else:
        print(x)
        assert False

# part 1
# setup the programs
Prog = []
for i in range(a,p+1):
    Prog.append( chr(i) )
# run the instructions
Prog = dance(Prog, Inst)
ans1 = ''.join(Prog)
print(ans1)

# part 2
# setup the programs
Prog = []
for i in range(a,p+1):
    Prog.append( chr(i) )
# run the instructions
Hist = []
n = 1000000000
for i in range(n):
    Prog = dance(Prog, Inst)
    out = ''.join(Prog)
    if out in Hist:
        rep = Hist.index(out)
        ans2 = Hist[rep + (n-1) % (len(Hist)-rep)]
        break
    else:
        Hist.append(out)
print(ans2)

