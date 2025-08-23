import sys

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# part 1
for i in range(3, len(X)):
    mark = X[i-3:i+1]
    if all(mark.count(char) == 1 for char in mark):
        ans1 = i+1
        break
print(ans1)

# part 2
for i in range(13, len(X)):
    mark = X[i-13:i+1]
    if all(mark.count(char) == 1 for char in mark):
        ans2 = i+1
        break
print(ans2)
