import sys
from collections import deque

D = [ (1,0), (0,-1), (-1,0), (0,1) ]

def is_open(coord, fav):
    x = coord[1]
    y = coord[0]
    s = bin(x*x + 3*x + 2*x*y + y + y*y + fav)[2:]
    if s.count('1') % 2 == 0:
        return True
    else:
        return False

# parsing
X = int(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
Start = (1,1)
End = (39,31)
Pos = deque( [Start] )
Step = deque( [0] )
min_step = None
Seen = { Start: 0 }
while Pos:
    r,c = Pos.popleft()
    step = Step.popleft()
    if min_step is not None and step > min_step:
        continue
    for dr,dc in D:
        nr = r+dr
        nc = c+dc
        if nr >= 0 and nc >= 0 and \
        ((nr,nc) not in Seen.keys() or Seen[(nr,nc)] > step+1) and \
        is_open( (nr,nc), X ):
            Seen[ (nr,nc) ] = step+1
            if (nr,nc) == End:
                min_step = step+1
            else:
                Pos.append( (nr,nc) )
                Step.append( step+1 )
ans1 = min_step
print(ans1)

# part 2
Start = (1,1)
Pos = deque( [Start] )
Step = deque( [0] )
Seen = { Start: 0 }
nstep = 50
while Pos:
    r,c = Pos.popleft()
    step = Step.popleft()
    if step+1 > nstep:
        continue
    for dr,dc in D:
        nr = r+dr
        nc = c+dc
        if nr >= 0 and nc >= 0 and \
        ((nr,nc) not in Seen.keys() or Seen[(nr,nc)] > step+1) and \
        is_open( (nr,nc), X ):
            Seen[ (nr,nc) ] = step+1
            Pos.append( (nr,nc) )
            Step.append( step+1 )
ans2 = len(Seen.keys())
print(ans2)

