import sys

# parsing
X1,X2 = open(sys.argv[1], 'r').read().strip().split('\n\n')
F = [tuple(map(int,x.split('-'))) for x in X1.split('\n')]
M = list(map(int,X2.split('\n')))

# part 1
ans1 = 0
for m in M:
    if any( f0<=m<=f1 for (f0,f1) in F ):
        ans1 += 1
print(ans1)

# part 2
# merge overlapping ranges
Merge = list(F)
i = 0
while i < len(Merge):
    j = i+1
    while j < len(Merge):
        mi0,mi1 = Merge[i]
        mj0,mj1 = Merge[j]
        if min(mi1,mj1) - max(mi0,mj0) >= 0:
            Merge.pop(i)
            Merge.pop(j-1)
            Merge = Merge[:i] + [(min(mi0,mj0), max(mi1, mj1))] + Merge[i:]
            j = i+1
        else:
            j += 1
    i += 1
# sum the final length of each range
ans2 = sum(m1-m0+1 for m0,m1 in Merge)
print(ans2)

