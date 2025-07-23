import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ]
N = [] # number, row, beginning, end
digits = '0123456789'
stnum = ''
for i,x in enumerate(X):
    for j,c in enumerate(x):
        if c in digits:
            stnum = ''.join([stnum, c])
        if not(c in digits) or j == len(x) - 1:
            if (c in digits) and j == len(x) - 1:
                end = j + 1
            else:
                end = j
            if stnum != '':
                N.append([int(stnum), i, j - len(stnum), end])
            stnum = ''
part = []
ans = 0
# find numbers touching characters
for n in N:
    stchar = ''
    left = max([0, n[2] - 1])
    right = min([n[3], len(X[0]) - 1]) + 1
    # get characters from line above
    if n[1] > 0:
        stchar = ''.join([stchar, X[n[1] - 1][left:right]])
        top = n[1] - 1
    else:
        top = n[1]
    # get characters from line below
    if n[1] < len(X) - 1:
        stchar = ''.join([stchar, X[n[1] + 1][left:right]])
        bottom = n[1] + 1
    else:
        bottom = n[1]
    # get character from left and right
    stchar = ''.join([stchar, X[n[1]][left:right]])
    for c in stchar:
        if not (c in digits) and c != '.':
            part.append(n + [top, bottom, left, right])
            ans += n[0]
print(ans)

# find candidate gears
G = []
for i,x in enumerate(X):
    for j,c in enumerate(x):
        if c == "*":
            G.append(["*", i, j, j + 1])
ans = 0
for g in G:
    npart = 0
    P = []
    for p in part:
        if p[4] <= g[1] <= p[5] and p[6] <= g[2] <= p[7] - 1:
            npart += 1
            P.append(p[0])
    if npart == 2:
        ans += P[0] * P[1]

print(ans)
