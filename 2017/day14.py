import sys
from collections import deque

D = [ (-1,0), (0,1), (1,0), (0,-1) ]

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

def knot_hash(txt):
    # convert the input to ascii codes
    B = list(map(ord, list(txt)))
    B += [17,31,73,47,23]
    # run 64 rounds of knot to get the sparse hash
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
    H = ''
    for d in D:
        H += f'{d:02x}'
    return(H)

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
ans1 = 0
B = []
for i in range(128):
    H = knot_hash(X + '-' + str(i))
    b = ''
    for h in H:
        b += f'{int(h, 16):04b}'
    ans1 += b.count('1')
    B.append(list(b))
print(ans1)

# part 2
nrow = len(B)
ncol = len(B[0])
Q = set([(r,c) for c in range(ncol) for r in range(nrow) if B[r][c] == '1'])
Reg = []
while Q:
    start = Q.pop()
    Q_Reg = deque([start])
    S_Reg = set([start])
    while Q_Reg:
        r,c = Q_Reg.popleft()
        for dr,dc in D:
            nr,nc = r+dr,c+dc
            if (nr,nc) in Q and (nr,nc) not in S_Reg:
                Q.remove( (nr,nc) )
                S_Reg.add( (nr,nc) )
                Q_Reg.append( (nr,nc) )
    Reg.append(S_Reg)
ans2 = len(Reg)
print(ans2)

