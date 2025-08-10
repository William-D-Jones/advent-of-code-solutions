X = [ l.strip() for l in open('input-2022-3.txt', 'r') ]

sl = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
pl = range(1, 53)
dl = { sl[i] : pl[i] for i in range(0, 52) }

P = []
for b in X:
    found = False
    div = len(b) // 2
    B = []
    B.append(b[0:div])
    B.append(b[div:len(b)])
    
    for i in range(div):
        for j in range(div):
            if B[0][i] == B[1][j]:
                P.append(dl[B[0][i]])
                found = True
                break
        if found:
            break

print(sum(P))

P = []
n = len(X) // 3
X3 = [' '.join(X[i*3:i*3+3]) for i in range(n)]
for b in X3:
    found = False
    B = b.split(' ')
    for i in range(len(B[0])):
        for j in range(len(B[1])):
            for k in range(len(B[2])):
                if B[0][i] == B[1][j] and B[0][i] == B[2][k]:
                    P.append(dl[B[0][i]])
                    found = True
                    break
            if found:
                break
        if found:
            break

print(sum(P))

