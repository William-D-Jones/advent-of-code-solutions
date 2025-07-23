import sys
sys.setrecursionlimit(50)
import math
from copy import deepcopy
from collections import defaultdict
import re

DICT_RIGHT = {'^': '>', '>': 'v', 'v': '<', '<': '^'}

def move_guard(guard_map, guard_coord, guard_dir):
    # establish new coordinate
    if guard_dir == '^':
        new_coord = (guard_coord[0] - 1, guard_coord[1])
    elif guard_dir == '<':
        new_coord = (guard_coord[0], guard_coord[1] - 1)
    elif guard_dir == '>':
        new_coord = (guard_coord[0], guard_coord[1] + 1)
    elif guard_dir == 'v':
        new_coord = (guard_coord[0] + 1, guard_coord[1])
    else:
        assert False
    # check the new coordinate
    if not(0 <= new_coord[0] < len(guard_map)) or \
    not(0 <= new_coord[1] < len(guard_map[1])):
        return None, guard_dir
    else:
        # establish new direction
        if guard_map[new_coord[0]][new_coord[1]] == '#':
            return guard_coord, DICT_RIGHT[guard_dir]
        else:
            return new_coord, guard_dir

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
guard_dir_start = None
for i in range(len(X)):
    for j in range(len(X[0])):
        if X[i][j] in '<>^v':
            guard_dir_start = X[i][j]
            X[i][j] = '.'
            guard_coord_start = (i,j)
            break
    if guard_dir_start is not None:
        break

# part 1
guard_coord = deepcopy(guard_coord_start)
guard_dir = guard_dir_start
set_pos = set()
while guard_coord is not None:
    set_pos.add(guard_coord)
    guard_coord, guard_dir = move_guard(X, guard_coord, guard_dir)
print(len(set_pos))

# part 2
set_loop_test = deepcopy(set_pos)
set_loop_test.remove(guard_coord_start)
set_loop = set()
for coord in set_loop_test:
    # setup the new guard status
    set_pos = set()
    guard_map_new = deepcopy(X)
    guard_map_new[coord[0]][coord[1]] = '#'
    guard_coord = deepcopy(guard_coord_start)
    guard_dir = guard_dir_start
    dict_coord_dir = defaultdict(set)
    # walk the guard
    while guard_coord is not None:
        if guard_dir in dict_coord_dir[guard_coord]:
            set_loop.add(coord)
            break
        dict_coord_dir[guard_coord].add(guard_dir)
        guard_coord, guard_dir = \
        move_guard(guard_map_new, guard_coord, guard_dir)
print(len(set_loop))

