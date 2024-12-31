import sys
from collections import defaultdict

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]
Cxn = defaultdict(set)
for x in X:
    c0,c1 = x.split('-')
    t = set([c0,c1])
    Cxn[c0] |= t
    Cxn[c1] |= t

# part 1
Source = list(Cxn.keys())
ans1 = 0
for i in range(len(Source)):
    s1 = Source[i]
    t1 = Cxn[s1]
    for j in range(i+1,len(Source)):
        s2 = Source[j]
        t2 = Cxn[s2]
        for k in range(j+1,len(Source)):
            s3 = Source[k]
            t3 = Cxn[s3]
            u = t1 & t2 & t3
            if s1 in u and s2 in u and s3 in u and \
            (s1.startswith('t') or s2.startswith('t') or s3.startswith('t')):
                ans1 += 1
print(ans1)

# part 2
Grp = []
for source,target in Cxn.items():
    # check for existing groups
    for grp in Grp:
        if all(g in target for g in grp):
            grp.add(source)
    # make new groups
    for t in target:
        if t != source:
            Grp.append(set([source, t]))
maxlen = 0
for grp in Grp:
    if len(grp) > maxlen:
        maxlen = len(grp)
        longest = grp
ans2 = ','.join(sorted(list(longest)))
print(ans2)
