import sys
import itertools

# parsing
X = int(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# find the power of each coordinate
nrow = 300
ncol = 300
F = [ [0 for c in range(ncol)] for r in range(nrow) ]
for r in range(nrow):
    for c in range(ncol):
        i = (c+1) + 10
        pwr = ( i*(r+1) + X ) * i
        pwr = ( (pwr%1000) - (pwr%100) ) // 100
        pwr -= 5
        F[r][c] = pwr

# part 1
max_pwr = None
for r in range(nrow-2):
    for c in range(ncol-2):
        pwr = sum([ F[rr][cc] for rr in range(r,r+3) for \
        cc in range(c,c+3) ])
        if max_pwr is None or pwr > max_pwr:
            max_pwr = pwr
            max_pwr_x = c+1
            max_pwr_y = r+1
ans1 = ','.join(map(str, [max_pwr_x,max_pwr_y]))
print(ans1)

# part 2
max_pwr = None
for r in range(nrow):
    for c in range(ncol):
        pwr = 0
        for sz in range(1, min(nrow-r,ncol-c)+1):
            pwr += sum(F[r+sz-1][c:c+sz])
            pwr += sum(F[rr][c+sz-1] for rr in range(r,r+sz))
            pwr -= F[r+sz-1][c+sz-1]
            if max_pwr is None or pwr > max_pwr:
                max_pwr = pwr
                max_pwr_x = c+1
                max_pwr_y = r+1
                max_pwr_sz = sz
            #print(sz, pwr)
ans2 = ','.join(map(str, [max_pwr_x,max_pwr_y,max_pwr_sz]))
print(ans2)

