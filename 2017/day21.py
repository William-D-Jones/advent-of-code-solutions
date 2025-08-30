import sys

def enhance(n):
    I = [list('.#.'), list('..#'), list('###')]
    for _ in range(n):
        # get the size of the image
        nrow = len(I)
        ncol = len(I[0])
        assert nrow == ncol
        sz = nrow
        # determine the divisibility rule
        if sz % 2 == 0:
            div = 2
        elif sz % 3 == 0:
            div = 3
        else:
            assert False
        # prepare the next image
        I_next = [ ['' for c in range(sz*(div+1)//div)] for \
        r in range(sz*(div+1)//div) ]
        # apply the enhancement rules
        for ix_r in range(sz//div):
            for ix_c in range(sz//div):
                # prepare the sub-grid
                S_in = tuple( \
                tuple(I[r][c] for c in range(div*ix_c, div*(ix_c+1))) for \
                r in range(div*ix_r, div*(ix_r+1)) )
                # match the sub-grid
                S_out = Rule[S_in]
                sz_next = len(S_out)
                # reassign pixels to the sub-grid following the rule
                for r in range(sz_next*ix_r, sz_next*(ix_r+1)):
                    for c in range(sz_next*ix_c, sz_next*(ix_c+1)):
                        I_next[r][c] = S_out[r-sz_next*ix_r][c-sz_next*ix_c]
        I = I_next
    return I

# parsing
X = [ l.strip().split(' => ') for l in open(sys.argv[1], 'r') ]
# extract the rules
Rule = {}
for s_in, s_out in X:
    G_in = [list(r) for r in s_in.split('/')]
    G_out = [list(r) for r in s_out.split('/')]
    nrow = len(G_in)
    ncol = len(G_in[0])
    T_in = [[G_in[r][c] for r in range(nrow)] for c in range(ncol)]
    for G in (G_in, T_in):
        Rule[ tuple(tuple(G[r]) for r in range(nrow)) ] = G_out
        Rule[ tuple(tuple(G[r][::-1]) for r in range(nrow)) ] = G_out
        Rule[ tuple(tuple(G[r]) for r in reversed(range(nrow))) ] = G_out
        Rule[ tuple(tuple(G[r][::-1]) for r in reversed(range(nrow))) ] = G_out

# part 1
I = enhance(5)
ans1 = sum(1 for c in range(len(I[0])) for r in range(len(I)) if I[r][c] == '#')
print(ans1)

# part 2
I = enhance(18)
ans2 = sum(1 for c in range(len(I[0])) for r in range(len(I)) if I[r][c] == '#')
print(ans2)

