import sys

def get_x_ranges(S, y):
    Dist = {}
    Ex = {}
    for s in S.keys():
        b = S[s]
        # get the manhattan distance to each beacon
        dist = abs(b[1]-s[1]) + abs(b[0]-s[0])
        Dist[s] = dist
        # no other beacon can be within this manhattan distance
        # get the range of excluded x positions in the target row
        dx = dist-abs(y-s[1])
        if dx > 0:
            x1 = s[0] + dx
            x2 = s[0] - dx
            Ex[s] = tuple(sorted([x1,x2]))
    # merge overlapping excluded ranges
    Em = list(Ex.values())
    i = 0
    while i < len(Em):
        j = i+1
        while j < len(Em):
            emi = Em[i]
            emj = Em[j]
            if min(emi[1], emj[1]) - max(emi[0], emj[0]) >= -1:
                Em = Em[:i] + Em[i+1:j] + Em[j+1:]
                Em.append( (min(emi[0], emj[0]), max(emi[1], emj[1])) )
                i = -1
                break
            j += 1
        i += 1
    return Em

# parsing
X = [ l.strip().split() for l in open(sys.argv[1], 'r') ]
S = {}
for x in X:
    S[ ( int(x[2][2:-1]), int(x[3][2:-1]) ) ] = \
    ( int(x[8][2:-1]), int(x[9][2:]) )
B = set(S.values())

# part 1
y1 = 2000000
Em = get_x_ranges(S, y1)
# calculate the number of x-positions that cannot contain a beacon
ans1 = 0
for em in Em:
    ans1 += em[1]-em[0]+1
    for b in B:
        if em[0]<=b[0]<=em[1] and b[1]==y1:
            ans1 -= 1
print(ans1)

# part 2
cmin = 0
cmax = 4000000
R = (cmin, cmax)
for y in range(cmin, cmax+1):
    Em = get_x_ranges(S, y)
    for em in Em:
        if min(em[1], cmax) - max(em[0], cmin) < cmax-cmin:
            if em[0] >= R[0]:
                R = (R[0], em[0]-1)
            if em[1] <= R[1]:
                R = (em[1]+1, R[1])
            yb = y
assert R[0] == R[1]
ans2 = 4000000*R[0] + yb
print(ans2)

