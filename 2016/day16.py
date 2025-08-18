import sys
from copy import copy

def dragon(data, sz):
    while len(data) < sz:
        a = copy(data)
        b = list(copy(data)[::-1])
        b = ''.join(['1' if b[i] == '0' else '0' for i in range(len(b))])
        data = a + '0' + b
    return data[:sz]

def checksum(data):
    out = ''
    for i in range(len(data) // 2):
        if data[2*i:2*i+1] == data[2*i+1:2*i+2]:
            out += '1'
        else:
            out += '0'
    if len(out) % 2 == 0:
        return checksum(out)
    else:
        return out

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
sz = 272
data = dragon(copy(X), sz)
ans1 = checksum(data)
print(ans1)

# part 2
sz = 35651584
data = dragon(copy(X), sz)
ans2 = checksum(data)
print(ans2)

