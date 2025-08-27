import sys

# parsing
X = [ l.strip().split('->') for l in open(sys.argv[1], 'r') ]
Path = []
for x in X:
    Path.append([])
    for xi in x:
        coord = tuple(map(int, xi.split(',')))
        Path[-1].append( (coord[1], coord[0]) )
# fill in the rock coordinates
Rock = set()
for path in Path:
    for i in range(1,len(path)):
        c1, c2 = path[i-1:i+1]
        rs = min(c1[0], c2[0])
        re = max(c1[0], c2[0]) + 1
        cs = min(c1[1], c2[1])
        ce = max(c1[1], c2[1]) + 1
        for r in range(rs, re):
            for c in range(cs, ce):
                Rock.add( (r,c) )
rmax = max(r for (r,c) in Rock)

# part 1
abyss = False
Sand = set()
while not abyss:
    r_sand = 0
    c_sand = 500
    RS = Rock|Sand
    while not abyss:
        if (r_sand+1, c_sand) in RS:
            if (r_sand+1, c_sand-1) not in RS:
                c_sand -= 1
            elif (r_sand+1, c_sand+1) not in RS:
                c_sand += 1
            else:
                Sand.add( (r_sand, c_sand) )
                break
        if r_sand+1>rmax:
            abyss = True
        r_sand += 1
ans1 = len(Sand)
print(ans1)

# part 2
abyss = False
Sand = set()
rmax += 2
while (r_sand, c_sand) != (0, 500):
    r_sand = 0
    c_sand = 500
    RS = Rock|Sand
    while r_sand+1 != rmax:
        if (r_sand+1, c_sand) in RS:
            if (r_sand+1, c_sand-1) not in RS:
                c_sand -= 1
            elif (r_sand+1, c_sand+1) not in RS:
                c_sand += 1
            else:
                Sand.add( (r_sand, c_sand) )
                break
        r_sand += 1
    if r_sand + 1 == rmax:
        Sand.add( (r_sand, c_sand) )
ans2 = len(Sand)
print(ans2)

