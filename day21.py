import sys
from copy import deepcopy
from collections import Counter

# the numeric keypad
KNUM = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']]
# the directional keypad
KDIR = [['', '^', 'A'], ['<', 'v', '>']]
# dictionary to convert directional keypad presses to directions
OPS = {'^':(-1,0), 'v':(1,0), '<':(0,-1), '>':(0,1), 'A':(0,0)}
# dictionary to convert directions to directional keypad presses
iOPS = {value:key for key,value in OPS.items()}

def seq2ops(seq):
    """
    Convert a keypad sequence to a dictionary of operations.
    """
    Ops = Counter()
    for i in range(len(seq)):
        if i==0:
            Ops[ ('A',seq[i]) ] += 1
        else:
            Ops[ (seq[i-1],seq[i]) ] += 1
    return Ops

def get_key_op(pad, start, end):
    """
    Get the key-presses required to journey on PAD from the START character
    to the END character and press it.
    """
    for r,row in enumerate(pad):
        for c,char in enumerate(row):
            if char == start:
                coord_start = (r,c)
            if char == end:
                coord_end = (r,c)
            if char == '':
                coord_blank = (r,c)
    # there are two shortest paths between points
    # (i) compute Manhattan distances in x and y
    dr = coord_end[0] - coord_start[0]
    dc = coord_end[1] - coord_start[1]
    # (ii) determine the key-press corresponding to the x and y directions
    keyr = iOPS[ ( dr//abs(dr) if dr!=0 else 0 , 0) ]
    keyc = iOPS[ (0 , dc//abs(dc) if dc!=0 else 0 ) ]
    # (iii) produce the key-press operations
    # row-then-column order
    Ops_rc = Counter()
    if abs(dr)>0:
        Ops_rc[ ('A',keyr) ] += 1
    if abs(dr)>1:
        Ops_rc[ (keyr,keyr) ] += abs(dr)-1
    if abs(dc)>0:
        Ops_rc[ (keyr,keyc) ] += 1
        Ops_rc[ (keyc,'A') ] += 1
    else:
        Ops_rc[ (keyr,'A') ] += 1
    if abs(dc)>1:
        Ops_rc[ (keyc,keyc) ] += abs(dc)-1
    # column-then-row order
    Ops_cr = Counter()
    if abs(dc)>0:
        Ops_cr[ ('A',keyc) ] += 1
    if abs(dc)>1:
        Ops_cr[ (keyc,keyc) ] += abs(dc)-1
    if abs(dr)>0:
        Ops_cr[ (keyc,keyr) ] += 1
        Ops_cr[ (keyr,'A') ] += 1
    else:
        Ops_cr[ (keyc,'A') ] += 1
    if abs(dr)>1:
        Ops_cr[ (keyr,keyr) ] += abs(dr)-1
    # (iv) determine the correct order of operations based on the blank square
    if coord_start[0]==coord_blank[0] and coord_end[1]==coord_blank[1]:
        return [ Ops_rc ]
    elif coord_start[1]==coord_blank[1] and coord_end[0]==coord_blank[0]:
        return [ Ops_cr ]
    elif dr==0 and dc==0:
        return [ Ops_rc ]
    elif dr!=0 and dc==0:
        return [ Ops_rc ]
    elif dr==0 and dc!=0:
        return [ Ops_cr ]
    else:
        return [ Ops_rc, Ops_cr ]

def get_key_collection(pad, Ops):
    Collect = [ Counter() ] # holds the possible key operations
    for op,n in Ops.items():
        # determine the key-presses required to produce the current operation
        start,end = op
        Key_Op = get_key_op(pad, start, end)
        # populate the collections
        Collect_New = []
        while Collect:
            for Ops_New in Key_Op:
                Ops_Running = deepcopy(Collect[-1])
                for op_new,n_new in Ops_New.items():
                    Ops_Running[op_new] += n*n_new
                Collect_New.append(Ops_Running)
            Collect.pop()
        Collect = Collect_New
    return Collect

def prune(Ops):
    shortest = min([sum(Op.values()) for Op in Ops])
    Out = []
    for Op in Ops:
        if sum(Op.values()) == shortest:
            Out.append(Op)
    return Out

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]

# part 1
ans1 = 0
ans2 = 0
ndir = 25
for seq in X:
    # convert the keypad sequence to operations
    Ops = seq2ops(seq)
    # convert the numberic operations to directional operations
    Ops = get_key_collection(KNUM, Ops)
    for i in range(ndir):
        Ops_Next = []
        for Op in Ops:
            Ops_Next += get_key_collection(KDIR, Op)
        Ops = Ops_Next
        Ops = prune(Ops)
        if i == 1 or i ==24:
            shortest = min([sum(Op.values()) for Op in Ops])
            if i == 1:
                ans1 += shortest * int(seq[:-1])
            else:
                ans2 += shortest * int(seq[:-1])
print(ans1)
print(ans2)

