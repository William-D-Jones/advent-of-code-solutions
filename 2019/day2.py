import sys

def intcode(P):
    pnt = 0
    while True:
        op = P[pnt]
        if op == 1:
            P[P[pnt+3]] = P[P[pnt+1]] + P[P[pnt+2]]
            jmp = 4
        elif op == 2:
            P[P[pnt+3]] = P[P[pnt+1]] * P[P[pnt+2]]
            jmp = 4
        elif op == 99:
            jmp = 1
            break
        else:
            assert False
        pnt += jmp
    return P

# parsing
X = tuple(map(int, open(sys.argv[1], 'r').read().strip().split(',')))

# part 1
P = list(X)
P[1] = 12
P[2] = 2
P = intcode(P)
ans1 = P[0]
print(ans1)

# part 2
Noun = []
Verb = []
for noun in range(len(X)):
    for verb in range(len(X)):
        P = list(X)
        P[1] = noun
        P[2] = verb
        out = intcode(P)[0]
        if out == 19690720:
            Noun.append(noun)
            Verb.append(verb)
assert len(Noun) == 1
assert len(Verb) == 1
noun = Noun.pop()
verb = Verb.pop()
ans2 = 100 * noun + verb
print(ans2)

