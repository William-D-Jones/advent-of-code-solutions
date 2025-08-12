import sys
import itertools

def sum_happy(Arrange, Happy):
    tot_happy = 0
    n = len(Arrange)
    for i, p1 in enumerate(Arrange):
        p0 = Arrange[(i-1)%n]
        p2 = Arrange[(i+1)%n]
        h0 = Happy[p1][p0]
        h2 = Happy[p1][p2]
        tot_happy += h0 + h2
    return tot_happy

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Happy = {}
People = set()
for x in X:
    xs = x.split(' ')
    p1 = xs[0]
    p2 = xs[10][:-1]
    val = int(xs[3])
    if xs[2] == 'gain':
        val *= 1
    elif xs[2] == 'lose':
        val *= -1
    else:
        assert False
    if p1 not in Happy.keys():
        Happy[p1] = {}
    Happy[p1][p2] = val
    People.add(p1)
    People.add(p2)

# part 1
Totals = []
for Arrange in itertools.permutations(list(People)):
    Totals.append( sum_happy(Arrange, Happy) )
ans1 = max(Totals)
print(ans1)

# part 2
Happy['me'] = {}
for p in People:
    Happy['me'][p] = 0
    Happy[p]['me'] = 0
People.add('me')
Totals = []
for Arrange in itertools.permutations(list(People)):
    Totals.append( sum_happy(Arrange, Happy) )
ans2 = max(Totals)
print(ans2)

