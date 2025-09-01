import sys
import itertools

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
n2 = 0
n3 = 0
for x in X:
    if any(x.count(char) == 2 for char in x):
        n2 += 1
    if any(x.count(char) == 3 for char in x):
        n3 += 1
ans1 = n2*n3
print(ans1)

# part 2
for x1,x2 in itertools.combinations(X, 2):
    if sum( 1 for ix in range(len(x1)) if x1[ix]!=x2[ix] ) == 1:
        ans2 = ''
        for ix in range(len(x1)):
            if x1[ix] == x2[ix]:
                ans2 += x1[ix]
        break
print(ans2)

