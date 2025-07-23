import sys
from collections import Counter

# parsing
X = open(sys.argv[1], 'r').read().strip()
X1,X2 = X.split('\n\n')
Towel = X1.split(', ')
Design = X2.split('\n')

# parts 1 and 2
ans1 = 0
ans2 = 0
for i,design in enumerate(Design):
    Mash = Counter()
    Mash[''] = 1
    while any(len(mash) < len(design) for mash in Mash.keys()):
        Next_Mash = Counter()
        for mash in Mash.keys():
            if len(mash) < len(design): 
                for towel in Towel:
                    next_mash = ''.join([mash, towel])
                    if design.startswith(next_mash):
                        Next_Mash[next_mash] += Mash[mash]
            elif mash == design:
                Next_Mash[mash] += Mash[mash]
        Mash = Next_Mash
    ans1 += 1 if Mash[design] > 0 else 0
    ans2 += Mash[design]
print(ans1)
print(ans2) 

