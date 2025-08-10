X = [ l.strip() for l in open('input-2022-1.txt', 'r') ]

X_weight = ('\n'.join(X)).split('\n\n')

W = []
for p in X_weight:
    w = 0
    for q in p.split('\n'):
        w += int(q)
    W.append(w)

Ws = sorted(W, reverse = True)
print(Ws[0])
print(sum(Ws[0:3]))

