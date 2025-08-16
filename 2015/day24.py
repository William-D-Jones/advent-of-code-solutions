import sys
import itertools
import math

def qe_smallest_group(X, num_groups):
    tot = sum(X) // num_groups
    Grp1 = []
    for n in range(1, len(X)-2):
        for grp1 in itertools.combinations(X, n):
            if sum(grp1) == tot:
                Grp1.append(grp1)
        if len(Grp1) > 0:
            break
    qe = min(math.prod(list(grp1)) for grp1 in Grp1)
    return qe

# parsing
X = sorted([ int(l.strip()) for l in open(sys.argv[1], 'r') ])

# Since we only care about one of the groups of presents, there is no need to 
# find the other 2-3 groups. Simply find the smallest number of presents that
# sums to the appropriate value.

# part 1
ans1 = qe_smallest_group(X, 3)
print(ans1)

# part 2
ans2 = qe_smallest_group(X, 4)
print(ans2)

