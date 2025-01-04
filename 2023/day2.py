import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

G = []
d = {'red': 0, 'green': 0, 'blue': 0}
for x in X:
    G.append(d.copy())
    W = x.split()
    Res = ' '.join(W[2:]).split('; ')
    for res in Res:
        X = res.split(', ')
        for x in X:
            m = x.split(' ')
            if int(m[0]) > G[-1][m[1]]:
                G[-1][m[1]] = int(m[0])
ans = 0
power = 0
for i,g in enumerate(G):
    if g['red'] <= 12 and g['green'] <= 13 and g['blue'] <= 14:
        ans += i + 1
    power += g['red'] * g['green'] * g['blue']
print(ans)
print(power)

