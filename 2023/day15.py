import sys
from collections import defaultdict, deque

# parsing
X = (''.join([ l.strip() for l in open(sys.argv[1], 'r') ])).split(',')

def hash(chars):
    h = 0
    for char in chars:
        h += ord(char)
        h *= 17
        h %= 256
    return h

# part 1
L1 = []
for chars in X:
    L1.append(hash(chars))
ans1 = sum(L1)
print(ans1)

# part 2
Box = defaultdict(list)
for chars in X:
    if "=" in chars:
        lbl, foc = chars.split("=")
        h = hash(lbl)
        f = int(foc)
        try:
            i = [lens[0] for lens in Box[h]].index(lbl)
            Box[h][i] = (lbl, f)
        except:
            Box[h].append( (lbl, f) )
    elif "-" in chars:
        lbl = chars[:-1]
        h = hash(lbl)
        try:
            i = [lens[0] for lens in Box[h]].index(lbl)
            Box[h].pop(i)
        except:
            pass
    else:
        assert False
ans2 = 0
for h in range(256):
    if len(Box[h]) > 0:
        for i, lens in enumerate(Box[h]):
            ans2 += (h + 1) * (i + 1) * lens[1]
print(ans2)

