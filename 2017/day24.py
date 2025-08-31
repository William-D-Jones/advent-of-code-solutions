import sys
from collections import deque, Counter

# parsing
X = [ tuple(map(int, l.strip().split('/'))) for l in open(sys.argv[1], 'r') ]
assert all(X.count(x) == 1 for x in X)

# parts 1 and 2
Q = deque([x] for x in X if 0 in x)
End = deque(x[0][1] if x[0][0] == 0 else x[0][0] for x in Q)
Strength = Counter()
while Q:
    B = Q.popleft()
    end = End.popleft()
    Join = [x for x in X if x not in B and end in x]
    if not Join:
        strength = sum(x[0] + x[1] for x in B)
        if strength >= Strength[len(B)]:
            Strength[len(B)] = strength
    for j in Join:
        Q.append(B + [j])
        End.append(j[1] if j[0] == end else j[0])
ans1 = max(Strength.values())
ans2 = Strength[max(Strength.keys())]
print(ans1)
print(ans2)

