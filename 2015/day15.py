import sys
import itertools

def bake(Tsp, Ingred, calories = None):
    Cookie = {}
    for name, tsp in Tsp.items():
        for prop, num in Ingred[name].items():
            if prop not in Cookie.keys():
                Cookie[prop] = 0
            Cookie[prop] += tsp * num
    tot = 1
    for prop, num in Cookie.items():
        if num < 0:
            return 0
        elif prop != 'calories':
            tot *= num
    if calories is not None and Cookie['calories'] != calories:
        return 0
    return tot

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Ingred = {}
Prop = set()
for x in X:
    name, xs = x.split(': ')
    xss = xs.split(', ')
    Ingred[name] = {}
    for xsss in xss:
        prop, num = xsss.split(' ')
        Ingred[name][prop] = int(num)
        Prop.add(prop)

# part 1
ntsp = 100
max_score = 0
Ingred_Name = list(Ingred.keys())
Ingred_It = [ range(ntsp+1) for _ in range(len(Ingred_Name)) ]
for combo in itertools.product(*Ingred_It):
    if sum(combo) > ntsp:
        continue
    Tsp = {}
    for i, name in enumerate(Ingred_Name):
        Tsp[name] = combo[i]
    score = bake(Tsp, Ingred, calories = None)
    if score > max_score:
        max_score = score
ans1 = max_score
print(ans1)

# part 2
ntsp = 100
max_score = 0
Ingred_Name = list(Ingred.keys())
Ingred_It = [ range(ntsp+1) for _ in range(len(Ingred_Name)) ]
for combo in itertools.product(*Ingred_It):
    if sum(combo) > ntsp:
        continue
    Tsp = {}
    for i, name in enumerate(Ingred_Name):
        Tsp[name] = combo[i]
    score = bake(Tsp, Ingred, calories = 500)
    if score > max_score:
        max_score = score
ans2 = max_score
print(ans2)

