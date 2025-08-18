import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Disc = []
for x in X:
    xs = x.split()
    Disc.append( (int(xs[1][1:]), int(xs[3]), int(xs[-1][:-1])) )

# part 1
# choose the time t so that for each disk k, (s+t+k)%p == 0
t = 0
while any( (t + disc[2] + disc[0]) % disc[1] != 0 for disc in Disc ):
    t += 1
ans1 = t
print(ans1)

# part 2
Disc.append( (max(disc[0] for disc in Disc)+1, 11, 0) )
t = 0
while any( (t + disc[2] + disc[0]) % disc[1] != 0 for disc in Disc ):
    t += 1
ans2 = t
print(ans2)

