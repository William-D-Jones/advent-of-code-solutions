import sys
import re

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
File = {}
Dir = ['/']
path = ['']
for x in X:
    xs = x.split()
    if xs[0] == '$':
        if xs[1] == 'cd':
            if xs[2] == '/':
                pass
            elif xs[2] == '..':
                path.pop()
            else:
                path.append(xs[2])
    else:
        # we are in the output of an ls command
        if xs[0] == 'dir':
            Dir.append('/'.join(path + [xs[1], '']))
        else:
            File['/'.join(path + [xs[1]])] = int(xs[0])

# part 1
ans1 = 0
Dir_Sz = {}
for path_dir in Dir:
    sz = 0
    for path_file, sz_file in File.items():
        if re.match('^'+path_dir, path_file):
            sz += sz_file
    Dir_Sz[path_dir] = sz
    if sz <= 100000:
        ans1 += sz
print(ans1)

# part 2
free = 70000000-Dir_Sz['/']
ans2 = min([sz for sz in Dir_Sz.values() if free+sz >= 30000000])
print(ans2)

