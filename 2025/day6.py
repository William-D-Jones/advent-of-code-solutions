import sys
import math

# parsing
# parse without removing spaces between numbers
X = list(map(list, open(sys.argv[1], 'r').read().strip().split('\n')))
nrow = len(X)
ncol = len(X[0])
assert all(len(row)==ncol for row in X[:-1])
# remove spaces between numbers
S = [''.join(x).split() for x in X]
nnum = len(S[0])
assert all(len(row)==nnum for row in S)

# part 1
ans1 = 0
for c in range(nnum):
    if S[-1][c] == '+':
        ans1 += sum(int(S[r][c]) for r in range(nrow-1))
    elif S[-1][c] == '*':
        ans1 += math.prod(int(S[r][c]) for r in range(nrow-1))
    else:
        assert False
print(ans1)

# part 2
ans2 = 0
c = 0
Num = []
while c < ncol:
    # establish a new operator if available
    if c < len(X[-1]) and X[-1][c] != ' ':
        op = X[-1][c]
    # consume a new operand
    s = ''.join(X[r][c] for r in range(nrow-1))
    Num.append( int(s.strip()) )
    # check if the operation should be completed
    if c+1 == ncol or all(X[r][c+1] == ' ' for r in range(nrow-1)):
        if op == '+':
            ans2 += sum(Num)
        elif op == '*':
            ans2 += math.prod(Num)
        else:
            assert False
        c += 1
        Num = []
    c += 1
print(ans2)

