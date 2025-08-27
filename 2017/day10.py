import sys

def knot(Num, X, point, skip):
    for x in X:
        assert x <= len(Num)
        s = point
        e = (point+x) % len(Num)
        if e>s:
            Num = Num[:s] + Num[s:e][::-1] + Num[e:]
        elif e<=s and x>0:
            S = Num[s:]
            E = Num[:e-len(Num)]
            Mid = Num[e-len(Num):s]
            SE = S + E
            SEr = SE[::-1]
            Sr = SEr[:len(Num)-s]
            Er = SEr[len(Num)-s:]
            Num = Er + Mid + Sr
        elif e==s and x==0:
            pass
        else:
            assert False
        point = (point + x + skip) % len(Num)
        skip += 1
    return Num, point, skip

# parsing
X = list(map(int, \
''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split(',')))

# part 1
Num = list(range(0,256))
point = 0
skip = 0
Num, point, skip = knot(Num, X, point, skip)
ans1 = Num[0] * Num[1]
print(ans1)

# part 2
# convert the numeric input to bytes
B = list(map(ord, list(','.join(list(map(str, X))))))
B += [17,31,73,47,23]
# run 64 rounds of knot
Num = list(range(0,256))
point = 0
skip = 0
for _ in range(64):
    Num, point, skip = knot(Num, B, point, skip)
# get the dense hash
D = []
for i in range(0, len(Num) // 16):
    block = Num[16*i:16*i+16]
    d = 0
    for num in block:
        d ^= num
    D.append(d)
# get the hex hash
ans2 = ''
for d in D:
    ans2 += hex(d)[2:]
print(ans2)

