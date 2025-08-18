import sys

# parsing
X = int(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
Pres = {i: 1 for i in range(X)}
src = 0
while True:
    if Pres[src] == 0:
        src = (src+1)%X
        continue
    tar = (src+1)%X
    while Pres[tar] == 0:
        tar = (tar+1)%X
    load = Pres[src] + Pres[tar]
    Pres[src] = load
    Pres[tar] = 0
    if load == X:
        break
    src = (tar+1)%X
ans1 = src+1
print(ans1)

# part 2
Pres = {i: 1 for i in range(X)}
src = 0
tar = src + X // 2
nz = X
while True:
    if Pres[src] == 0:
        src = (src+1)%X
        continue
    load = Pres[src] + Pres[tar]
    Pres[src] = load
    Pres[tar] = 0
    if load == X:
        break
    src = (src+1)%X
    if nz % 2 == 0:
        jump = 1
    else:
        jump = 2
    while jump > 0:
        tar = (tar+1)%X
        if Pres[tar] != 0:
            jump -= 1
    nz -= 1
ans2 = src+1
print(ans2)

