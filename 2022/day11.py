import sys
import re
import math
from copy import deepcopy

def count_insp(Mon, n, p2):
    Insp = {i: 0 for i in range(num_mon)}
    for _ in range(n):
        for mon_id in range(num_mon):
            held, mon_worry, mon_fun = Mon[mon_id]
            while held:
                Insp[mon_id] += 1
                if p2:
                    item = mon_worry(held.pop(0)) % math.lcm(*Div)
                else:
                    item = mon_worry(held.pop(0)) // 3
                mon_tar = mon_fun(item)
                Mon[mon_tar][0].append(item)
    return Insp

# parsing
X = ('\n'.join([ l.strip() for l in open(sys.argv[1], 'r') ])).split('\n\n')
Mon = {}
Div = []
for x in X:
    xs = x.split('\n')
    # extract the monkey id
    mon_id = int(re.match('^Monkey ([0-9]+):$', xs[0]).group(1))
    # extract the starting items
    mon_start = list(map(int, \
    re.match('^Starting items: (.+)$', xs[1]).group(1).split(', ')\
    ))
    # extract the operation
    match_op = re.match('^Operation: new = old (.) (old|[0-9]+)$', xs[2])
    # extract the test
    mon_div = int(re.match('^Test: divisible by ([0-9]+)$', xs[3]).group(1))
    # extract the output
    mon_true = \
    int(re.match('If true: throw to monkey ([0-9]+)', xs[4]).group(1))
    mon_false = \
    int(re.match('If false: throw to monkey ([0-9]+)', xs[5]).group(1))
    # construct the worry lambda function
    if match_op.group(1) == '+' and match_op.group(2) != 'old':
        mon_worry = lambda old, op=int(match_op.group(2)): old + op 
    elif match_op.group(1) == '*' and match_op.group(2) != 'old':
        mon_worry = lambda old, op=int(match_op.group(2)): old * op
    elif match_op.group(1) == '+' and match_op.group(2) == 'old':
        mon_worry = lambda old: old + old
    elif match_op.group(1) == '*' and match_op.group(2) == 'old':
        mon_worry = lambda old: old * old
    else:
        assert False
    # construct the throwing lambda function
    mon_fun = lambda worry, mon_div = mon_div, mon_true = mon_true, \
    mon_false = mon_false: \
    mon_true if worry % mon_div == 0 else mon_false
    # setup the monkey
    Mon[mon_id] = [mon_start, mon_worry, mon_fun]
    Div.append(mon_div)
num_mon = len(Mon.keys())

# part 1
Insp = count_insp(deepcopy(Mon), 20, False)
ans1 = math.prod(sorted(Insp.values())[-2:])
print(ans1)

# part 2
Insp = count_insp(deepcopy(Mon), 10000, True)
ans2 = math.prod(sorted(Insp.values())[-2:])
print(ans2)

