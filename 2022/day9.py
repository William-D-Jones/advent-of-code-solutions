import sys

D = { 'U': (-1,0), 'R': (0,1), 'D': (1,0), 'L': (0,-1) }

def drag_tail(len_rope):
    Knot = {i: (0,0) for i in range(len_rope)}
    Seen = set()
    for dx,n in Mot:
        dr,dc = D[dx]
        for i in range(n):
            # move the head of the rope
            hr,hc = Knot[0]
            hr += dr
            hc += dc
            Knot[0] = (hr,hc)
            # move the next knots
            for k in range(1, len_rope):
                hr,hc = Knot[k-1]
                tr,tc = Knot[k]
                ar = hr-tr
                ac = hc-tc
                if ar == 0 and abs(ac)>1:
                    tc += ac//abs(ac)
                elif ac == 0 and abs(ar)>1:
                    tr += ar//abs(ar)
                elif abs(ar)==1 and abs(ac)>1:
                    tr=hr
                    tc += ac//abs(ac)
                elif abs(ac)==1 and abs(ar)>1:
                    tc=hc
                    tr += ar//abs(ar)
                elif abs(ar)>1 and abs(ac)>1:
                    tr += ar//abs(ar)
                    tc += ac//abs(ac)
                Knot[k] = (tr,tc)
            Seen.add(Knot[len_rope-1])
    return Seen

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Mot = []
for x in X:
    xs = x.split()
    Mot.append( (xs[0], int(xs[1])) )

# part 1
ans1 = len(drag_tail(2))
print(ans1)

# part 2
ans2 = len(drag_tail(10))
print(ans2)

