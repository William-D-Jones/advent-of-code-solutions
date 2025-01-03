import sys
from copy import deepcopy

# parsing
X = list(map(int,list(open(sys.argv[1], 'r').read().strip())))
Mem = []
free = None
id_file_max = 0
for i,x in enumerate(X):
    if i % 2 == 0: # filled block
        for j in range(x):
            Mem.append(i // 2)
            if i // 2 > id_file_max:
                id_file_max = i // 2
    else: # empty block
        if free is None:
            free = len(Mem)
        for j in range(x):
            Mem.append('.')

# part 1
Compact = deepcopy(Mem)
for i in reversed(range(len(Compact))):
    if free > i:
        break
    if Compact[i] != '.':
        Compact[free] = Compact[i]
        Compact[i] = '.'
        while Compact[free] != '.':
            free += 1
ans1 = 0
for i,mem in enumerate(Compact):
    if mem != '.':
        ans1 += i * mem
    else:
        break
print(ans1)

# part 2
Compact = deepcopy(Mem)
ix_file = len(Compact) - 1
id_file = id_file_max
len_file = 1
while id_file >= 0:
    # get the index of the end of the file
    while ix_file > 0 and Compact[ix_file] != id_file:
        ix_file -= 1
    if ix_file == 0:
        break
    # get the length of the file
    while ix_file - (len_file - 1) - 1 >= 0 and \
    Compact[ix_file - (len_file - 1) - 1] == id_file:
        len_file += 1
    # find free space
    ix_free = 0
    len_free = 0
    while ix_free < ix_file - (len_file - 1) and len_free < len_file:
        if Compact[ix_free] == '.':
            if Compact[ix_free + len_free] == '.':
                len_free += 1
                if len_free >= len_file:
                    break
            else:
                ix_free = ix_free + len_free
                len_free = 0
        else:
            ix_free += 1
    # move the file
    if len_free >= len_file:
        for i in range(len_file):
            Compact[ix_free + i] = Compact[ix_file - i]
            Compact[ix_file - i] = '.'
    # reset for the next file
    id_file -= 1
    ix_file = ix_file - (len_file - 1)
    len_file = 1
ans2 = 0
for i,mem in enumerate(Compact):
    if mem != '.':
        ans2 += i * mem
print(ans2)


