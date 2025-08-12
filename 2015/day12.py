import sys
import json
from collections import deque

def sum_numbers(X):
    tot = 0
    s = ''
    for i in range(len(X)):
        char = X[i:i+1]
        if char in '1234567890':
            s += char
        elif char == '-':
            if len(s) > 0:
                num = int(s)
                tot += num
            s = '-'
        elif len(s) > 0:
            num = int(s)
            tot += num
            s = ''
    return tot

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
ans1 = sum_numbers(X)
print(ans1)
        
# part 2
ans2 = 0
J = json.loads(X)
Parse = deque([J])
while Parse:
    parse = Parse.popleft()
    if type(parse) is dict:
        if any(val == 'red' for val in parse.values()):
            continue
        else:
            for key, val in parse.items():
                Parse.append(key)
                Parse.append(val)
    elif type(parse) is list:
        for item in parse:
            Parse.append(item)
    elif type(parse) is str:
        continue
    elif type(parse) is int:
        ans2 += parse
    else:
        assert False
print(ans2)

