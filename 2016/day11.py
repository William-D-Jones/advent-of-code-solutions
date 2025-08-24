import sys
import re
from collections import deque
from copy import deepcopy
import itertools

FLOOR = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4}
MIN_FLOOR = min(FLOOR.values())
MAX_FLOOR = max(FLOOR.values())

def is_safe(Items):
    """
    Determine if a collection of generators and microchips is valid.
    Unpaired microchips can only be among other unpaired microchips.
    """
    C = []
    G = []
    P = []
    for eq in Items:
        if eq[1] == 'generator':
            mate_type = 'microchip'
        elif eq[1] == 'microchip':
            mate_type = 'generator'
        else:
            assert False
        if (eq[0], mate_type) not in Items:
            if eq[1] == 'generator':
                G.append(eq)
            elif eq[1] == 'microchip':
                C.append(eq)
            else:
                assert False
        else:
            P.append(eq)
    if (len(P) > 0 or len(G) > 0) and len(C) > 0:
        return False
    else:
        return True

def select_loads(Equip, floor):
    Eq_src = [eq for eq in Equip if Equip[eq] == floor]
    min_occupied = min(Equip.values())
    max_occupied = max(Equip.values())
    num_to_do = sum([1 for f in Equip.values() if f < MAX_FLOOR])
    L_out_up = []
    L_out_down = []
    for sz in (1,2):
        for L in itertools.combinations(Eq_src, sz):
            Eq_left = [eq for eq in Eq_src if eq not in L]
            if not is_safe(Eq_left):
                continue
            L_up = L
            L_down = L
            for f_up in range(floor+1, MAX_FLOOR+1):
                if f_up > MAX_FLOOR or not is_safe([eq for eq in Equip if \
                Equip[eq] == f_up or eq in L_up]) or \
                (f_up > max_occupied and len(L_up) == 1 and \
                num_to_do > len(L_up)):
                    L_up = []
                    break
                if L_up:
                    L_out_up.append( (f_up,L) )
            for f_down in range(floor-1, MIN_FLOOR-1, -1):
                if f_down < min_occupied or not is_safe([eq for eq in Equip if \
                Equip[eq] == f_down or eq in L_down]) or \
                (f_down < min_occupied and len(L_down) == 1):
                    L_down = []
                    break
                if L_down:
                    L_out_down.append( (f_down,L) )
    return L_out_up+L_out_down

def get_state(Equip):
    C = []
    G = []
    P = []
    for eq,f_eq in Equip.items():
        if eq[1] == 'generator':
            mate_type = 'microchip'
        elif eq[1] == 'microchip':
            mate_type = 'generator'
        else:
            assert False
        if Equip[ (eq[0], mate_type) ] != f_eq:
            if eq[1] == 'generator':
                G.append(f_eq)
            elif eq[1] == 'microchip':
                C.append(f_eq)
            else:
                assert False
        else:
            P.append(f_eq)
    s = ( tuple(sorted(C)), tuple(sorted(G)), tuple(sorted(P)) )
    return s

def move_equipment(Equip):
    Q_Equip = deque([deepcopy(Equip)])
    Q_Floor = deque([MIN_FLOOR])
    Q_Step = deque([0])
    min_step = None
    Seen = {(get_state(Equip),MIN_FLOOR): 0}
    while Q_Equip:
        #for i in range(len(Q_Equip)):
        #    print(Q_Step[i], Q_Floor[i], Q_Equip[i])
        #print('\n')
        if len(Q_Equip)%10000 == 0:
            print(len(Q_Equip), Q_Step[-1])
        equip = Q_Equip.popleft()
        floor = Q_Floor.popleft()
        step = Q_Step.popleft()
        Loads = select_loads(equip, floor)
        if not Loads:
            continue
        for f_next,L_next in Loads:
            # move the equipment
            equip_next = deepcopy(equip)
            for item in L_next:
                equip_next[item] = f_next
            # adjust the step counter
            step_next = step+abs(f_next-floor)
            if min_step is not None and min_step <= step_next:
                continue
            # check if the state has been seen before
            s = get_state(equip_next)
            if (s,f_next) in Seen.keys() and Seen[(s,f_next)] <= step_next:
                continue
            Seen[(s,f_next)] = step
            # check if we have moved everything to the top floor
            if all(f == MAX_FLOOR for f in equip_next.values()):
                if min_step is None or step_next<min_step:
                    min_step = step_next
                continue
            Q_Equip.append(equip_next)
            Q_Floor.append(f_next)
            Q_Step.append(step_next)
    return min_step

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Equip = {}
for x in X:
    match_floor = re.match('^The ([^ ]+) floor', x)
    match_eq = re.findall('([a-z]+)(-compatible)* (generator|microchip)', x)
    f_eq = FLOOR[match_floor.group(1)]
    for m in match_eq:
        Equip[ (m[0], m[2]) ] = f_eq

# part 1
ans1 = move_equipment(Equip)
print(ans1)

# part 2
Equip[('elerium', 'generator')] = 1
Equip[('elerium', 'microchip')] = 1
Equip[('dilithium', 'generator')] = 1
Equip[('dilithium', 'microchip')] = 1
ans2 = move_equipment(Equip)
print(ans2)

