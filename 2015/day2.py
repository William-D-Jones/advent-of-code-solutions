import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Dim = []
for x in X:
    l, w, h = map(int, x.split('x'))
    Dim.append( (l,w,h) )

# part 1
ans1 = 0
for l, w, h in Dim:
    sa = 2*l*w + 2*w*h + 2*h*l
    sl = min(l*w, w*h, h*l)
    ans1 += sa + sl
print(ans1)

# part 2
ans2 = 0
for l, w, h in Dim:
    wrap = min(2*(l+w), 2*(w+h), 2*(h+l))
    bow = l*w*h
    ans2 += wrap + bow
print(ans2)


