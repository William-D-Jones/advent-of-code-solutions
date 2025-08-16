import sys
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]
match = re.match('.+ row ([0-9]+), column ([0-9]+)\\.', X)
r = int(match.group(1))
c = int(match.group(2))

# part 1

# first, find the index of the code at position (r,c)
# find the index of the diagonal that position (r,c) is on
#r = 1
#c = 4
ix_diag = r + (c-1)
# in general, the kth diagonal contains k codes
# therefore, the index of the code at position (r,c) is:
ix_code = (ix_diag-1) * ix_diag // 2 + c

# find the code
code = 20151125
for i in range(2, ix_code + 1):
    code = code * 252533 % 33554393
ans1 = code
print(ans1)

