import sys

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]
Inst = [(x[0], int(x[1:])) for x in X]

# part 1
ans1 = 0
pnt = 50
dial = 100
tar = 0
for dx, n in Inst:
    if dx == 'L':
        pnt = (pnt-n) % dial
    elif dx == 'R':
        pnt = (pnt+n) % dial
    else:
        assert False
    if pnt == tar:
        ans1 += 1
print(ans1)

# part 2
ans2 = 0
pnt = 50
dial = 100
tar = 0
for dx, n in Inst:
    if dx == 'L':
        n2tar = pnt-tar if pnt > tar else dial-tar+pnt
        if n >= n2tar:
            ans2 += 1 + (n-n2tar) // dial
        pnt = (pnt-n) % dial
    elif dx == 'R':
        n2tar = tar-pnt if pnt < tar else dial-pnt+tar
        if n >= n2tar:
            ans2 += 1 + (n-n2tar) // dial
        pnt = (pnt+n) % dial
    else:
        assert False
print(ans2)

