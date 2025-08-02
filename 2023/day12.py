import sys
from copy import deepcopy
import functools

@functools.cache
def align_recursive(Conditions, Groups, match_group):
    """
    Recursively align groups to conditions.

    match_group: if True, we must consume Groups[0]. If False, we can either
        start work on Groups[0] or skip.
    """

    if len(Conditions) == 0:
        # we have matched all conditions
        if len(Groups) == 0 or ( len(Groups) == 1 and Groups[0] == 0 ):
            # all Groups have been consumed
            return 1
        else:
            # some Groups are incomplete
            return 0
    else:
        # we need to match the next condition
        if match_group and Groups[0] > 0:
            # we are currently consuming a group
            if Conditions[0] == '#' or Conditions[0] == '?':
                return align_recursive(\
                Conditions[1:], (Groups[0]-1, ) + Groups[1:], True)
            elif Conditions[0] == '.':
                return 0
            else:
                assert False
        elif match_group and Groups[0] == 0:
            # we need to complete a group
            if Conditions[0] == '?' or Conditions[0] == '.':
                return align_recursive(Conditions[1:], Groups[1:], False)
            elif Conditions[0] == '#':
                return 0
            else:
                assert False
        elif not match_group:
            # we can start a new group, or continue skipping undamaged
            if Conditions[0] == '#':
                if len(Groups) > 0:
                    return align_recursive(\
                    Conditions[1:], (Groups[0]-1, ) + Groups[1:], True)
                else:
                    return 0
            elif Conditions[0] == '.':
                return align_recursive(Conditions[1:], Groups, False)
            elif Conditions[0] == '?':
                if len(Groups) > 0:
                    # make the condition damaged
                    align_damaged = \
                    align_recursive(\
                    Conditions[1:], (Groups[0]-1, ) + Groups[1:], True)
                    # make the condition undamaged
                    align_undamaged = \
                    align_recursive(Conditions[1:], Groups, False)
                    # return the sum
                    return align_damaged + align_undamaged
                else:
                    return align_recursive(Conditions[1:], Groups, False)
            else:
                assert False
        else:
            assert False

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Con = []
Grp = []
for x in X:
    con, grp = x.split(' ')
    Con.append( tuple(con) )
    Grp.append( tuple(map(int, grp.split(','))) )

# part 1
ans1 = 0
for con, grp in zip(Con, Grp):
    num_aln = align_recursive(con, grp, False)
    ans1 += num_aln
print(ans1)

# part 2
ans2 = 0
for con, grp in zip(Con, Grp):
    con2 = deepcopy(con)
    grp2 = deepcopy(grp)
    for _ in range(4):
        con2 += ('?', )
        con2 += con
        grp2 += grp
    num_aln = align_recursive(con2, grp2, False)
    ans2 += num_aln
print(ans2)

