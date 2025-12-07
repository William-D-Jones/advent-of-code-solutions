import sys
import re

def play(nm):
    C = {0: (0,0)} # each marble id returns (previous_marble,next_marble)
    Score = [0] * np
    pl = 0 # the current player
    pnt = 0 # the pointer, set to the current marble at the end of each iteration
    m = 1 # the new marble
    while m <= nm:
        if m % 23 != 0:
            # find the marble counterclockwise from which m should be inserted
            for _ in range(2):
                pnt = C[pnt][1]
            # update the marble counterclockwise from m
            C[C[pnt][0]] = (C[C[pnt][0]][0], m)
            # add the new marble m
            C[m] = (C[pnt][0], pnt)
            # update the marble clockwise from m
            C[pnt] = (m, C[pnt][1])
            # update the current marble
            pnt = m
        else:
            # the current player receives this marble
            Score[pl] += m
            # find the marble which should be removed
            for _ in range(7):
                pnt = C[pnt][0]
            # the current player receives the marble that was removed
            Score[pl] += pnt
            # remove the marble and update the current marble
            C[ C[pnt][0] ] = (C[ C[pnt][0] ][0], C[pnt][1])
            C[ C[pnt][1] ] = (C[pnt][0], C[ C[pnt][1] ][1])
            nxt = C[pnt][1]
            C[pnt] = (None, None)
            pnt = nxt
        pl = (pl + 1) % np
        m += 1
    return max(Score)

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])
M = re.match('^([0-9]+) players; last marble is worth ([0-9]+) points', X)
np, nm = int(M.group(1)), int(M.group(2))

# part 1
ans1 = play(nm)
print(ans1)

# part 2
ans2 = play(nm * 100)
print(ans2)

