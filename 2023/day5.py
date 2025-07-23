import sys
from copy import deepcopy
# from collections import defaultdict
# import re
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Xc = '\n'.join(X).split('\n\n')

# converting
def convert(lconvert, valin):
    self = True
    for l in lconvert:
        dest, source, r = l
        if valin >= source and valin < source + r:
            valout = valin - source + dest
            self = False
            break
    if not self:
        return valout
    else:
        return valin
def stepconvert(dkey, dconvert, valin, keyin, keyout):
    key = keyin
    val = valin
    while key != keyout:
        lconvert = dconvert[key]
        val = convert(lconvert, val)
        key = dkey[key]
    return val
def rsplit(lconvert, rin):
    lout = []
    rnow = [rin]
    while len(rnow) > 0:
        for i,l in enumerate(lconvert):
            dest, source, r = l
            o = min([source + r, rnow[-1][1]]) - max([source, rnow[-1][0]])
            if o > 0:
                rpop = rnow.pop()
                if rpop[0] < source:
                    rnow.append([rpop[0], source])
                    left = source
                else:
                    left = rpop[0]
                if rpop[1] > source + r:
                    rnow.append([source + r, rpop[1]])
                    right = source + r
                else:
                    right = rpop[1]
                lout.append([left, right])
                break
            if i == len(lconvert) - 1:
                rpop = rnow.pop()
                lout.append(rpop)
    return lout
def rconvert(lconvert, rin):
    rout = []
    self = True
    for l in lconvert:
        dest, source, r = l
        if rin[0] >= source and rin[1] <= source + r:
            rout.append(rin[0] - source + dest)
            rout.append(rin[1] - source + dest)
            self = False
            break
    if not self:
        return rout
    else:
        return rin
def rstepconvert(dkey, dconvert, rin, keyin, keyout):
    key = keyin
    rdo = [rin]
    while key != keyout:
        #print("A new conversion step is beginning...")
        #print("The key is: ", key)
        #print("The ranges to do are: ", rdo)
        lconvert = dconvert[key]
        #print("The conversion list is: ", lconvert)
        rdone = []
        while len(rdo) > 0:
            #print("We performed a split...")
            #print("The split input was: ", rdo[-1])
            lsplitin = rsplit(lconvert, rdo.pop())
            #print("The split output was: ", lsplitin)
            for splitin in lsplitin:
                rdone.append(rconvert(lconvert, splitin))
            #print("After conversion, the ranges were: ", rdone)
        key = dkey[key]
        rdo = deepcopy(rdone)
    return rdone

# parse input
dkey = {}
dconvert = {}
for i,x in enumerate(Xc):
    s = x.strip().split()
    if i == 0:
        Seeds = [int(s[j]) for j in range(1, len(s))]
    else:
        lconvert = []
        for j,R in enumerate(s):
            if j == 0:
                key1,key2 = R.split('-to-')
                dkey[key1] = key2
            if (j - 2) % 3 == 0:
                lconvert.append([int(s[j]), int(s[j+1]), int(s[j+2])])
        dconvert[key1] = lconvert

# part 1
Loc = []
for seed in Seeds:
    Loc.append(stepconvert(dkey, dconvert, seed, 'seed', 'location'))
print(min(Loc))

# part 2
LocR = []
rin = []
for i,seed in enumerate(Seeds):
    if i % 2 == 0:
        start = Seeds[i]
        stop = start + Seeds[i+1]
        rin.append([start, stop])
for r in rin:
    LocR = LocR + rstepconvert(dkey, dconvert, r, 'seed', 'location')
for i,l in enumerate(LocR):
    if i == 0:
        mloc = l[0]
    else:
        if l[0] < mloc:
            mloc = l[0]
print(mloc)

