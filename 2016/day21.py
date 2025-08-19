import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Inst = []
for x in X:
    xs = x.split()
    com = xs[0]
    if com == 'swap':
        if xs[1] == 'position':
            Inst.append( (com, xs[1], int(xs[2]), int(xs[5])) )
        elif xs[1] == 'letter':
            Inst.append( (com, xs[1], xs[2], xs[5]) )
    elif com == 'rotate':
        if xs[1] in ('left', 'right'):
            Inst.append( (com, xs[1], int(xs[2])) )
        elif xs[3] == 'position':
            Inst.append( (com, xs[3], xs[6]) )
        else:
            assert False
    elif com == 'reverse':
        Inst.append( (com, int(xs[2]), int(xs[4]) ) )
    elif com == 'move':
        Inst.append( (com, int(xs[2]), int(xs[5]) ) )
    else:
        assert False

# part 1
password = list('abcdefgh')
for inst in Inst:
    com = inst[0]
    if com == 'swap':
        if inst[1] == 'position':
            password[inst[2]], password[inst[3]] = \
            password[inst[3]], password[inst[2]]
        elif inst[1] == 'letter':
            for i in range(len(password)):
                if password[i] == inst[2]:
                    password[i] = inst[3]
                elif password[i] == inst[3]:
                    password[i] = inst[2]
    elif com == 'rotate':
        if inst[1] == 'left':
            rot = -1 * inst[2]
        elif inst[1] == 'right':
            rot = inst[2]
        elif inst[1] == 'position':
            ix = password.index(inst[2])
            rot = 1 + ix + (1 if ix >= 4 else 0)
        else:
            assert False
        rot = rot % len(password)
        if rot > 0:
            password = password[-rot:] + password[:len(password)-rot]
    elif com == 'reverse':
        password = password[:inst[1]] + password[inst[1]:inst[2]+1][::-1] + \
        password[inst[2]+1:]
    elif com == 'move':
        mv = password.pop(inst[1])
        password = password[:inst[2]] + [mv] + password[inst[2]:]
    else:
        assert False
ans1 = ''.join(password)
print(ans1)

# part 2
password = list('fbgdceah')
# For inverting the positional rotation operation, I computed what the old
# index of a character was based on its new index, since there are only 8
# positions.
assert len(password) == 8
D_Pos_Inv = {1:0, 3:1, 5:2, 7:3, 2:4, 4:5, 6:6, 0:7}
for inst in reversed(Inst):
    com = inst[0]
    if com == 'swap':
        if inst[1] == 'position':
            password[inst[2]], password[inst[3]] = \
            password[inst[3]], password[inst[2]]
        elif inst[1] == 'letter':
            for i in range(len(password)):
                if password[i] == inst[2]:
                    password[i] = inst[3]
                elif password[i] == inst[3]:
                    password[i] = inst[2]
    elif com == 'rotate':
        if inst[1] == 'left':
            rot = inst[2]
        elif inst[1] == 'right':
            rot = -1 * inst[2]
        elif inst[1] == 'position':
            ix = password.index(inst[2])
            rot = D_Pos_Inv[ix] - ix
        else:
            assert False
        rot = rot % len(password)
        if rot > 0:
            password = password[-rot:] + password[:len(password)-rot]
    elif com == 'reverse':
        password = password[:inst[1]] + password[inst[1]:inst[2]+1][::-1] + \
        password[inst[2]+1:]
    elif com == 'move':
        mv = password.pop(inst[2])
        password = password[:inst[1]] + [mv] + password[inst[1]:]
    else:
        assert False
ans2 = ''.join(password)
print(ans2)

