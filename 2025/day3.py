import sys

# parsing
X = [list(map(int, l.strip())) for l in open(sys.argv[1], 'r')]

# part 1
ans1 = 0
n = 2
for x in X:
    num = 0
    i = -1
    for ix in range(n):
        d = max(x[i+1:len(x)-(n-1-ix)])
        i = x.index(d, i+1)
        num += 10**(n-1-ix) * d
    ans1 += num
print(ans1)

# part 2
ans2 = 0
n = 12
for x in X:
    num = 0
    i = -1
    for ix in range(n):
        d = max(x[i+1:len(x)-(n-1-ix)])
        i = x.index(d, i+1)
        num += 10**(n-1-ix) * d
    ans2 += num
print(ans2)

