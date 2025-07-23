import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

r = '0123456789'
R = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
dR = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8, 
    'nine': 9 }

N = []
for m, x in enumerate(X):
    N.append('')
    for i in range(len(x)):
        if x[i : i + 1] in r:
            N[m] = ''.join([N[m], x[i : i + 1]])
    N[m] = int(''.join([N[m][0], N[m][-1]]))
print(sum(N))

N = []
for m, x in enumerate(X):
    N.append('')
    for i in range(len(x)):
        if x[i : i + 1] in r:
            N[m] = ''.join([N[m], x[i : i + 1]])
        else:
            for w in R:
                if x[i : i + len(w)] == w:
                    N[m] = ''.join([N[m], str(dR[w])])       
    N[m] = int(''.join([N[m][0], N[m][-1]]))
print(sum(N))

