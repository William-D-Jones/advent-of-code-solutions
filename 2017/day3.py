import sys

D = [ (0,1), (-1,0), (0,-1), (1,0) ]

# parsing
X = int(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1

# If the ith square has k elements on one of its sides, the (i+1)th square has
# k+2. The number of elements in a square with k elements on its side is 
# 2k+2(k-2)=2k+2k-4=4k-4=4(k-1).
k = 1 # the number of elements on a side of a square
n = 1 # the total number of elements consumed so far
while True:
    k_next = k+2 # the next number of elements on a side
    n_next = 4*(k_next-1) # the number of elements in the next square
    if n + n_next <= X:
        k = k_next
        n += n_next
    else:
        break
# how many elements remain to be consumed after completing this many squares
n_rem = X-n
# find the number of elements on a side of the current square
if n_rem > 0:
    k = k_next
# how many elements remain after consuming full sides
n_side = n_rem % (k-1) if k-1>0 else 0
# compute the Manhattan distance
ans1 = k // 2 + abs(k // 2 - n_side)
print(ans1)

# part 2

val = 1
Pos = (0,0)
Num = {Pos: val}
dx = 0
while val <= X:
    r,c = Pos
    dr,dc = D[dx]
    r += dr
    c += dc
    if not (min(pos[0] for pos in Num.keys()) <= r <= \
    max(pos[0] for pos in Num.keys())) or not \
    (min(pos[1] for pos in Num.keys()) <= c <= \
    max(pos[1] for pos in Num.keys())):
        dx = (dx+1)%len(D)
    Pos = (r,c)
    val = 0
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr == 0 and dc == 0:
                continue
            nr = r+dr
            nc = c+dc
            if (nr,nc) in Num.keys():
                val += Num[(nr,nc)]
    Num[(r,c)] = val
ans2 = val
print(ans2)

