import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Block = []
for x in X:
    Block.append( tuple(map(int, x.split('-'))) )

# part 1
# merge overlapping ranges of blocked addresses
Block = sorted(Block)[::-1]
Merge = []
while Block:
    bs,be = Block.pop()
    found = False
    for i, (ms,me) in enumerate(Merge):
        if min(be,me) - max(bs,ms) >= -1:
            Merge[i] = (min(bs,ms), max(be,me))
            found = True
            break
    if not found:
        Merge.append( (bs,be) )
# find the first allowed IP
if Merge[0][0] == 0:
    ans1 = Merge[0][1] + 1
else:
    ans1 = 0
print(ans1)

# part 2
s = 0
ans2 = 0
for ms,me in Merge:
    ans2 += ms-s
    s = me+1
ans2 += 4294967295-me
print(ans2)
    
