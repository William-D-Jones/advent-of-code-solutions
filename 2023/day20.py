import sys
import math
from copy import copy
from collections import defaultdict, deque

def mod_pulse(pulse, source, mod):
    mod_type, state, Dest = mod
    if mod_type == '%':
        if pulse == 1:
            out = None
        elif pulse == 0:
            if state == 0:
                state = 1
                out = 1
            elif state == 1:
                state = 0
                out = 0
            else:
                assert False
        else:
            assert False
    elif mod_type == '&':
        state[source] = pulse
        if all(value == 1 for value in state.values()):
            out = 0
        else:
            out = 1
    elif mod_type == 'broadcaster':
        out = pulse
    else:
        assert False
    mod = (mod_type, state, Dest)
    return out, mod

def push_button(Pulse, Source, Dest, L, H, Mod):
    Low = []
    High = []
    while Dest:
        pulse = Pulse.popleft()
        source = Source.popleft()
        dest = Dest.popleft()
        if dest in Mod.keys():
            pulse_out, mod_out = mod_pulse(pulse, source, Mod[dest])
            Mod[dest] = mod_out
            if pulse_out is not None:
                for _ in range(len(mod_out[2])):
                    Pulse.append(pulse_out)
                    Source.append(dest)
                    if pulse_out == 0:
                        L += 1
                        Low.append(source)
                    elif pulse_out == 1:
                        H += 1
                        High.append(source)
                    else:
                        assert False
                Dest += mod_out[2]
    return L, H, Mod, Low, High

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Mod = {}
Inputs = defaultdict(list)
for x in X:
    str_name, str_dest = x.split(' -> ')
    if str_name[0:1] == '%' or str_name[0:1] == '&':
        mod_name = str_name[1:]
        mod_type = str_name[0:1]
    else:
        mod_name = str_name
        mod_type = 'broadcaster'
    if mod_type == '%':
        state = 0
    elif mod_type == '&':
        state = {}
    elif mod_type == 'broadcaster':
        state = None
    else:
        assert False
    Dest = deque(str_dest.split(', '))
    for dest in Dest:
        Inputs[dest].append(mod_name)
    Mod[mod_name] = (mod_type, state, Dest)
for mod_name, mod in Mod.items():
    if mod[0] == '&':
        for input_name in Inputs[mod_name]:
            mod[1][input_name] = 0

# I examined the input manually and made the following observations, which
# I will take as assumptions for this input:
# (1) Exactly one & module feeds to rx.
#      (1a) Therefore, all memories into the & module must be high pulses.
# (2) Exactly 4 & modules feed to the & module described in (1).
#      (2a) Therefore, all memories into these & modules must be low pulses.
# (3) Into each of these 4 & modules feeds exactly one & module.
#      (3a) Therefore, all memories into these & modules must be high pulses.
# (4) Into each of these 4 & module feeds a collection of % modules.
#      (4a) Therefore, all these % modules must send high pulses.
#      (4b) Therefore, all these % modules must be in the off state and receive
#           a low pulse.
# (5) The % modules appear to regularly cycle between the on/off states.

# First step through the & modules upstream of rx, identifying the 4 & modules
# upstream of the final & module that feeds into rx.
Mod_rx_input = deque(['rx'])
Mod_rx_upstream = set()
while Mod_rx_input:
    upstream_name = Mod_rx_input.popleft()
    for mod_name, mod in Mod.items():
        if upstream_name in mod[2]:
            if mod[0] == '%':
                Mod_rx_upstream.add(upstream_name)
            elif mod[0] == '&':
                Mod_rx_input.append(mod_name)
# All the modules in Mod_rx_upstream need to send a high pulse.

# run simulations, collecting data for parts 1 and 2
L = 0
H = 0
Cycles = defaultdict(int)
nsim = 10 ** 4
n1 = 1000
for i in range(nsim):
    # count the low and high pulses for part 1
    L, H, Mod, Low, High = \
    push_button(deque([0]), deque(['button']), deque(['broadcaster']), \
    L + 1, H, Mod)
    # examine the % modules to identify cyclic behavior
    for upstream_name in Mod_rx_upstream:
        if upstream_name in High:
            if Cycles[upstream_name] == 0:
                Cycles[upstream_name] = i + 1
    if i == n1 - 1:
        L1 = copy(L)
        H1 = copy(H)

# part 1
ans1 = L1 * H1
print(ans1)

# part 2
LCM = []
for upstream_name in Mod_rx_upstream:
    assert Cycles[upstream_name] > 0
    LCM.append(Cycles[upstream_name])
ans2 = math.lcm(*LCM)
print(ans2)

