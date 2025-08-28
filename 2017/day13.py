import sys

# parsing
X = [ list(map(int, l.strip().split(': '))) for l in open(sys.argv[1], 'r') ]
F = {}
for x in X:
    F[x[0]] = x[1]
lmin = 0
lmax = max(F.keys()) + 1

# part 1
ans1 = 0
for i in F.keys():
    if i % (2 * F[i] - 2) == 0:
        ans1 += i * F[i]
print(ans1)

# part 2
ans2 = 0
while any( (i+ans2) % (2 * F[i] - 2) == 0 for i in F.keys() ):
    ans2 += 1
print(ans2)

