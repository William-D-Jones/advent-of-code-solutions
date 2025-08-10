import sys
from collections import defaultdict

def is_nice_1(txt):
    # count the number of vowels
    num_vowel = txt.count('a') + txt.count('e') + txt.count('i') + \
    txt.count('o') + txt.count('u')
    if num_vowel < 3:
        return False
    # identify prohibited strings
    num_prohibited = txt.count('ab') + txt.count('cd') + txt.count('pq') + \
    txt.count('xy')
    if num_prohibited > 0:
        return False
    # identify double letters
    dbl = -1
    for i in range(1, len(txt)):
        c1, c2 = list( txt[i-1:i+1] )
        if c1 == c2:
            dbl = i
            break
    if dbl == -1:
        return False

    # if all the criteria are fulfilled, the string is nice
    return True

def is_nice_2(txt):
    # identify repeated letters with one letter between them
    dbl = -1
    for i in range(2, len(txt)):
        c1, c2, c3 = list( txt[i-2:i+1] )
        if c1 == c3:
            dbl = i
            break
    if dbl == -1:
        return False
    # identify pairs of letters
    Pair = defaultdict(list)
    pair_found = None
    for i in range(1, len(txt)):
        pair = txt[i-1:i+1]
        for ix in Pair[pair]:
            if ix<(i-1) or ix>i+1:
                pair_found = (pair, ix, i)
                break
        Pair[pair].append(i)
        if pair_found is not None:
            break
    if pair_found is None:
        return False

    # if all the criteria are fulfilled, the string is nice
    return True

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
ans1 = 0
for x in X:
    if is_nice_1(x):
        ans1 += 1
print(ans1)

# part 2
ans2 = 0
for x in X:
    if is_nice_2(x):
        ans2 += 1
print(ans2)

