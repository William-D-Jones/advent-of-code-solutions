X = [ l.strip() for l in open('input-2022-4.txt', 'r') ]

A = []
for x in X:
    a = []
    R = ('-'.join(x.split(','))).split('-')
    for r in R:
        a.append(int(r))
    A.append(a)

x = 0
for a in A:
    if (a[2] >= a[0] and a[3] <= a[1]) or (a[0] >= a[2] and a[1] <= a[3]):
        x += 1
print(x)

x = 0
for a in A:
    r1 = range(a[0], a[1] + 1)
    r2 = range(a[2], a[3] + 1)
    for e in r1:
        if e in r2:
            x += 1
            break
print(x)
    
