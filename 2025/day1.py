import sys

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]
Inst = [(x[0], int(x[1:])) for x in X]

# part 1
ans1 = 0
pnt = 50
dial = 100
for dx, n in Inst:
    if dx == 'L':
        pnt = (pnt-n) % dial
    elif dx == 'R':
        pnt = (pnt+n) % dial
    else:
        assert False
    if pnt == 0:
        ans1 += 1
print(ans1)

# part 2
ans2 = 0
pnt = 50
dial = 100
for dx, n in Inst:
    if dx == 'L':
        for _ in range(n):
            pnt = (pnt-1) % dial
            if pnt == 0:
                ans2 += 1
    elif dx == 'R':
        for _ in range(n):
            pnt = (pnt+1) % dial
            if pnt == 0:
                ans2 += 1
    else:
        assert False
print(ans2)

