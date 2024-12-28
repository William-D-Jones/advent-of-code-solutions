import sys
from collections import Counter
from copy import deepcopy

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
nrow = len(X)
ncol = len(X[0])
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == 'S':
            start = (r,c)
        elif X[r][c] == 'E':
            end = (r,c)

# find the fastest base time and path to the end
D = set([(-1,0),(1,0),(0,-1),(0,1)])
tmin = 0
pos = deepcopy(start)
Seen = Counter()
Seen[start] = 0
while pos != end:
    for dr,dc in D:
        next_pos = (pos[0]+dr,pos[1]+dc)
        if next_pos not in Seen.keys() and X[next_pos[0]][next_pos[1]] != '#':
            tmin += 1
            pos = next_pos
            Seen[pos] = tmin
            break

# parts 1 and 2
Cheat = [] # each cheat entry is a list of positions followed by savings
ch_len = 20
for ch0 in Seen.keys():
    Cheat_Path = [[ch0]] # list of active cheat paths
    Cheat_Seen = Counter() # counts cheat time to seen cheat coordinates
    Cheat_Seen[ch0] = 0
    for i in range(ch_len):
        Cheat_Path_Next = []
        for path in Cheat_Path:
            chi = path[-1] # the last cheat coordinate for this active path
            for dr, dc in D:
                # get the next possible cheat coordinate
                chj = (chi[0]+dr,chi[1]+dc)
                if chj not in Cheat_Seen.keys():
                    # we have not yet seen this coordinate in the cheat
                    Cheat_Seen[chj] = i+1
                else:
                    # we have cheated to this coordinate before (and faster)
                    continue
                # continue the cheat
                Cheat_Path_Next.append(path + [chj])
                # check if we returned to the path
                if chj in Seen.keys():
                    ch_save = Seen[chj] - (Seen[ch0] + i+1)
                    if ch_save > 0:
                        Cheat.append(Cheat_Path_Next[-1] + [ch_save])
        Cheat_Path = Cheat_Path_Next
ans1 = 0
ans2 = 0
for cheat in Cheat:
    if cheat[-1] >= 100:
        if len(cheat) <= 4:
            ans1 += 1
        ans2 += 1
print(ans1)
print(ans2)
