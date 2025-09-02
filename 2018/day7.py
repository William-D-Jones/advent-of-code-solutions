import sys
import re

A = ord('A')

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Rule = []
Step = set()
for x in X:
    M = re.match(\
    '^Step ([A-Z]+) must be finished before step ([A-Z]+) can begin.$', x)
    Rule.append( (M.group(1),M.group(2)) )
    Step.add( M.group(1) )
    Step.add( M.group(2) )

# part 1
Order = []
Q = list(Step)
i = 0
Step_Next = []
while Q:
    i = 0
    while i < len(Q):
        Prep = [ rule[0] for rule in Rule if rule[1] == Q[i] ]
        if not Prep or all( prep in Order for prep in Prep ):
            Step_Next.append(Q.pop(i))
        else:
            i += 1
    Step_Next = sorted(Step_Next)
    Order.append(Step_Next.pop(0))
ans1 = ''.join(Order)
print(ans1)

# part 2
Order = []
Q = list(Step)
i = 0
Step_Next = []
Step_Work = []
Time_Work = []
num_work = 5
time_add = 60
ans2 = 0
while Q:
    i = 0
    # setup the queue of work to be done
    while i < len(Q):
        Prep = [ rule[0] for rule in Rule if rule[1] == Q[i] ]
        if not Prep or all( prep in Order for prep in Prep ):
            Step_Next.append(Q.pop(i))
        else:
            i += 1
    Step_Next = sorted(Step_Next)
    # assign times to the work
    while Step_Next and len(Step_Work) < num_work:
        step = Step_Next.pop(0)
        Step_Work.append( step )
        Time_Work.append( time_add + ord(step)-A+1 )
    # complete the work
    min_time = min(Time_Work)
    ans2 += min_time
    for j in range(len(Time_Work)):
        Time_Work[j] -= min_time
    # identify completed work
    j = 0
    while j < len(Time_Work):
        if Time_Work[j] == 0:
            Time_Work.pop(j)
            Order.append(Step_Work.pop(j))
        else:
            j += 1
print(ans2)

