import sys
import hashlib
from collections import deque

D = {'U': (-1,0), 'R': (0,1), 'D': (1,0), 'L': (0,-1)}
D_ix = {0: 'U', 1: 'D', 2: 'L', 3: 'R'}

def get_doors(code):
    Open = []
    code_hash = hashlib.md5(code.encode()).hexdigest()
    for i in D_ix.keys():
        if code_hash[i:i+1] in 'bcdef':
            Open.append(D_ix[i])
    return Open

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
nrow = 4
ncol = 4
End = (3,3)
Path = deque([''])
Pos = deque([(0,0)])
min_step = None
while Path:
    path = Path.popleft()
    r,c = Pos.popleft()
    code = X + path
    if min_step is not None and len(path)+1 > min_step:
        continue
    for dx in get_doors(code):
        dr,dc = D[dx]
        nr = r+dr
        nc = c+dc
        if 0<=nr<nrow and 0<=nc<ncol:
            if (nr,nc) == End:
                if min_step is None or min_step > len(path+dx):
                    min_step = len(path+dx)
                    min_path = path+dx
            else:
                Path.append( path+dx )
                Pos.append( (nr,nc) )
ans1 = min_path
print(ans1)

# part 2
nrow = 4
ncol = 4
End = (3,3)
Path = deque([''])
Pos = deque([(0,0)])
max_step = None
while Path:
    path = Path.popleft()
    r,c = Pos.popleft()
    code = X + path
    for dx in get_doors(code):
        dr,dc = D[dx]
        nr = r+dr
        nc = c+dc
        if 0<=nr<nrow and 0<=nc<ncol:
            if (nr,nc) == End:
                if max_step is None or max_step < len(path+dx):
                    max_step = len(path+dx)
                    max_path = path+dx
            else:
                Path.append( path+dx )
                Pos.append( (nr,nc) )
ans2 = max_step
print(ans2)

