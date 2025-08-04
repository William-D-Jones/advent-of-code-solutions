import sys
from copy import deepcopy

def brick2coord(B):
    Coord = set()
    xmin = min(B[0][0], B[1][0])
    xmax = max(B[0][0], B[1][0])
    ymin = min(B[0][1], B[1][1])
    ymax = max(B[0][1], B[1][1])
    zmin = min(B[0][2], B[1][2])
    zmax = max(B[0][2], B[1][2])
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                Coord.add( (x,y,z) )
    return Coord

def drop_bricks(Brick, check_for_drops = False):
    Occupied = set()
    Fallen = set()
    Brick_Original = deepcopy(Brick)
    for B in Brick:
        Occupied |= brick2coord(B)
    diff = 1
    while diff > 0:
        diff = 0
        for i, B in enumerate(Brick):
            B1, B2 = deepcopy(B)
            Occupied -= brick2coord(B)
            drop = 0
            while True:
                B1[2] -= 1
                B2[2] -= 1
                Coord_Test = brick2coord( [B1, B2] )
                if any( coord in Occupied for coord in Coord_Test) or \
                B1[2] < 1 or B2[2] < 1:
                    B1[2] += 1
                    B2[2] += 1
                    break
                drop += 1
            Occupied |= brick2coord( [B1, B2] )
            if drop > 0:
                Fallen.add(i)
                if len(Fallen) == len(Brick_Original):
                    return len(Fallen)
                Brick[i] = [B1, B2]
                diff += 1
    if check_for_drops:
        return len(Fallen)
    else:
        return Brick

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Brick = []
for x in X:
    c1, c2 = x.split('~')
    t1 = list( map(int, c1.split(',')) )
    t2 = list( map(int, c2.split(',')) )
    Brick.append( [t1, t2] )

# parts 1 and 2
ans1 = 0
ans2 = 0
B1 = drop_bricks(deepcopy(Brick), check_for_drops = False)
for i in range(len(B1)):
    num_drop = drop_bricks( B1[:i] + B1[i+1:], check_for_drops = True)
    if num_drop == 0:
        ans1 += 1
    ans2 += num_drop
print(ans1)
print(ans2) 

