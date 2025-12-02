import sys

# parsing
X = open(sys.argv[1], 'r').read().strip().split(',')
I = [tuple(map(int,x.split('-'))) for x in X]

# part 1
ans1 = 0
for i0,i1 in I:
    for i in range(i0,i1+1):
        s = str(i)
        if s[0:len(s)//2] == s[len(s)//2:]:
            ans1 += i
print(ans1)
    
# part 2
ans2 = 0
for i0,i1 in I:
    for i in range(i0,i1+1):
        s = str(i)
        div = 2
        while div <= len(s):
            if len(s) % div == 0:
                l = len(s) // div
                Spl = [ s[n*l : (n+1)*l] for n in range(div) ]
                if all(Spl[0] == spl for spl in Spl):
                    ans2 += i
                    break
            div += 1
print(ans2)

