import sys

D = { '>': (0,1), '<': (0,-1) }

ROCK = """\
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##\
"""
RX = [RS.strip().split('\n') for RS in ROCK.strip().split('\n\n')]
dRock = {}
for i, rx in enumerate(RX):
    dRock[i] = set()
    nrow = len(rx)
    ncol = len(rx[0])
    dRock[i] = set([(r,c) for r in range(nrow) for c in range(ncol) if \
    rx[r][c] == '#'])

def make_rock(start_left, start_bottom, rock_type, dRock):
    Rock = set()
    rmax = max(r for r,c in dRock[rock_type])
    cmin = min(c for r,c in dRock[rock_type])
    Rock = set([ (start_bottom+(r-rmax), start_left+(c-cmin)) for \
    r,c in dRock[rock_type]])
    return Rock

# parsing
X = list(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
Room = set()
width = 7
rock_type = 0
jet = 0
last_height = 0
Hist = []
for i in range(2022):
    # make a new rock
    Rock = make_rock(2, min(r for r,c in Room)-4 if Room else -4, \
    rock_type, dRock)
    while True:
        x = X[jet]
        # jet the rock
        Rock_Next = set()
        for r,c in Rock:
            dr,dc = D[x]
            r,c = r+dr,c+dc
            if r<0 and 0<=c<width and (r,c) not in Room:
                Rock_Next.add( (r,c) )
            else:
                break
        if len(Rock_Next) == len(Rock):
            Rock = Rock_Next
        jet = (jet+1) % len(X)
        # drop the rock
        Rock_Next = set()
        for r,c in Rock:
            dr,dc = 1,0
            r,c = r+dr,c+dc
            if r<0 and 0<=c<width and (r,c) not in Room:
                Rock_Next.add( (r,c) )
            else:
                break
        if len(Rock_Next) != len(Rock):
            Room |= Rock
            break
        Rock = Rock_Next
    # record which rock was added and how much the tower increased
    next_height = abs(min(r for r,c in Room))
    hist_next = (rock_type, jet, next_height-last_height)
    Hist.append(hist_next)
    last_height = next_height
    # switch the rock_type for the next rock
    rock_type = (rock_type+1) % len(dRock)
ans1 = abs(min(r for r,c in Room))
print(ans1)

# part 2
# use the history list to try to find a pattern:
Rep = []
for i in range(len(Hist)):
    histi = Hist[i]
    try:
        j = Hist[i+1:].index(histi) + i+1
        if len(Rep) == 0 or Rep[-1][1] == j-1:
            Rep.append( (i,j) )
        else:
            Rep = [ (i,j) ]
    except:
        pass
# use the pattern to extrapolate the height of the tower
i_rep = Rep[0][0]
len_rep = Rep[0][1]-Rep[0][0]
h_start = sum(Hist[i][2] for i in range(0, i_rep))
h_rep = sum(Hist[i][2] for i in range(i_rep, i_rep+len_rep))
n_rep = (1000000000000 - i_rep) // len_rep
n_rem = (1000000000000 - i_rep) % len_rep
h_rem = sum(Hist[i][2] for i in range(i_rep, i_rep+n_rem))
ans2 = h_start + h_rep * n_rep + h_rem
print(ans2)

