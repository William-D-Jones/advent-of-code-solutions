import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Rein = {}
for x in X:
    xs = x.split(' ')
    name = xs[0]
    speed = int(xs[3])
    time = int(xs[6])
    rest = int(xs[13])
    Rein[name] = (speed, time, rest)

# part 1
t1 = 2503
Dist = []
for rein, (speed, time, rest) in Rein.items():
    cyc = t1 // (time+rest)
    rem = t1 % (time+rest)
    dist = cyc * time * speed
    if rem >= time:
        dist += speed * time
    else:
        dist += speed * rem
    Dist.append(dist)
ans1 = max(Dist)
print(ans1)

# part 2
t2 = 2503
Remaining = [val[1] for val in Rein.values()]
Dist = [0 for _ in range(len(Rein))]
Pts = [0 for _ in range(len(Rein))]
Rein_Val = list(Rein.values())
for t in range(t2):
    for i, (speed, time, rest) in enumerate(Rein_Val):
        if Remaining[i] > 0:
            Remaining[i] -= 1
            Dist[i] += speed
            if Remaining[i] == 0:
                Remaining[i] = -1 * rest
        elif Remaining[i] < 0:
            Remaining[i] += 1
            if Remaining[i] == 0:
                Remaining[i] = time
        else:
            assert False
    dmax = max(Dist)
    for i, dist in enumerate(Dist):
        if dist == dmax:
            Pts[i] += 1
ans2 = max(Pts)
print(ans2)

