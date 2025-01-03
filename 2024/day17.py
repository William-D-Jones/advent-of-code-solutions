import sys
from copy import deepcopy

def get_combo(operand, register):
    if 0<=operand<=3:
        return operand
    elif operand==4:
        return register['A']
    elif operand==5:
        return register['B']
    elif operand==6:
        return register['C']
    else:
        assert False

def execute(pointer, opcode, operand, register):
    out = None
    if opcode == 0: # A = A // 2**combo
        combo = get_combo(operand, register)
        result = register['A'] // 2 ** combo
        register['A'] = result
        pointer += 2
    elif opcode == 1: # B = B ^ literal
        result = register['B'] ^ operand
        register['B'] = result
        pointer += 2
    elif opcode == 2: # B = combo % 8
        result = get_combo(operand, register) % 8
        register['B'] = result
        pointer += 2
    elif opcode == 3: # jump if A != 0
        if register['A'] == 0:
            pointer += 2
        else:
            pointer = operand
    elif opcode == 4: # B = B ^ C
        register['B'] = register['B'] ^ register['C']
        pointer += 2
    elif opcode == 5: # output combo % 8
        out = get_combo(operand, register) % 8
        pointer += 2
    elif opcode == 6: # B = A // 2**combo
        combo = get_combo(operand, register)
        result = register['A'] // 2 ** combo
        register['B'] = result
        pointer += 2
    elif opcode == 7: # C = A // 2**combo
        combo = get_combo(operand, register)
        result = register['A'] // 2 ** combo
        register['C'] = result
        pointer += 2
    else:
        assert False
    return pointer, register, out

def run(R, P):
    pointer = 0
    Out = []
    while pointer < len(P):
        pointer, R, out = \
        execute(pointer, P[pointer], P[pointer+1], R)
        if out is not None:
            Out.append(out)
    return Out

# parsing
X = open(sys.argv[1], 'r').read().strip()
X1,X2 = X.split('\n\n')
init = {}
for x in X1.split('\n'):
    xs = x.split()
    init[xs[1][:-1]] = int(xs[2])
P = list(map(int, (X2.split()[1]).split(',')))

# part 1
R = deepcopy(init)
Out = run(R, P)
print(','.join(list(map(str,Out))))

# part 2
A = 0
A_next = 0
for i in range(len(P)):
    for A_next in range(8):
        Out_Needed = P[len(P) - (i+1):]
        R = deepcopy(init)
        R['A'] = (A << 3) + A_next
        Out = run(R, P)
        if Out == Out_Needed:
            break
    A = (A << 3) + A_next
print(A)

