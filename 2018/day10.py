import sys
import re
import itertools

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Pnt = []
for x in X:
    M = re.match('^position=<([\\- 0-9]+), ([\\- 0-9]+)> '+\
    'velocity=<([\\- 0-9]+), ([\\- 0-9]+)>$', x)
    Pnt.append( tuple(int(M.group(i).strip()) for i in range(1,5)) )

# parts 1 and 2
# we will minimize the total distance between all pairs of points.
dist_last = sum( abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) for \
p1,p2 in itertools.combinations(Pnt,2) )
dt = 1 # the time change between tries
dx = 1 # the direction of the time change (1 increasing, -1 decreasing)
dt_max = None # the maximum time change between tries
t = 0 # the time
dist_min = dist_last # the minimum distance encountered
while True:
    # adjust the time based on the current time change
    t += dt*dx
    # calculate the new points
    Pnt_Next = [ (x+vx*t,y+vy*t,vx,vy) for x,y,vx,vy in Pnt ]
    # calculate the new distance
    dist = sum( abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) for \
    p1,p2 in itertools.combinations(Pnt_Next,2) )
    # adjust the time change
    if dist - dist_last > 0: # the distance is increasing
        if dt == 1:
            break
        dt = max(dt//10, 1)
        dx *= -1
        dt_max = dt
    if dist - dist_last < 0: # the distance is decreasing
        if dt_max is None or 10*dt <= dt_max:
            dt *= 10
    dist_last = dist
# the last time was best, use that
t -= dt*dx
Pnt_Msg = [ (x+vx*t,y+vy*t,vx,vy) for x,y,vx,vy in Pnt ]
xmin = min(x for x,y,vx,vy in Pnt_Msg)
xmax = max(x for x,y,vx,vy in Pnt_Msg)
ymin = min(y for x,y,vx,vy in Pnt_Msg)
ymax = max(y for x,y,vx,vy in Pnt_Msg)
# setup the message
Msg = [['.' for c in range(xmin,xmax+1)] for r in range(ymin,ymax+1)]
for r in range(ymin,ymax+1):
    rrel = r-ymin
    for c in range(xmin,xmax+1):
        crel = c-xmin
        if any( x==c and y==r for x,y,vx,vy in Pnt_Msg ):
            Msg[rrel][crel] = '#'
ans1 = '\n'.join([''.join(row) for row in Msg])
print(ans1)
ans2 = t
print(t)

