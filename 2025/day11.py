import sys
import functools

# parsing
X = [l.strip().split(': ') for l in open(sys.argv[1], 'r')]
CON = {x[0]: tuple(x[1].split(' ')) for x in X}

@functools.cache
def trace(pnt, target, Collect):
    if pnt == target and len(Collect) == 0:
        return 1
    elif pnt in CON:
        return sum( \
        trace(pnt_next, target, \
        tuple(item for item in Collect if item != pnt_next)) for \
        pnt_next in CON[pnt] \
        )
    else:
        return 0

# part 1
ans1 = trace('you', 'out', tuple())
print(ans1)

# part 2
ans2 = trace('svr', 'out', ('dac', 'fft'))
print(ans2)

