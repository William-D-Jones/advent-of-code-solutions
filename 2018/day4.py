import sys
import re
from collections import defaultdict, Counter
import datetime

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Log = []
for x in X:
    M = re.match('^\\[([0-9]{4})-([0-9]{2})-([0-9]{2}) '+\
    '([0-9]{2}):([0-9]{2})\\] (.+)$', x)
    time = datetime.datetime(*[int(M.group(i)) for i in range(1,6)], \
    0, tzinfo=datetime.timezone.utc)
    gs = M.group(6).split()
    Log.append((time, gs))
Log = sorted(Log)
Guard = defaultdict(list)
for i,(time,gs) in enumerate(Log):
    if gs[0] == 'Guard':
        if i > 0:
            Guard[guard].append( (state, time) )
        guard = int(gs[1][1:])
        state = 1 # 1 for awake, 0 for asleep
        Guard[guard].append( (state,time) )
    elif gs[0] == 'falls':
        state = 0
        Guard[guard].append( (state, time) )
    elif gs[0] == 'wakes':
        state = 1
        Guard[guard].append( (state, time) )

# identify the minutes when each guard was sleeping
Sleep = []
for guard in Guard.keys():
    for i in range(len(Guard[guard])-1):
        if Guard[guard][i][0] == 0 and Guard[guard][i+1][0] == 1:
            r = range(Guard[guard][i][1].minute, \
            Guard[guard][i+1][1].minute)
            for m in r:
                Sleep.append( (m, guard) )
Minutes = Counter(Sleep)

# part 1
# determine the guard that slept the most
Tot_Slept = Counter(sl[1] for sl in Sleep)
g1 = sorted( (slept,guard) for guard,slept in Tot_Slept.items() )[-1][1]
g1_minute = \
sorted( (n,m) for (m,guard),n in Minutes.items() if guard == g1 )[-1][1]
ans1 = g1 * g1_minute
print(ans1)

# part 2
# determine which guard is most frequently asleep on the same minute
g2 = sorted( (n,m,guard) for (m,guard),n in Minutes.items() )[-1][2]
g2_minute = sorted( (n,m,guard) for (m,guard),n in Minutes.items() )[-1][1]
ans2 = g2 * g2_minute
print(ans2)

