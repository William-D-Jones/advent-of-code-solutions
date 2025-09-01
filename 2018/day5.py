import sys

A = ord('A')
a = ord('a')
Z = ord('Z')
z = ord('z')

# parsing
X = list(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
i = 0
X1 = list(X)
while i < len(X1)-1:
    if (a<=ord(X1[i])<=z and chr(ord(X1[i])-a+A) == X1[i+1]) or \
    (A<=ord(X1[i])<=Z and chr(ord(X1[i])-A+a) == X1[i+1]):
        X1.pop(i)
        X1.pop(i)
        i -= 1
    else:
        i += 1
ans1 = len(X1)
print(ans1)

# part 2
D = {}
for ix in range(a, z+1):
    c1 = chr(ix)
    c2 = chr(ix-a+A)
    i = 0
    if c1 not in X and c2 not in X:
        continue
    X1 = list(x for x in X if x != c1 and x != c2)
    while i < len(X1)-1:
        if (a<=ord(X1[i])<=z and chr(ord(X1[i])-a+A) == X1[i+1]) or \
        (A<=ord(X1[i])<=Z and chr(ord(X1[i])-A+a) == X1[i+1]):
            X1.pop(i)
            X1.pop(i)
            i -= 1
        else:
            i += 1
    D[chr(ix)] = len(X1)
ans2 = min(D.values())
print(ans2)

