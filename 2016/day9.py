import sys
import re

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
ix = 0
ans1 = 0
while ix < len(X):
    Match = re.match('^\\(([0-9]+)x([0-9]+)\\)', X[ix:])
    if Match:
        m1 = int(Match.group(1))
        m2 = int(Match.group(2))
        ans1 += (m1 * m2)
        ix += (len(Match.group(0)) + m1)
    else:
        ans1 += 1
        ix += 1
print(ans1)

# part 2
ix = 0
ans2 = 0
Grp_Mul = [1]
Grp_Cnt = [0]
Grp_End = [len(X)]
while ix < len(X):
    Match = re.match('^\\(([0-9]+)x([0-9]+)\\)', X[ix:])
    if Match:
        m1 = int(Match.group(1))
        m2 = int(Match.group(2))
        Grp_Mul.append(m2)
        Grp_End.append(ix + len(Match.group(0)) + m1)
        Grp_Cnt.append(0)
        ix += len(Match.group(0))
    else:
        Grp_Cnt[-1] += 1
        while len(Grp_End) > 0 and ix >= Grp_End[-1] - 1:
            mul = Grp_Mul.pop()
            cnt = Grp_Cnt.pop()
            Grp_End.pop()
            if len(Grp_Cnt) > 0:
                Grp_Cnt[-1] += cnt * mul
            else:
                ans2 += cnt * mul
        ix += 1
print(ans2)

