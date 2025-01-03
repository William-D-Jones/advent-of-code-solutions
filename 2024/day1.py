import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
l1 = []
l2 = []
for x in X:
    v1, v2 = x.split()
    l1.append(int(v1))
    l2.append(int(v2))

# part 1
ls1 = sorted(l1)
ls2 = sorted(l2)
ans = 0
for num1, num2 in zip(ls1, ls2):
    ans += abs(num1 - num2)
print(ans)

# part 2
ans = 0
for num1 in l1:
    ans += num1 * l2.count(num1)
print(ans)
