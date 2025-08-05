import sys
import numpy as np
from collections import deque

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Pos = deque()
Vel = deque()
for x in X:
    spos, svel = x.split(' @ ')
    Pos.append(tuple(map(int, spos.split(','))))
    Vel.append(tuple(map(int, svel.split(','))))

# part 1
xmin = 200000000000000
xmax = 400000000000000
ymin = 200000000000000
ymax = 400000000000000
ans1 = 0
for i in range(len(Pos)):
    for j in range(i+1, len(Pos)):
        # collect the positions and velocities
        xi, yi, zi = Pos[i]
        xj, yj, zj = Pos[j]
        vxi, vyi, vzi = Vel[i]
        vxj, vyj, vzj = Vel[j]
        # solve the simultaneous equations
        tj_denom = vyj/vyi - vxj/vxi
        tj_num = (xj - xi)/vxi - (yj - yi)/vyi
        if tj_denom != 0:
            tj = tj_num / tj_denom # time of crossing for j
            ti = (xj - xi + vxj * tj) / vxi # time of crossing for i
            cx = xi + vxi * ti # crossing x-coordinate
            cy = yi + vyi * ti # crossing y-coordinate
            if tj >= 0 and ti >= 0 and xmin<=cx<=xmax and ymin<=cy<=ymax:
                ans1 += 1
print(ans1)

# part 2

# Let mi be the meeting time between the rock and the ith hailstone.
# Let (rx,ry,rz) be the starting position of the rock, and let (pxi,pyi,pzi)
# by the starting position of the ith hailstone.
# Let (sx,sy,sz) be the velocity of the rock, and let (vxi,vyi,vzi) be the
# velocity of the ith hailstone.
#
# Then we can write the following equations:
# rx + sx * mi = pxi + vxi * mi
# ry + sy * mi = pyi + vyi * mi
# rz + sz * mi = pzi + vzi * mi
# 
# Consider only the x and y axes, and consider the ith and the jth hailstone.
# Solving for mi and mj, and combining equations, we can write:
# (rx-pxi)(vyi-sy) = (ry-pyi)(vxi-sx)
# (rx-pxj)(vyj-sy) = (ry-pyj)(vxj-sx)
#
# Rearranging:
# rx*vyi - rx*sy - pxi*vyi + pxi*sy = ry*vxi - ry*sx - pyi*vxi + pyi*sx
# -rx*vyj + rx*sy + pxj*vyj - pxj*sy = -ry*vxj + ry*sx + pyj*vxj - pyj*sx
#
# Add the 2 equations to eliminate the rx*sy and ry*sx terms as follows:
# rx * (vyi-vyj) + sy * (pxi-pxj) + (pxj*vyj - pxi*vyi) = 
# ry * (vxi-vxj) + sx * (pyi-pyj) + (pyj*vxj - pyi*vxi)
#
# Finally, rearrange to obtain:
# 
# rx * (vyi-vyj) - ry * (vxi-vxj) - sx * (pyi-pyj) + sy * (pxi-pxj) = 
# (pyj*vxj - pyi*vxi) - (pxj*vyj - pxi*vyi)
#
# This is a linear equation in 4 unknowns rx, ry, sx, sy. With 4 such
# equations, we can solve the system of linear equations. Therefore, we need
# to collect data from 5 hailstones.

# collect the coefficients from 5 hailstones
LHS = []
RHS = []
i = 0
for j in range(1, 5):
    # get coefficients for the left-hand side of the equation
    lhs = [ \
    Vel[i][1]-Vel[j][1], \
    Vel[j][0]-Vel[i][0], \
    Pos[j][1]-Pos[i][1], \
    Pos[i][0]-Pos[j][0] \
    ]
    # get constants for the right-hand side of the equation
    rhs = [\
    Pos[j][1]*Vel[j][0] - Pos[i][1]*Vel[i][0] - \
    Pos[j][0]*Vel[j][1] + Pos[i][0]*Vel[i][1] \
    ]
    # record the data
    LHS.append(lhs)
    RHS.append(rhs)

# solve for the x and y positions and velocities of the rock
SOLXY = np.linalg.solve(LHS, RHS)
rx = round( SOLXY[0,0] )
ry = round( SOLXY[1,0] )
sx = round( SOLXY[2,0] )
sy = round( SOLXY[3,0] )

# solve for the meeting time between the rock and 2 hailstones
# From above, we have:
# rx + sx * mi = pxi + vxi * mi
# Rearranging:
# mi = (rx-pxi) / (vxi-sx)
MEET = []
for i in range(2):
    meet = (rx-Pos[i][0]) // (Vel[i][0]-sx)
    MEET.append(meet)

# solve for the z position and velocity of the rock, using 2 hailstones
# rz + sz * mi = pzi + vzi * mi
LHS = []
RHS = []
for i in range(2):
    # get coefficients for the left-hand side of the equation
    lhs = [ \
    1, \
    MEET[i] \
    ]
    # get constants for the right-hand side of the equation
    rhs = [\
    Pos[i][2] + Vel[i][2] * MEET[i] \
    ]
    # record the data
    LHS.append(lhs)
    RHS.append(rhs)
SOLZ = np.linalg.solve(LHS, RHS)
rz = round( SOLZ[0,0] )
sz = round( SOLZ[1,0] )

# produce the final answer
ans2 = rx + ry + rz
print(ans2)


