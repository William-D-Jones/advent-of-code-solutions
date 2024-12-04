import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
R = []
for x in X:
    R.append([int(r) for r in x.split()])

def issafe(report):
    if sorted(report) != report and sorted(report, reverse = True) != report:
        return False
    for i in range(len(report) - 1):
        dist = abs(report[i+1] - report[i])
        if dist < 1 or dist > 3:
            return False
    return True

# part 1
ans = 0
for report in R:
    if issafe(report):
        ans += 1
print(ans)

# part 2
ans = 0
for report in R:
    for i in range(len(report)):
        keep = list(range(0, i)) + list(range(i+1, len(report)))
        report_drop = [report[j] for j in keep]
        if issafe(report_drop):
            ans += 1
            break
print(ans)

