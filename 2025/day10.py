import sys
from collections import deque
import math
import numpy as np
import sympy as sy
import itertools

def min_ind(Target, Buttons):
    Q = deque([ (0, tuple(0 for _ in Target)) ])
    Seen = { (tuple(0 for _ in Target)) }
    min_step = None
    while Q:
        step, State = Q.popleft()
        # check if we have finished the search
        if State == Target:
            if min_step is None or step < min_step:
                min_step = step
            continue
        step_next = step + 1
        for button in Buttons:
            # generate the next indicator state
            State_Next = list(State)
            for ind in button:
                State_Next[ind] = (State_Next[ind] + 1) % 2
            State_Next = tuple(State_Next)
            # check if this indicator state has been seen
            if State_Next in Seen:
                continue
            Seen.add(State_Next)
            # continue the search
            Q.append( (step_next, State_Next) )
    return min_step

def min_cnt(Target, Buttons):
    # identify the buttons operating on each counter
    Op = [tuple(j for j,button in enumerate(Buttons) if i in button) for \
    i in range(len(Target))]
    # identify any redundant counters
    M = sy.Matrix([[1 if i in button else 0 for button in Buttons] \
    for i in range(len(Target))])
    RRT, ix_piv = M.T.rref()
    if len(Buttons) == len(ix_piv):
        # solve the system of linear equations directly
        A = np.array([[1 if i in button else 0 for button in Buttons] \
        for i in range(len(Target)) if i in ix_piv])
        B = np.array([cnt for i,cnt in enumerate(Target) if i in ix_piv])
        S = np.linalg.solve(A, B)
        return int(np.sum(S))
    else:

        # determine the number of buttons that must be guessed
        n_guess = len(Buttons)-len(ix_piv)
        State = list(Target)
        # determine the range of counts for each button
        Rng = [[0, sum(State)] for button in Buttons]
        # determine the maximum number of presses for each button
        for i,button in enumerate(Buttons):
            Rng[i][1] = min(State[ix] for ix in button)
        # determine the minimum number of presses for each button
        for ix in range(len(State)):
            n_button = sum(1 for button in Buttons if ix in button)
            if n_button == 1:
                ix_button = \
                [i for i,button in enumerate(Buttons) if ix in button]
                assert len(ix_button)==1
                ix_button = ix_button.pop()
                Rng[ix_button][0] = State[ix]

        # identify which buttons to guess
        Rng_Combo = []
        for combo in itertools.combinations(list(range(len(Buttons))), n_guess):
            MC = [[1 if i in button else 0 for button in Buttons] \
            for i in range(len(Target)) if i in ix_piv]
            for ix_button in combo:
                MC.append( 
                [1 if i==ix_button else 0 for i in range(len(Buttons))] 
                )
            RRC, ix_piv_c = sy.Matrix(MC).T.rref()
            if len(ix_piv_c) == len(Buttons):
                rng_tot = \
                math.prod(\
                rng[1]-rng[0]+1 for i,rng in enumerate(Rng) if i in combo)
                Rng_Combo.append( (rng_tot, combo) )
        Rng_Combo = sorted(Rng_Combo)

        # guess buttons
        min_step = None
        ix_pick = Rng_Combo[0][1]
        Rng_Guess = [range(rng[0], rng[1]+1) for \
        i,rng in enumerate(Rng) if i in ix_pick]
        for Guess in itertools.product(*Rng_Guess):
            # prepare and solve the system of linear equations directly
            A = [[1 if i in button else 0 for button in Buttons] \
            for i in range(len(Target)) if i in ix_piv]
            B = [cnt for i,cnt in enumerate(Target) if i in ix_piv]
            for ix_guess in range(n_guess):
                ix_button = ix_pick[ix_guess]
                A.append( \
                [1 if i==ix_button else 0 for i in range(len(Buttons))] 
                )
                B.append( Guess[ix_guess] )
            # get the solution, rounding to integers if needed
            S = np.linalg.solve(np.array(A), np.array(B))
            S = np.round(S).astype(int)
            # check if the output is correct
            if np.array_equal( np.dot(A, S), B ) and np.all(S>=0):
                step = sum(S)
                if min_step is None or min_step > step:
                    min_step = step
        return min_step

# parsing
STATE = {'.': 0, '#': 1}
X = [l.strip().split(' ') for l in open(sys.argv[1], 'r')]
Ind = []
But = []
Jol = []
for x in X:
    But.append( [] )
    for item in x:
        if item[0] == '[' and item[-1] == ']':
            Ind.append( tuple(STATE[char] for char in list(item[1:-1])) )
        elif item[0] == '(' and item[-1] == ')':
            But[-1].append( tuple(map(int,item[1:-1].split(','))) )
        elif item[0] == '{' and item[-1] == '}':
            Jol.append( tuple(map(int,item[1:-1].split(','))) )
        else:
            assert False

# part 1
ans1 = 0
for ind,but in zip(Ind,But):
    min_step = min_ind(ind, but)
    ans1 += min_step
print(ans1)

# part 2
ans2 = 0
for i,(jol,but) in enumerate(zip(Jol,But)):
    min_step = min_cnt(jol, but)
    ans2 += min_step
print(ans2)

