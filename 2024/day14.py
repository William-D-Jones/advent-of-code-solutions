import sys
from copy import deepcopy

# parsing
Pos_Start = []
Vel = []
X = [l.strip() for l in open(sys.argv[1], 'r')]
for x in X:
    pos, vel = x.split()
    Pos_Start.append( list(map(int, pos[2:].split(','))) )
    Vel.append( list(map(int, vel[2:].split(','))) )
nrow = 103
ncol = 101

# part 1
Pos = deepcopy(Pos_Start)
nsec = 100
for i in range(len(Pos)):
    assert 0 <= Pos[i][0] < ncol
    assert 0 <= Pos[i][1] < nrow
    Pos[i][0] = (Pos[i][0] + Vel[i][0] * nsec) % ncol
    Pos[i][1] = (Pos[i][1] + Vel[i][1] * nsec) % nrow
Q = [0, 0, 0, 0] # quadrants are clockwise from top left
qrow = nrow // 2
qcol = ncol // 2
for robot in Pos:
    assert 0 <= robot[0] < ncol
    assert 0 <= robot[1] < nrow
    if robot[0] < qcol and robot[1] < qrow:
        Q[0] += 1
    elif qcol+1 <= robot[0] and robot[1] < qrow:
        Q[1] += 1
    elif qcol+1 <= robot[0] and qrow+1 <= robot[1]:
        Q[2] += 1
    elif robot[0] < qcol and qrow+1 <= robot[1]:
        Q[3] += 1
ans1 = 1
for q in Q:
    ans1 *= q
print(ans1)

# part 2
Pos = deepcopy(Pos_Start)
neighbor_max = 0
for sec in range(1, nrow * ncol):
    Pic = [[' ' for c in range(ncol)] for r in range(nrow)]
    for i in range(len(Pos)):
        assert 0 <= Pos[i][0] < ncol
        assert 0 <= Pos[i][1] < nrow
        Pos[i][0] = (Pos[i][0] + Vel[i][0] * 1) % ncol
        Pos[i][1] = (Pos[i][1] + Vel[i][1] * 1) % nrow
        Pic[Pos[i][1]][Pos[i][0]] = '#'
    # to find the Christmas tree, identify robots with direct neighbors
    neighbor_score = 0
    Pos_Checked = deepcopy(Pos)
    while Pos_Checked:
        pos = Pos_Checked.pop()
        Neighbors = [[pos[0]-1, pos[1]], [pos[0]+1, pos[1]],\
        [pos[0], pos[1]-1], [pos[0], pos[1]+1]]
        for neighbor in Neighbors:
            if neighbor in Pos_Checked:
                neighbor_score += 1
    if neighbor_score > 500:
        neighbor_max = neighbor_score
        print('The number of seconds that have elapsed is: ',sec)
        print('The neighbor score is: ',neighbor_max)
        print('\n'.join([''.join(line) for line in Pic]))
        break

