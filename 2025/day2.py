import sys
import re

# parsing
X = open(sys.argv[1], 'r').read().strip().split(',')
I = [tuple(map(int,x.split('-'))) for x in X]

# part 1
ans1 = 0
for i0,i1 in I:
    for i in range(i0,i1+1):
        s = str(i)
        M = re.match(r'^([0-9]+)\1$', s)
        if M:
            ans1 += i
print(ans1)
    
# part 2
ans2 = 0
for i0,i1 in I:
    for i in range(i0,i1+1):
        s = str(i)
        M = re.match(r'^([0-9]+)\1+$', s)
        if M:
            ans2 += i
print(ans2)

