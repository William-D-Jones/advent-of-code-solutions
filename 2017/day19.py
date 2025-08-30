import sys

D = { (1,0): '|', (0,-1): '-', (-1,0): '|', (0,1): '-' }
A = ord('A')
Z = ord('Z')

# parsing
X = [ list(l) for l in open(sys.argv[1], 'r') ]
nrow = len(X)
ncol = len(X[0])

# parts 1 and 2
x = '|'
r = 0
c = X[0].index(x)
dr,dc = (1,0)
Path = []
nstep = 1
while x != ' ':
    # get the next coordinate
    r_next = r+dr
    c_next = c+dc
    #print(r_next,c_next,nstep)
    x_next = X[r_next][c_next]
    # get the next direction
    if x_next == '+':
        for dr_next,dc_next in D.keys():
            if 0<=r_next+dr_next<nrow and 0<=c_next+dc_next<ncol and \
            not (dr_next,dc_next) == (-dr,-dc) and \
            (X[r_next+dr_next][c_next+dc_next] == D[(dr_next,dc_next)] or \
            A<=ord(X[r_next+dr_next][c_next+dc_next])<=Z):
                r_next += dr_next
                c_next += dc_next
                x_next = X[r_next][c_next]
                dr = dr_next
                dc = dc_next
                nstep += 1
                break
    if A<=ord(x_next)<=Z:
        Path.append(x_next)
    if x_next == ' ':
        break
    nstep += 1
    r = r_next
    c = c_next
    x = x_next
ans1 = ''.join(Path)
print(ans1)
ans2 = nstep
print(ans2)

