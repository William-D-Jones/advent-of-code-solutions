import sys

# parsing
X1,X2 = '\n'.join([ l.strip() for l in open(sys.argv[1], 'r') ]).split('\n\n')
S = []
for i,p in enumerate(list(X1.strip().split()[2])):
    if p == '#':
        S.append(i)
    elif p == '.':
        pass
    else:
        assert False
R = []
for x in X2.split('\n'):
    s_in, p_out = x.split(' => ')
    assert not (s_in == '.....' and p_out == '#')
    R.append( (list(s_in), p_out) )

# parts 1 and 2
g1 = 20
g2 = 50000000000
for g in range(g2):
    S_next = []
    for i in range(min(S)-2, max(S)+2):
        for s_in, p_out in R:
            if all( (s_in[2+j] == '#' and i+j in S) or \
            (s_in[2+j] == '.' and i+j not in S) for j in range(-2,3)):
                if p_out == '#':
                    S_next.append(i)
                elif p_out == '.':
                    pass
                else:
                    assert False
    if all(len(S_next) == len(S) and S_next[i] == S[i]+1 for \
    i in range(len(S))):
        n = g2-1-g
        ans2 = sum(s + n for s in S_next)
        break
    S = S_next
    if g == g1-1:
        ans1 = sum(S)
print(ans1)
print(ans2)

