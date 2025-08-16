import sys
from collections import Counter

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]

# parts 1 and 2
num_char = len(X[0])
ans1 = ''
ans2 = ''
for i in range(num_char):
    Cnt = Counter([x[i] for x in X])
    max_cnt = max(Cnt.values())
    min_cnt = min(Cnt.values())
    for char, n in Cnt.items():
        if n == max_cnt:
            ans1 += char
        if n == min_cnt:
            ans2 += char
print(ans1)
print(ans2)

