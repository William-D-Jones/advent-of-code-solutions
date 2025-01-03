import sys
import re

# parsing
X = open(sys.argv[1], 'r').read().strip()

ans1 = 0
ans2 = 0
re_mul = re.compile("^mul\(([0-9]{1,3}),([0-9]{1,3})\)")
re_do = re.compile("^do\(\)")
re_dont = re.compile("^don't\(\)")
ins = True
i = 0
len_max = len("mul(000,000)")
while i < len(X):
    match_do = re_do.search(X[i:i+len_max])
    match_dont = re_dont.search(X[i:i+len_max])
    if match_do is not None:
        ins = True
        i += len("do()") - 1
    elif match_dont is not None:
        ins = False
        i += len("don't()") - 1
    match_mul = re_mul.search(X[i:])
    if match_mul is not None:
        ans1 += int(match_mul[1]) * int(match_mul[2])
        ans2 += (int(match_mul[1]) * int(match_mul[2]) if ins else 0)
        i += len(match_mul[0]) - 1
    i += 1
print(ans1)
print(ans2)
