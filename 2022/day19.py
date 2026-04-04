import sys
import re
from collections import defaultdict
import heapq

def get_max_geode(Mv, Start, max_time):
    max_geode = 0
    Seen = {Start: 0}
    Q = []
    heapq.heappush( Q, (max_time, Start, tuple()) )
    # We can produce at most one robot per turn. For each resource, determine
    # the maximum number of that resource needed to buy any robot, and 
    # produce no more than this number of robots for that resource.
    Max_Rob = tuple(\
    -min(Z) for Z in zip(*tuple(Move_Res for Move_Res, Move_Rob in Mv)))
    while Q:
        time_left, State, Block = heapq.heappop(Q)
        # get the new time
        time_next = time_left - 1
        # parse the state
        State_Res = [state[0] for state in State]
        State_Rob = [state[1] for state in State]
        # check if sufficient time remains to beat the maximum geode count
        if max_geode >= State_Res[0] + \
        (2 * State_Rob[0] + time_left - 1) * (time_left) // 2:
            continue
        # try all possible moves
        buy = True
        Block_Next = []
        for ix_move, (Move_Res, Move_Rob) in enumerate(Mv):
            if ix_move in Block:
                continue
            if ix_move <= 0 and time_next <= 3:
                continue
            elif ix_move <= 1 and time_next <= 2:
                continue
            elif ix_move <= 2 and time_next <= 1:
                continue
            elif ix_move <= 3 and time_next <= 0:
                continue
            # In general, we should always make a move if one is available.
            # However, all moves consume the common resource, ore. Therefore, it
            # may be best to make no move in order to save ore for a later 
            # purchase. We should only do this if (i) we have robots available
            # to make a different purchase and (ii) we have insufficient 
            # resources to make that purchase.
            if ix_move == len(Mv)-1 and buy:
                continue
            # check if the move is valid
            State_Res_Move = tuple(sum(Z) for Z in zip(State_Res, Move_Res))
            if any(z < 0 for z in State_Res_Move):
                if buy and all(state_rob > 0 for \
                mv_res, state_rob in zip(Move_Res, State_Rob) if \
                mv_res != 0):
                    buy = False
                continue
            if ix_move != len(Mv)-1:
                Block_Next.append(ix_move)
            # get the new state of resources
            State_Res_Next = \
            tuple(sum(Z) for Z in zip(State_Res_Move, State_Rob))
            # get the new state of robots
            State_Rob_Next = tuple(sum(Z) for Z in zip(State_Rob, Move_Rob))
            if any(state_rob > max_rob for \
            state_rob, max_rob in zip(State_Rob_Next[1:], Max_Rob[1:])):
                continue
            # get the new final state
            State_Next = tuple(zip(State_Res_Next, State_Rob_Next))
            if State_Next not in Seen or Seen[State_Next] < time_next:
                Seen[State_Next] = time_next
                max_geode = max(max_geode, \
                State_Next[0][0] + time_next * State_Next[0][1])
                if ix_move == len(Mv)-1:
                    heapq.heappush(Q, \
                    (time_next, State_Next, tuple(Block_Next)))
                else:
                    heapq.heappush(Q, (time_next, State_Next, tuple()))
    return max_geode

# parsing
X = [line.split(': ') for line in open(sys.argv[1], 'r')]
# parse the cost of each robot in each blueprint
Cost = defaultdict(list)
IX = list()
for x0,x1 in X:
    M0 = re.match(r'^Blueprint ([0-9]+)$', x0)
    ix = int(M0.group(1))
    for xc in x1.strip().split('. '):
        MC = re.match('^Each ([^ ]+) robot costs ([^.]+)\\.*$', xc.strip())
        rob = MC.group(1)
        for C in MC.group(2).split(' and '):
            num, res = C.split(' ')
            Cost[(ix, rob)].append( (int(num), res) )
    IX.append(ix)
IX = sorted(IX)
# extract all the resources and which resources are currencies to build robots
Res = {rob for ix, rob in Cost.keys()}
Cur = set()
for C in Cost.values():
    for num, res in C:
        Cur.add(res)

# For this problem, we make some key simplifying assumptions.
# (i) There is a strict priority order for resources and robots in the puzzle.
# We can identify this order.
# (i-a) The highest priority resource is the geode, as given in the problem:
P0 = 'geode'
# (i-b) No robot requires geodes to build:
assert P0 not in Cur
# (i-c) One resource is required for every robot, and this is ore, produced by
# the robot we start with. Furthermore, each robot requires either the common 
# resource only or the common resource and exactly one other resource. 
# If the robot requires a resource in addition to the common resource, that 
# second resource is not required for any other robot:
Tar = defaultdict(set)
for (ix, rob), C in Cost.items():
    for num, res in C:
        Tar[res].add(rob)
Cmn = set()
Unis = defaultdict(set)
for res, Rob in Tar.items():
    if len(Rob) == 1:
        Unis[list(Rob)[0]].add(res)
    elif len(Rob) == len(Res):
        Cmn.add(res)
    else:
        assert False
assert len(Cmn) == 1
cmn = Cmn.pop()
assert cmn == 'ore'
Uni = {}
for rob, Res in Unis.items():
    assert len(Res) == 1
    res = Res.pop()
    Uni[rob] = res
U = list(Uni.values())
assert all( U.count(res) == 1 for res in U )
# (i-d) Therefore, the second-highest priority resource is the unique resource 
# needed to produce the geode robot. The third-highest priority resource is the 
# resource needed to produce the robot that produces the second-highest 
# priority resource, etc. The lowest priority resource is the common resource.
P = [P0]
while P[-1] in Uni:
    P.append(Uni[P[-1]])
P.append(cmn)
# (ii) Only one robot should ever be built at once. This is because, if two
# robots are built simultaneously, there must be sufficient resources for two
# robots to be built. However, it is always less optimal to postpone making a
# particular robot if the resources for that robot are available.

# Having established the priority order [P0, P1, P2, ..., cmn], 
# we now define a State as a tuple of the form:
# ((number_of_resource_P0, number_of_robot_P0), (number_of_resource_P1,
# number_of_robot_P1), ..., (number_of_robot_cmn, number_of_resource_cmn))
# Use this idea to rebuild the Cost dictionary using numeric tuples only:
Move = defaultdict(list)
for (ix, rob), C in Cost.items():
    Move_Rob = tuple(1 if res == rob else 0 for res in P)
    Move_Res = [0 for res in P]
    for num, res in C:
        Move_Res[P.index(res)] = -num
    Move[ix].append( (tuple(Move_Res), Move_Rob) )
# We can also choose to produce no robots
for ix in IX:
    Move[ix].append( (tuple(0 for res in P), tuple(0 for res in P)) )

# construct the starting State, given in the problem
S = tuple( (0, 1) if res == cmn else (0, 0) for res in P )

# part 1
ans1 = 0
for ix in Move.keys():
    max_geode = get_max_geode(tuple(Move[ix]), S, 24)
    ans1 += ix * max_geode
print(ans1)

# part 2
ans2 = 1
for ix in Move.keys():
    if not 1 <= ix <= 3:
        continue
    max_geode = get_max_geode(Move[ix], S, 32)
    ans2 *= max_geode
print(ans2)

