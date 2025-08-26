import sys

# parsing
X = list(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# parts 1 and 2
is_gar = False
score = 0
ans1 = 0
ans2 = 0
i = 0
while i < len(X):
    char = X[i]
    if char == '!':
        i += 2
        continue
    if char == '<' and not is_gar:
        is_gar = True
    elif char == '>' and is_gar:
        is_gar = False
    elif is_gar:
        ans2 += 1
    elif char == '{':
        score += 1
    elif char == '}':
        ans1 += score
        score -= 1
    i += 1
print(ans1)
print(ans2)
        
