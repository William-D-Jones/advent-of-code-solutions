import sys
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Gen = {}
for x in X:
    M = re.match('^Generator ([A-Z]+) starts with ([0-9]+)$', x)
    Gen[ M.group(1) ] = int(M.group(2))

# part 1
fa = 16807
fb = 48271
d = 2147483647
A = Gen['A']
B = Gen['B']
ans1 = 0
n = 40000000
for i in range(n):
    A = A * fa % d
    B = B * fb % d
    if A % 2**16 == B % 2**16:
        ans1 += 1
print(ans1)
    
# part 2
fa = 16807
fb = 48271
d = 2147483647
A = Gen['A']
B = Gen['B']
ans2 = 0
n = 5000000
for i in range(n):
    A = A * fa % d
    while A % 4 != 0:
        A = A * fa % d
    B = B * fb % d
    while B % 8 != 0:
        B = B * fb % d
    if A % 2**16 == B % 2**16:
        ans2 += 1
print(ans2)

