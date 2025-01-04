import sys

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

Win = []
Plays = []
for x in X:
    wins = True
    num = []
    for i,val in enumerate(x.split()):
        if i < 2:
            continue
        if val == '|':
            wins = False
            Win.append(num)
            num = []
            continue
        num.append(val)
    Plays.append(num)
Score = []
for i,P in enumerate(Plays):
    nwin = 0
    score = 0
    for p in P:
        if p in Win[i]:
            nwin += 1
            if nwin > 1:
                score = score * 2
            else:
                score += 1
    Score.append(score)
print(sum(Score))

Score = []
for i in range(len(Plays)):
    Score.append(1)
for i,P in enumerate(Plays):
    # get the number of matching numbers
    nwin = 0
    for p in P:
        if p in Win[i]:
            nwin += 1
    # apply the matching numbers to the subsequent cards
    j = i + 1
    while j - i <= nwin:
        Score[j] += Score[i]
        j += 1
print(sum(Score))

