import sys

# parsing
X = int(''.join([ l.strip() for l in open(sys.argv[1], 'r') ]))

# part 1
Buffer = [0]
point = 0
for num in range(1, 2018):
    point = (point + X + 1) % len(Buffer)
    Buffer = Buffer[:point+1] + [num] + Buffer[point+1:]
ans1 = Buffer[ Buffer.index(2017)+1 ]
print(ans1)

# part 2
ans2 = 0
for num in range(1, 50000000):
    point = (point + X + 1) % num
    if point == 0:
        ans2 = num
print(ans2)

