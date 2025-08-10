import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
ans1 = X.count('(') - X.count(')')
print(ans1)

# part 2
floor = 0
for i,char in enumerate(X):
    if char == '(':
        floor += 1
    elif char == ')':
        floor -= 1
    else:
        assert False
    if floor == -1:
        ans2 = i+1
        break
print(ans2)
    
