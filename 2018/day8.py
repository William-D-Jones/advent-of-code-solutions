import sys

# parsing
X = \
list(map(int, ''.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split()))

# parts 1 and 2
Q = list(X)
ix = [ [0,1] ]
MQ = [] # the metadata queue
Val = [[]] # the values of the nodes in memory
ans1 = 0
while Q:
    ix[-1][0] += 1
    nchild = Q.pop(0)
    nmeta = Q.pop(0)
    if nchild == 0:
        # consume the metadata
        val = 0
        for _ in range(nmeta):
            meta = Q.pop(0)
            ans1 += meta
            val += meta
        Val[-1].append(val)
        # go to the next sibling
        while len(ix) > 0 and ix[-1][0] >= ix[-1][1]:
            ix.pop()
            if len(MQ) > 0:
                nmeta = MQ.pop()
                Sib = Val.pop()
                val = 0
                for _ in range(nmeta):
                    meta = Q.pop(0)
                    ans1 += meta
                    val += Sib[meta-1] if 0<=meta-1<len(Sib) else 0
                Val[-1].append(val)
    elif nchild > 0:
        ix.append( [0,nchild] )
        MQ.append( nmeta )
        Val.append([])
    else:
        assert False
print(ans1)
ans2 = Val.pop().pop()
print(ans2)

