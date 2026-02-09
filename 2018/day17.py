import sys
import re
from collections import deque

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Clay = set()
for x in X:
    Mx = re.match('.*x=([0-9.]+).*', x)
    My = re.match('.*y=([0-9.]+).*', x)
    xx = list(map(int, Mx.group(1).split('..')))
    if len(xx) == 1:
        xx.append(xx[0])
    yy = list(map(int, My.group(1).split('..')))
    if len(yy) == 1:
        yy.append(yy[0])
    for r in range(yy[0], yy[1]+1):
        for c in range(xx[0], xx[1]+1):
            Clay.add( (r,c) )
rmin = min(c[0] for c in Clay)
rmax = max(c[0] for c in Clay)

# part 1
Wet = set()
Full = set()
Q = deque([((0,500), ((0,500),))])
while Q:
    (r,c), Drop = Q.popleft()
    if (r+1,c) in Wet and (r+1,c) not in Full:
        continue
    # move down if possible
    elif (r+1,c) not in Clay and (r+1,c) not in Full:
        if r+1<rmin:
            Drop_Next = tuple(list(Drop) + [(r+1,c)])
            Q.append( ((r+1,c), Drop_Next) )
        if rmin<=r+1<=rmax:
            Wet.add( (r+1,c) )
            Drop_Next = tuple(list(Drop) + [(r+1,c)])
            Q.append( ((r+1,c), Drop_Next) )
        elif r+1>rmax:
            continue
    else:
        # move left or right
        c_left = c
        drop_left = False
        c_right = c
        drop_right = False
        Fill = set([(r,c)])
        while (r,c_left-1) not in Clay and (r,c_left-1) not in Full:
            c_left -= 1
            Wet.add( (r,c_left) )
            Fill.add( (r,c_left) )
            if (r+1,c_left) not in Clay and (r+1,c_left) not in Full:
                Q.append( ((r,c_left), Drop) )
                drop_left = True
                break
        while (r,c_right+1) not in Clay and (r,c_right+1) not in Full:
            c_right += 1
            Wet.add( (r,c_right) )
            Fill.add( (r,c_right) )
            if (r+1,c_right) not in Clay and (r+1,c_right) not in Full:
                Q.append( ((r,c_right), Drop) )
                drop_right = True
                break
        # check if the water accumulates
        if not drop_left and not drop_right:
            Full |= Fill
            Drop_Next = list(Drop)
            nr,nc = Drop_Next[-1]
            while (nr,nc) in Full:
                Drop_Next.pop()
                nr,nc = Drop_Next[-1]
            Q.append( ((nr,nc), Drop_Next) )
ans1 = len(Wet)
print(ans1)

# part 2
ans2 = len(Full)
print(ans2)

