import sys
import itertools

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Sz = [int(x) for x in X]

# parts 1 and 2
tot = 150
ans1 = 0
Dict_Combo = {}
for i in range(len(Sz)):
    for combo in itertools.combinations(Sz, i):
        if sum(combo) == tot:
            if i not in Dict_Combo.keys():
                Dict_Combo[i] = 0
            Dict_Combo[i] += 1
            ans1 += 1
print(ans1)
ans2 = Dict_Combo[min(Dict_Combo.keys())]
print(ans2)

