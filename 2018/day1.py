import sys

# parsing
X = [ int(l.strip()) for l in open(sys.argv[1], 'r') ]

# part 1
ans1 = sum(X)
print(ans1)

# part 2
freq = 0
Seen = set()
i = 0
while freq not in Seen:
    Seen.add(freq)
    freq += X[i]
    i = (i + 1) % len(X)
ans2 = freq
print(ans2)

