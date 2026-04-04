import sys

# parsing
X = [int(line) for line in open(sys.argv[1], 'r')]

# part 1
ans1 = sum( m // 3 - 2 for m in X )
print(ans1)

# part 2
ans2 = 0
for m in X:
    f = m // 3 - 2
    while f > 0:
        ans2 += f
        f = f // 3 - 2
print(ans2)

