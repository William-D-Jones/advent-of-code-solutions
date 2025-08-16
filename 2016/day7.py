import sys

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]

# part 1
ans1 = 0
for x in X:
    i = 0
    abba = {'in': 0, 'out': 0}
    abba_type = 'out'
    while i <= len(x)-4:
        if x[i] == '[':
            abba_type = 'in'
        elif x[i] == ']':
            abba_type = 'out'
        else:
            if x[i] == x[i+3] and x[i+1] == x[i+2] and x[i] != x[i+1] and \
            x[i+1] != '[' and x[i+1] != ']':
                abba[abba_type] += 1
                if abba['in'] > 0:
                    break
        i += 1
    if abba['out'] > 0 and abba['in'] == 0:
        ans1 += 1
print(ans1)

# part 2
ans2 = 0
for x in X:
    i = 0
    aba = {'in': [], 'out': []}
    aba_type = 'out'
    while i <= len(x)-3:
        if x[i] == '[':
            aba_type = 'in'
        elif x[i] == ']':
            aba_type = 'out'
        else:
            if x[i] == x[i+2] and x[i] != x[i+1] and \
            x[i+1] != '[' and x[i+1] != ']':
                aba[aba_type].append(''.join(x[i:i+3]))
        i += 1
    if any(''.join([seq[1:2], seq[0:1], seq[1:2]]) in aba['in'] for \
    seq in aba['out']):
        ans2 += 1
print(ans2)

