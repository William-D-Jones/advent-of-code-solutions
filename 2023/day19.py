import sys
from copy import deepcopy
from collections import deque

def check_part(Part, Workflow, start = 'in'):
    for rule in Workflow[start]:
        if len(rule) == 1:
            out = rule[0]
            break
        else:
            name, op, rating, target = rule
            if op == '<' and Part[name] < rating or \
            op == '>' and Part[name] > rating:
                out = target
                break
    if out == 'R' or out == 'A':
        return out
    else:
        return check_part(Part, Workflow, start = out)
    
# parsing
XW,XP = ('\n'.join([ l.strip() for l in open(sys.argv[1], 'r') ])).split('\n\n')
Flow = {}
for l in XW.split('\n'):
    name, flow = l[:-1].split('{')
    Rule = []
    for x in flow.split(','):
        rule = x.split(':')
        assert 0<len(rule)<=2
        if len(rule) == 2:
            Rule.append( \
            (rule[0][:1], rule[0][1:2], int(rule[0][2:]), rule[1]) )
        else:
            Rule.append( (rule[0], ) )
    Flow[name] = Rule
Parts = [] 
for l in XP.split('\n'):
    part = {}
    for x in l[1:-1].split(','):
        name, rating = x.split('=')
        part[name] = int(rating)
    Parts.append(part)

# part 1
ans1 = 0
for part in Parts:
    if check_part(part, Flow) == 'A':
        ans1 += sum(part.values())
print(ans1)

# part 2
XMAS = deque([ {'x': (1,4001), 'm': (1,4001), 'a': (1,4001), 's': (1,4001) } ])
Point = deque(['in'])
A = []
R = []
while XMAS:
    xmas = XMAS.pop()
    point = Point.pop()
    for rule in Flow[point]:
        # apply the rule and construct a new range
        if len(rule) == 1:
            name = 'x'
            range_pass = xmas[name]
            range_fail = (0, 0)
            target = rule[0]
        else:
            name, op, rating, target = rule
            if op == '<':
                range_pass = ( xmas[name][0], min(xmas[name][1], rating) )
                range_fail = ( max(xmas[name][0], rating), xmas[name][1] )
            elif op == '>':
                range_pass = ( max(xmas[name][0], rating + 1), xmas[name][1] )
                range_fail = ( xmas[name][0], min(xmas[name][1], rating + 1) )
            else:
                assert False
        # construct a new xmas object and store it
        if range_pass[1] - range_pass[0] > 0:
            if target == 'R':
                xmas[name] = range_pass
                R.append(deepcopy(xmas))
            elif target == 'A':
                xmas[name] = range_pass
                A.append(deepcopy(xmas))
            else:
                xmas[name] = range_pass
                XMAS.appendleft(deepcopy(xmas))
                Point.appendleft(target)
        if range_fail[1] - range_fail[0] > 0:
            xmas[name] = range_fail
        else:
            break
ans2 = 0
for xmas in A:
    num_A = 1
    for range_pass in xmas.values():
        num_A *= (range_pass[1] - range_pass[0])
    ans2 += num_A
print(ans2)
    
