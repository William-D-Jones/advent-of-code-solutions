import sys
import math

def get_divisors(k):
    Divisors = []
    d = 1
    dmax = k
    while d < dmax:
        dmax = k // d
        if k % d == 0:
            Divisors.append(d)
            Divisors.append(dmax)
        d += 1
    return sorted(Divisors)

# parsing
X = [ int(l.strip()) for l in open(sys.argv[1], 'r') ][0]

# part 1
k = 1
num_presents = 10
max_div = math.ceil(X / num_presents)
while k <= X:
    if sum(get_divisors(k)) >= max_div:
        break
    k += 1
ans1 = k
print(ans1)

# part 2
k = 1
num_presents = 11
max_houses = 50
max_div = math.ceil(X / num_presents)
while k <= X:
    Div = get_divisors(k)
    Div_Fil = []
    for div in Div:
        if div * max_houses >= k:
            Div_Fil.append(div)
    if sum(Div_Fil) >= max_div:
        break
    k += 1
ans2 = k
print(ans2)

