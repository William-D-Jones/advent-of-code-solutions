import sys
import itertools

# parsing
X = [ list(map(int, l.strip().split())) for l in open(sys.argv[1], 'r') ]

# part 1
ans1 = 0
for x in X:
    ans1 += max(x) - min(x)
print(ans1)

# part 2
ans2 = 0
for x in X:
    for n1,n2 in itertools.combinations(x, 2):
        if n1 >= n2 and n1 % n2 == 0:
            ans2 += n1 // n2
        elif n2 >= n1 and n2 % n1 == 0:
            ans2 += n2 // n1
print(ans2)

