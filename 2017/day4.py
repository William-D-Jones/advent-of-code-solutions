import sys

# parsing
X = [ l.strip().split() for l in open(sys.argv[1], 'r') ]

# part 1
ans1 = 0
for x in X:
    valid = True
    for el in x:
        if x.count(el) > 1:
            valid = False
            break
    if valid:
        ans1 += 1
print(ans1)

# part 2
ans2 = 0
for x in X:
    xs = [''.join(sorted(el)) for el in x]
    valid = True
    for el in xs:
        if xs.count(el) > 1:
            valid = False
            break
    if valid:
        ans2 += 1
print(ans2)

