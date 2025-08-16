import sys

def count_triangles(T):
    count = 0
    for t in T:
        if t[0]+t[1]>t[2] and t[0]+t[2]>t[1] and t[1]+t[2]>t[0]:
            count += 1
    return count

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
T = []
for x in X:
    T.append(list(map(int, x.split())))

# part 1
ans1 = count_triangles(T)
print(ans1)

# part 2
Tv = []
for i in range(len(T) // 3):
    T3 = T[(i*3):(i*3)+3]
    for j in range(3):
        Tv.append([t[j] for t in T3])
ans2 = count_triangles(Tv)
print(ans2)
    
