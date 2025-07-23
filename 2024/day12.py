import sys
from copy import deepcopy

def make_neighbor_set(set_coord, set_exclude, nrow, ncol):
    """
    Returns the neighbors of coordinates in set_coord, excluding any in
    set_exclude and any outside the bounds set by nrow and ncol.

    Each coordinate is a tuple in the format (row, column).
    """
    set_neighbor = set()
    for coord in set_coord:
        up = (coord[0] - 1, coord[1])
        down = (coord[0] + 1, coord[1])
        left = (coord[0], coord[1] - 1)
        right = (coord[0], coord[1] + 1)
        if coord[0] > 0 and not (up in set_exclude):
            set_neighbor.add(up)
        if coord[0] < nrow - 1 and not (down in set_exclude):
            set_neighbor.add(down)
        if coord[1] > 0 and not (left in set_exclude):
            set_neighbor.add(left)
        if coord[1] < ncol - 1 and not (right in set_exclude):
            set_neighbor.add(right)
    return set_neighbor

def merge_perimeters(set_perimeter):
    """
    Given a set of perimeter coordinates in the format (x,y,0|1,0|1), merges the
    perimeters to produce sides. Returns a set of side coordinates, in the
    format [(x1,y1), (x2,y2), k], which means:
    * if x1==x2, runs horizontally above row x1, from the point to the left
    of y1 to the point to the left of y2
    * if y1==y2, runs vertically to the left of column y1, from the point
    above x1 to the point above x2
    * if k==0, the coordinates in the indicated row/column are not occupied
    * if k==1, the coordinates in the indicated row/column are occupied
    """

    Sides = []
    while len(set_perimeter) > 0:
        # get a side to work on
        perim = set_perimeter.pop()
        dir_perim = perim[2]
        occ = perim[3]
        coord_perim = perim[0:2]
        if dir_perim == 0: # a vertical side
            side = [ coord_perim, (coord_perim[0]+1, coord_perim[1]), occ ]
        if dir_perim == 1: # a horizontal side
            side = [ coord_perim, (coord_perim[0], coord_perim[1]+1), occ ]
        # extend the side
        Walk = [-1, 1]
        while not ( all(walk is None for walk in Walk) ):
            for i,walk in enumerate(Walk):
                if walk is not None:
                    # construct a new perimeter coordinate to check
                    new_coord_perim = list(side[0 if walk < 0 else 1])
                    new_coord_perim[dir_perim] += walk if walk < 0 else 0
                    new_coord_perim += [dir_perim, occ]
                    new_coord_perim = tuple(new_coord_perim)
                    if new_coord_perim in set_perimeter:
                        set_perimeter.remove(new_coord_perim)
                        if walk < 0:
                            side[0] = new_coord_perim[0:2]
                        else:
                            new_coord_perim = list(new_coord_perim[0:2])
                            new_coord_perim[dir_perim] += 1
                            side[1] = tuple(new_coord_perim)
                    else:
                        Walk[i] = None
        Sides.append(side)
    return Sides

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
nrow = len(X)
ncol = len(X[0])

# identify regions
Region = [] # each region is a list, (1) crop string, (2) set of coordinates
for r in range(nrow):
    for c in range(ncol):
        crop = X[r][c]
        in_existing = False
        for region in Region:
            if (r, c) in region[1]:
                in_existing = True
                break
        if not in_existing:
            set_region = set( [(r, c)] )
            set_neighbor = set( [(r, c)] )
            while len(set_neighbor) > 0:
                set_new_neighbor = make_neighbor_set( \
                set_neighbor, set_region, nrow, ncol )
                set_neighbor = set()
                for neighbor in set_new_neighbor:
                    if X[neighbor[0]][neighbor[1]] == crop:
                        set_region.add(neighbor)
                        set_neighbor.add(neighbor)
            Region.append( [crop, set_region] )

# parts 1 and 2
ans1 = 0
ans2 = 0
for crop, Coord in Region:
    area = len(Coord)
    perim = 0
    # make a set to hold the perimeter coordinates
    # A perimeter coordinate (x,y,1) means there is a (horizontal) side above 
    # the coordinate at position (x,y). A perimeter coordinate (x,y,0) means 
    # there is a vertical side to the left of the coordinate at position (x,y).
    set_perim = set()
    # part 1: calculate the perimeter
    for coord in Coord:
        # check the up neighbor
        if (coord[0]-1, coord[1]) not in Coord:
            perim += 1
            set_perim.add( (coord[0], coord[1], 1, 1) )
        # check the down neighbor
        if (coord[0]+1, coord[1]) not in Coord:
            perim += 1
            set_perim.add( (coord[0]+1, coord[1], 1, 0) )
        # check the left neighbor
        if (coord[0], coord[1]-1) not in Coord:
            perim += 1
            set_perim.add( (coord[0], coord[1], 0, 1) )
        # check the right neighbor
        if (coord[0], coord[1]+1) not in Coord:
            perim += 1
            set_perim.add( (coord[0], coord[1]+1, 0, 0) )
    ans1 += area * perim
    # part 2: walk around the perimeter
    sides = merge_perimeters(set_perim)
    ans2 += area * len(sides)
print(ans1)
print(ans2)
