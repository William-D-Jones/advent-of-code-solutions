import sys

def mix(Val, Pos):
    for i,val in sorted(Val.items()):
        start_left, start_right = Pos[i]
        pointer = i
        val %= len(Val)-1
        if val == 0:
            continue
        Pos[start_left] = (Pos[start_left][0], start_right)
        Pos[start_right] = (start_left, Pos[start_right][1])
        for _ in range(abs(val)):
            if val<0:
                pointer = Pos[pointer][0]
            elif val>0:
                pointer = Pos[pointer][1]
        if val>0:
            pointer = Pos[pointer][1]
        end_left, end_right = Pos[pointer]
        Pos[end_left] = (Pos[end_left][0], i)
        Pos[end_right] = (pointer, Pos[end_right][1])
        Pos[i] = (end_left, pointer)
        Pos[pointer] = (i, end_right)
    return Val, Pos

def grove(Val, Pos, Jump, start):
    dist = tuple(JMP[i]- ( 0 if i==0 else JMP[i-1] ) for i in range(len(JMP)))
    tot = 0
    pointer = start
    for jmp in dist:
        if jmp == 0:
            continue
        for _ in range(abs(jmp)):
            if jmp<0:
                pointer = Pos[pointer][0]
            elif jmp>0:
                pointer = Pos[pointer][1]
        tot += Val[pointer]
    return tot

# parsing
X = [int(line.strip()) for line in open(sys.argv[1], 'r')]
JMP = (1000, 2000, 3000)

# part 1
Val = {i: val for i,val in enumerate(X)}
Pos = {i: ( (i-1) % len(X), (i+1) % len(X) ) for i in range(len(X))}
i0 = {i for i,val in Val.items() if val==0}
assert len(i0)==1
i0 = i0.pop()
Val, Pos = mix(Val, Pos)
# compute the grove coordinates
ans1 = grove(Val, Pos, (1000, 2000, 3000), i0)
print(ans1)

# part 2
dk = 811589153
rep = 10
Val = {i: val * dk for i,val in enumerate(X)}
Pos = {i: ( (i-1) % len(X), (i+1) % len(X) ) for i in range(len(X))}
i0 = {i for i,val in Val.items() if val==0}
assert len(i0)==1
i0 = i0.pop()
for _ in range(rep):
    Val, Pos = mix(Val, Pos)
# compute the grove coordinates
ans2 = grove(Val, Pos, (1000, 2000, 3000), i0)
print(ans2)

