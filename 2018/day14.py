import sys

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])
x = int(X)

# part 1
R = [3,7]
i = 0
j = 1
while len(R) < x+10:
    nxt = R[i] + R[j]
    R += list(map(int, list(str(nxt))))
    i = (i + 1 + R[i]) % len(R)
    j = (j + 1 + R[j]) % len(R)
ans1 = ''.join(map(str, R[x:x+10]))
print(ans1)

# part 2
R = ['3','7']
i = 0
j = 1
# each recipe set adds only 1 or 2 digits
# therefore, we do not need to check the whole string
while X not in ''.join(R[-len(X)-1:]):
    nxt = list(str(int(R[i]) + int(R[j])))
    R += nxt
    i = (i + 1 + int(R[i])) % len(R)
    j = (j + 1 + int(R[j])) % len(R)
ix = (''.join(R[-len(X)-1:])).index(X)
ans2 = len(R) - len(X) - (1-ix)
print(ans2)

