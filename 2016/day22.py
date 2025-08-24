import sys
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Node = {}
for i in range(2,len(X)):
    xs = X[i].split()
    M_coord = re.match('^/dev/grid/node-x([0-9]+)-y([0-9]+)$', xs[0])
    coord = ( int(M_coord.group(2)), int(M_coord.group(1)) )
    # Size, Used, Avail
    vals = tuple(int(val[:-1]) for val in xs[1:-1])
    Node[coord] = vals 
Coords = list(Node.keys())

# part 1
ans1 = 0
for i in range(len(Coords)):
    for j in range(len(Coords)):
        A = Coords[i]
        B = Coords[j]
        if i != j and Node[A][1] != 0 and Node[A][1] <= Node[B][2]:
            ans1 += 1
print(ans1)

# part 2

# get the extrema of the grid
ymin = min(coord[0] for coord in Coords)
ymax = max(coord[0] for coord in Coords)
xmin = min(coord[1] for coord in Coords)
xmax = max(coord[1] for coord in Coords)

# the data node
D = (0,xmax)
# the target node
T = (0,0)

# This grid has a few important characteristics:
# (i) There is exactly one empty node (E). We only ever transfer to this node,
# because no other node can be transferred to.
E = [(y,x) for (y,x) in Node.keys() if Node[(y,x)][1] == 0]
assert len(E) == 1
E = E.pop()
# (ii) All nodes can transfer into the empty node, with one row in exception.
# There is one row of the grid where all but one of the nodes cannot
# transfer to the empty node, and therefore cannot be transferred at all. Only
# one of the nodes in this row can transfer data, and we refer to this as the
# Port node (P).
Block = set()
for i in range(len(Coords)):
    for j in range(len(Coords)):
        A = Coords[i]
        B = Coords[j]
        if i == j:
            continue
        if Node[A][1] != 0 and Node[A][1] <= Node[B][2]:
            assert B == E
        elif B == E:
            Block.add(A)
assert len(Block) == xmax+1-xmin-1
row_block = set([r for (r,c) in Block])
assert len(row_block) == 1
row_block = row_block.pop()
P = [(r,c) for (r,c) in Coords if r == row_block and (r,c) not in Block]
assert len(P) == 1
P = P.pop()
# (iii) Row-wise, the Port node lies between the Empty node and row 0 (where
# the Data node and the Target node lie).
assert E[0]>P[0]>0

# Solve in 2 phases:
# (A) Empty the node to the left of the Data node. This is accomplished in 
# a number of steps equal to the Manhattan distance from the Empty node to the
# Port node, plus the Manhattan distance from the Port node to the node to the
# left of the data node.
ans2 = abs(P[0]-E[0]) + abs(P[1]-E[1])
ans2 += abs(P[0]-D[0]) + abs(P[1]-(D[1]-1))
# (B) Sequentially move the data from the Data node to the Target node.
# (B-i) The data moves one step to the left. The node to the right is empty.
# (B-ii) Four nodes transfer their data to make room to the left of the data.
# * D 0   ==>  0 D *
# * * *        * * *
# This procedure is repeated until the data arrives
ans2 += 5*(xmax-(xmin+1))
ans2 += 1
print(ans2)

