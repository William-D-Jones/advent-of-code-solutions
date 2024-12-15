import sys
from copy import deepcopy

DICT_MOVE = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
def walk(coord, dx, sign, expansion = None):
    dest = (coord[0] + DICT_MOVE[dx][0] * sign, \
    coord[1] + DICT_MOVE[dx][1] * sign)
    if expansion is not None:
        dest += (1,) if expansion else (0,)
    return dest

# parsing
X = open(sys.argv[1], 'r').read().strip()
inr, inm = X.split('\n\n')
Room_In = [list(l) for l in inr.split('\n')]
Moves_In = list(''.join(inm.split('\n')))
# find the robot
R = len(Room_In)
C = len(Room_In[0])
for r in range(R):
    for c in range(C):
        if Room_In[r][c] == '@':
            robot = (r,c)
            break

# part 1
Room = deepcopy(Room_In)
Moves = deepcopy(Moves_In)
for i in range(len(Moves)):
    dx = Moves.pop(0)
    target = walk(robot, dx, 1)
    if Room[target[0]][target[1]] == '.':
        Room[robot[0]][robot[1]] = '.'
        robot = deepcopy(target)
        Room[robot[0]][robot[1]] = '@'
    elif Room[target[0]][target[1]] == 'O':
        while Room[target[0]][target[1]] == 'O':
            target = walk(target, dx, 1)
        if Room[target[0]][target[1]] == '.':
            Room[target[0]][target[1]] = 'O'
            while target != robot:
                target = walk(target, dx, -1)
            target = walk(robot, dx, 1)
            Room[robot[0]][robot[1]] = '.'
            robot = deepcopy(target)
            Room[robot[0]][robot[1]] = '@'
        elif Room[target[0]][target[1]] == '#':
            pass
        else:
            assert False
    elif Room[target[0]][target[1]] == '#': 
        pass
    else:
        assert False
ans1 = 0
for r in range(R):
    for c in range(C):
        if Room[r][c] == 'O':
            ans1 += 100 * r + c
print(ans1)

# part 2
# make the new room
Room = []
for r in range(R):
    Room.append([])
    for c in range(C):
        if Room_In[r][c] == '#':
            Room[-1] += ['#', '#']
        elif Room_In[r][c] == 'O':
            Room[-1] += ['[', ']']
        elif Room_In[r][c] == '.':
            Room[-1] += ['.', '.']
        elif Room_In[r][c] == '@':
            Room[-1] += ['@', '.']
        else:
            assert False
R = len(Room)
C = len(Room[0])
for r in range(R):
    for c in range(C):
        if Room[r][c] == '@':
            robot = (r,c)
            break
Moves = deepcopy(Moves_In)
for i in range(len(Moves)):
    dx = Moves.pop(0)
    target = walk(robot, dx, 1)
    if Room[target[0]][target[1]] == '.':
        Room[robot[0]][robot[1]] = '.'
        robot = deepcopy(target)
        Room[robot[0]][robot[1]] = '@'
    elif Room[target[0]][target[1]] in '[]' and dx in '<>':
        while Room[target[0]][target[1]] in '[]':
            target = walk(target, dx, 1)
        if Room[target[0]][target[1]] == '.':
            while target != robot:
                new_target = walk(target, dx, -1)
                Room[target[0]][target[1]] = Room[new_target[0]][new_target[1]]
                target = deepcopy(new_target)
            target = walk(robot, dx, 1)
            Room[robot[0]][robot[1]] = '.'
            robot = deepcopy(target[0:2])
        elif Room[target[0]][target[1]] == '#':
            pass
        else:
            assert False
    elif Room[target[0]][target[1]] in '[]' and dx in '^v':
        # here, the last entry in every tuple indicates if an expansion occurred
        # 0 for no expansion, 1 for an expansion
        if Room[target[0]][target[1]] == '[':
            Target = [target + (0,), walk(target, '>', 1, True)]
        elif Room[target[0]][target[1]] == ']':
            Target = [walk(target, '<', 1, True), target + (0,)]
        else:
            assert False
        go = True
        Back = [Target]
        while not all(Room[target[0]][target[1]] == '.' for target in Target):
            New_Target = []
            for target in Target:
                if Room[target[0]][target[1]] == '.':
                    continue
                new_target = walk(target, dx, 1, False)
                if walk(target, dx, 1, True) in New_Target:
                    New_Target.remove(walk(target, dx, 1, True)) 
                if Room[new_target[0]][new_target[1]] == '#':
                    go = False
                    break
                elif Room[new_target[0]][new_target[1]] == '[':
                    New_Target.append(new_target)
                    if walk(new_target, '>', 1, False) not in New_Target:
                        New_Target.append(walk(new_target, '>', 1, True))
                elif Room[new_target[0]][new_target[1]] == ']': 
                    if walk(new_target, '<', 1, False) not in New_Target:
                        New_Target.append(walk(new_target, '<', 1, True))
                    New_Target.append(new_target)
                elif Room[new_target[0]][new_target[1]] == '.': 
                    New_Target.append(new_target)
                else:
                    assert False
            if not go:
                break
            Target = deepcopy(New_Target)
            Back.append(Target)
        if go:
            while Back:
                Target = Back.pop()
                for target in Target:
                    if target[2] == 0:
                        back = walk(target, dx, -1)
                        Room[target[0]][target[1]] = Room[back[0]][back[1]]
                        Room[back[0]][back[1]] = '.'
                        if Room[target[0]][target[1]] == '@':
                            robot = deepcopy(target[0:2])
    elif Room[target[0]][target[1]] == '#': 
        pass
    else:
        assert False
ans2 = 0
for r in range(R):
    for c in range(C):
        if Room[r][c] == '[':
            ans2 += 100 * r + c
print(ans2)

