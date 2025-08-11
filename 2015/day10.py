import sys
from copy import copy

def look_say(txt):
    i = 1
    out = ''
    same = txt[0:1]
    while i < len(txt):
        new = txt[i:i+1]
        if new == same[0:1]:
            same += new
        else:
            out += str(len(same))
            out += same[0:1]
            same = new
        if i == len(txt)-1:
            out += str(len(same))
            out += same[0:1]
        i += 1
    return out

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
txt = copy(X)
for _ in range(40):
    txt = look_say(txt)
ans1 = len(txt)
print(ans1)

# part 2
txt = copy(X)
for _ in range(50):
    txt = look_say(txt)
ans2 = len(txt)
print(ans2)

