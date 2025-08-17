import sys
import hashlib
import re

def extract_rep(s, Rep, First_Only):
    Out = {rep: set() for rep in Rep}
    for rep in Rep:
        pattern = '(.)\\1{' + str(rep-1) + ',}'
        match = re.findall(pattern, s)
        if len(match) > 0:
            if rep in First_Only:
                Out[rep] |= set(match[0])
            else:
                Out[rep] |= set(match)
    return Out

def stretch_hash(hash_in, n):
    for i in range(n):
        hash_in = hashlib.md5(hash_in.encode()).hexdigest()
    return hash_in

def find_keys(salt, num_key, max_search, stretch):
    Key = []
    Q_Rep = []
    Q_Start = []
    i = 0
    while len(Key) < num_key or \
    (len(Q_Start) > 0 and min(Q_Start) < max(key[0] for key in Key)):
        hash_in = salt + str(i)
        hash_out = stretch_hash(hash_in, stretch)
        Reps = extract_rep(hash_out, (3,5), (3,))
        while len(Q_Start) > 0 and i > Q_Start[0] + max_search:
            Q_Rep.pop(0)
            Q_Start.pop(0)
        if len(Reps[5]) > 0:
            point = 0
            while point < len(Q_Rep):
                rep = Q_Rep[point]
                start = Q_Start[point]
                if len(rep & Reps[5]) > 0:
                    Q_Rep.pop(point)
                    Q_Start.pop(point)
                    Key.append((start, i))
                else:
                    point += 1
        if len(Reps[3]) > 0:
            Q_Start.append(i)
            Q_Rep.append(Reps[3])
        i += 1
    return Key

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
num_key = 64
max_search = 1000
Key = sorted(find_keys(X, num_key, max_search, 1))
ans1 = Key[num_key-1][0]
print(ans1)

# part 2
num_key = 64
max_search = 1000
Key = sorted(find_keys(X, num_key, max_search, 2017))
ans2 = Key[num_key-1][0]
print(ans2)

