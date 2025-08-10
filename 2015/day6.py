import sys
from collections import defaultdict

# parsing
Inst = []
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
for x in X:
    xs = x.split(' ')
    if xs[0] == 'turn':
        tar = xs[1]
    else:
        tar = xs[0]
    sx, sy = map(int, xs[-3].split(','))
    ex, ey = map(int, xs[-1].split(','))
    Inst.append( (tar, (sx, sy), (ex, ey)) )

# part 1
Light = defaultdict(int)
for inst in Inst:
    sx, sy = inst[1]
    ex, ey = inst[2]
    for x in range(sx, ex+1):
        for y in range(sy, ey+1):
            if inst[0] == 'on':
                Light[ (x,y) ] = 1
            elif inst[0] == 'off':
                Light[ (x,y) ] = 0
            elif inst[0] == 'toggle':
                Light[ (x,y) ] = (Light[ (x,y) ] + 1) % 2
            else:
                assert False
ans1 = 0
for (x,y), status in Light.items():
    if status == 1:
        ans1 += 1
print(ans1)

# part 2
Light = defaultdict(int)
for inst in Inst:
    sx, sy = inst[1]
    ex, ey = inst[2]
    for x in range(sx, ex+1):
        for y in range(sy, ey+1):
            if inst[0] == 'on':
                Light[ (x,y) ] += 1
            elif inst[0] == 'off':
                Light[ (x,y) ] = max(0, Light[ (x,y) ] - 1)
            elif inst[0] == 'toggle':
                Light[ (x,y) ] += 2
            else:
                assert False
ans2 = 0
for (x,y), status in Light.items():
    ans2 += status
print(ans2)
    
