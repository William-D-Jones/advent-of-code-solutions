import sys

def run(Inst, Reg, i, stop = None):
    mul = 0
    if stop is None:
        stop = len(Inst)
    while i < len(Inst):
        if i >= stop:
            break
        inst = Inst[i]
        if inst[0] == 'set':
            if inst[2] in Reg.keys():
                Reg[inst[1]] = Reg[inst[2]]
            else:
                Reg[inst[1]] = inst[2]
            i += 1
        elif inst[0] == 'sub':
            if inst[2] in Reg.keys():
                Reg[inst[1]] -= Reg[inst[2]]
            else:
                Reg[inst[1]] -= inst[2]
            i += 1
        elif inst[0] == 'mul':
            if inst[2] in Reg.keys():
                Reg[inst[1]] *= Reg[inst[2]]
            else:
                Reg[inst[1]] *= inst[2]
            i += 1
            mul += 1
        elif inst[0] == 'jnz':
            if (inst[1] in Reg.keys() and Reg[inst[1]] != 0) or \
            (inst[1] not in Reg.keys() and inst[1] != 0):
                if inst[2] in Reg.keys():
                    i += Reg[inst[2]]
                else:
                    i += inst[2]
            else:
                i += 1
        else:
            assert False
    return Reg, i, mul

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
Reg = {chr(x):0 for x in range(ord('a'), ord('h')+1)}
Reg, i, mul = run(Inst, Reg, 0)
ans1 = mul
print(ans1)

# part 2

# I made the following observations about the input:
# (i) There is only one h instruction, a sub operation by a constant
inst_h = [inst for inst in Inst if inst[1] == 'h' or inst[2] == 'h']
assert len(inst_h) == 1
inst_h = inst_h.pop()
ix_h = Inst.index(inst_h)
assert inst_h[0] == 'sub'
h_sub = inst_h[2]
assert type(h_sub) is int
# (ii) The program cannot terminate by simply reaching the end of the program,
# since the program ends in a negative jnz instruction. Instead, the program
# must execute a positive jnz instruction before the end in order to skip the
# last instruction. This terminating jnz instruction is controlled by a nonzero
# integer, so as long as this terminating jnz intruction is reached, it will by
# executed.
assert Inst[-1][0] == 'jnz' and Inst[-1][1] > 0 and Inst[-1][2] < 0
inst_term = []
ix_term = []
for i,inst in enumerate(Inst):
    if inst[0] == 'jnz' and i+inst[2] >= len(Inst):
        inst_term.append(inst)
        ix_term.append(i)
assert len(inst_term) == 1
inst_term = inst_term.pop()
ix_term = ix_term.pop()
assert type(inst_term[1]) is int
# (ii-a) There exists exactly one jnz instruction that can prevent inst_term
# from executing. This instruction is controlled by a register value, so that
# register value must equal zero for the program to terminate.
inst_block = []
ix_block = []
for i,inst in enumerate(Inst):
    if inst[0] == 'jnz' and i < ix_term and i+inst[2] > ix_term:
        inst_block.append(inst)
        ix_block.append(i)
assert len(inst_block) == 1
inst_block = inst_block.pop()
ix_block = ix_block.pop()
assert type(inst_block[1]) is str
reg_block = inst_block[1]
# (ii-b) Just before the inst_block is considered, reg_block is set and then
# subtracted from using 2 registers, testing whether the values in those 
# registers are equal.
inst_eq_1 = Inst[ix_block-2]
inst_eq_2 = Inst[ix_block-1]
assert inst_eq_1[0] == 'set' and inst_eq_2[0] == 'sub' and \
inst_eq_1[1] == reg_block and inst_eq_2[1] == reg_block
reg_eq = (inst_eq_1[2], inst_eq_2[2])
# (ii-c) If those 2 registers are not equal at the beginning of the program,
# they can become equal by the end of the program due to a sub instruction that
# alters one of those registers. This sub instruction occurs after inst_term,
# which means every time that the program does not terminate, the register is
# updated, potentially bringing the two registers closer to being equal. The 
# value subtracted in the sub operation is an integer.
inst_eq_sub = []
ix_eq_sub = []
for i,inst in enumerate(Inst):
    if i <= ix_term:
        continue
    if inst[0] == 'sub' and inst[1] in reg_eq and type(inst[2]) is int:
        inst_eq_sub.append(inst)
        ix_eq_sub.append(i)
assert len(inst_eq_sub) == 1
inst_eq_sub = inst_eq_sub.pop()
ix_eq_sub = ix_eq_sub.pop()
reg_eq_sub = inst_eq_sub[1]
reg_eq_const = [reg for reg in reg_eq if reg != reg_eq_sub]
assert len(reg_eq_const) == 1
reg_eq_const = reg_eq_const.pop()
# (iii) The program begins with some instructions that are never executed again
# regardless of any subsequent jnz operations. The two registers reg_eq are
# setup during the preamble, and only one of them is ever operated on again
# after the preamble, which is reg_eq_sub, and it is only operated on by
# inst_eq_sub.
ix_pre_max = len(Inst)
for i,inst in enumerate(Inst):
    if inst[0] == 'jnz' and inst[2] < 0 and i+inst[2] < ix_pre_max:
        ix_pre_max = i+inst[2]
for i,inst in enumerate(Inst):
    if inst[1] == reg_eq_sub:
        assert i<ix_pre_max or i == ix_eq_sub
    elif inst[1] == reg_eq_const:
        assert i<ix_pre_max
# (iii-a) Given all the above information, we can determine how many times
# inst_eq_sub will need to execute before the program can terminate.
# First, run only the preamble of the program:
Reg = {chr(x):0 for x in range(ord('a'), ord('h')+1)}
Reg['a'] = 1
Reg, i, mul = run(Inst, Reg, 0, ix_pre_max)
# Second, determine how many times reg_eq_sub needs to be substracted from to
# produce the same value as in reg_eq_const:
n_sub = abs(Reg[reg_eq_const] - Reg[reg_eq_sub]) // abs(inst_eq_sub[2])
assert Reg[reg_eq_sub] - inst_eq_sub[2] * n_sub == Reg[reg_eq_const]
# (iii-b) Therefore, after reaching the inst_eq_sub instruction n_sub times,
# the program will terminate on the next run-through (i.e. the n_sub+1th time).
# (iv) The h instruction is not executed every time the program is run, because
# one of the jnz instructions skips the h instruction. This jnz instruction
# refers to a register that the program only ever sets explictly to 0 or 1.
# The instruction that sets the register to 1 is only reached when the last
# instruction in the program jumps back to just after the preamble, starting
# over the main loop of the program.
inst_h_block = []
ix_h_block = []
for i,inst in enumerate(Inst):
    if inst[0] == 'jnz' and i < ix_h and i+inst[2] > ix_h:
        inst_h_block.append(inst)
        ix_h_block.append(i)
assert len(inst_h_block) == 1
inst_h_block = inst_h_block.pop()
ix_h_block = ix_h_block.pop()
reg_h_block = inst_h_block[1]
for i,inst in enumerate(Inst):
    if i != ix_h_block and inst[1] == reg_h_block:
        assert inst[0] == 'set' and 0<=inst[2]<=1
        if inst[2] == 1:
            ix_reset = i
assert ix_reset == len(Inst)-1+Inst[-1][2]
# (v) The register is set to 0 by a mul instruction that checks if two registers
# multiplied equal reg_eq_sub. The program is therefore counting the number of
# composite numbers between the starting values of reg_eq_sub and reg_eq_const,
# if abs(inst_eq_sub[2]) is added each time.

# find the number of composite numbers
ans2 = 0
val = Reg[reg_eq_sub]
while val <= Reg[reg_eq_const]:
    div = 2
    while div <= val // div:
        if val % div == 0:
            break
        div += 1
    if val % div == 0:
        ans2 += 1
    val += abs(inst_eq_sub[2])
print(ans2)

