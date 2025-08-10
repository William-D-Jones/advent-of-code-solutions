import copy

X = [ l for l in open('input-2022-5.txt', 'r') ]

# initial parsing
div = 0
for i in range(len(X)):
    if X[i] == '\n':
        div = i
        break
S = X[ 0 : div ]
C = X[ (div+1) : len(X) ]

# parse stacks
n = len(S[-1].split())
st = []
for i in range(n):
    st.append([])
for i in range(len(S) - 1):
    for j in range(n):
        p = S[i][ (j * 4 + 1) : (j * 4 + 2) ]
        if p != ' ' and p != '':
            st[j].append(p)
for i in range(len(st)):
    st[i] = list(reversed(st[i]))

# parse com
com = []
for c in C:
    lc = c.strip().split(' ')
    com.append([int(lc[1]), int(lc[3]), int(lc[5])])

st1 = copy.deepcopy(st)
st2 = copy.deepcopy(st)

# part 1: move blocks
for c in com:
    for i in range(c[0]):
       st1[c[2] - 1].append(st1[c[1] - 1].pop())
ans = []
for x in st1:
    ans.append(x[-1])
print(''.join(ans))

# part 2: move blocks, retaining order
for c in com:
    st2[c[2] - 1] += st2[c[1] - 1][-c[0] : ]
    st2[c[1] - 1] = (st2[c[1] - 1])[ : -c[0]]
ans = []
for x in st2:
    ans.append(x[-1])
print(''.join(ans))

