import sys
import re
from collections import deque
import itertools

def walk_valves(Con, Flow, use_elephant, max_step):
    # current valve, steps, open valves, pressure released
    Q = deque([('AA', 'AA', 0, tuple(), 0)])
    Seen = set([('AA', 'AA', 0, tuple(), 0)])
    max_pressure = 0
    while Q:
        v, vel, step, Open, pressure = Q.popleft()
        for v_next, vel_next in itertools.product(\
        [None] + Con[v], ['AA'] if not use_elephant else [None] + Con[vel]):
            # execute the movement or the valve opening for the elf
            if v_next is None:
                if Flow[v] > 0 and v not in Open:
                    v_next = v
                    Open_Next = tuple(sorted(list(Open)+[v]))
                    pressure_next = \
                    pressure + Flow[v] * (max_step-(step+1))
                else:
                    continue
            else:
                Open_Next = tuple(Open)
                pressure_next = pressure
            # execute the movement or the valve opening for the elephant
            if vel_next is None:
                if Flow[vel] > 0 and vel not in Open_Next:
                    vel_next = vel
                    Open_Next = tuple(sorted(list(Open_Next)+[vel]))
                    pressure_next = \
                    pressure_next + Flow[vel] * (max_step-(step+1))
                else:
                    continue
            else:
                Open_Next = tuple(Open_Next)
                pressure_next = pressure_next
            # setup the next state and check if it has been seen
            step_next = step+1
            if step_next >= max_step or len(Open_Next) >= len(Flow):
                if pressure_next > max_pressure:
                    max_pressure = pressure_next
                continue
            State_Next = (*sorted([v_next, vel_next]), \
            step_next, pressure_next)
            if State_Next in Seen:
                continue
            Seen.add(State_Next)
            Q.append( (v_next, vel_next, step_next, Open_Next, pressure_next) )
    return max_pressure

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Flow = {}
Con = {}
for x in X:
    M = re.match('^Valve ([A-Z]+) has flow rate=([0-9]+); ' + \
    'tunnels* leads* to valves* ([A-Z, ]+)$', x)
    v_id = M.group(1)
    v_flow = int(M.group(2))
    v_dest = M.group(3).split(', ')
    Flow[v_id] = v_flow
    Con[v_id] = v_dest

# part 1
ans1 = walk_valves(Con, Flow, False, 30)
print(ans1)

# part 2
ans2 = walk_valves(Con, Flow, True, 26)
print(max(ans1,ans2))

