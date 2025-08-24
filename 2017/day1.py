import sys

# parsing
X = list(map(int, list(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))))

# part 1
ans1 = 0
for i in range(len(X)):
    c1 = X[i]
    c2 = X[(i+1)%len(X)]
    if c1 == c2:
        ans1 += c1
print(ans1)

# part 2
ans2 = 0
for i in range(len(X)):
    c1 = X[i]
    c2 = X[(i+len(X)//2)%len(X)]
    if c1 == c2:
        ans2 += c1
print(ans2)

