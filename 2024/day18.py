import sys
from collections import defaultdict

# parsing
X = [tuple(map(int,l.split(','))) for l in open(sys.argv[1], 'r')]

# part 1
D = set([(-1,0), (1,0), (0,-1), (0,1)])
nrow = 71
ncol = 71
Cor = set(X[0:1024])
start = (0,0)
end = (nrow-1, ncol-1)
Path = [start]
Score = [0]
Seen_Score = defaultdict(int)
min_path = None
while not all(path == end for path in Path):
    Path_Next = []
    Score_Next = []
    for path,score in zip(Path,Score):
        score_next = score+1
        for dc,dr in D:
            # setup the new step and score
            step = (path[0]+dc, path[1]+dr)
            if step == start or step in Cor or \
            not (0<=step[0]<ncol and 0<=step[1]<nrow):
                continue
            # check if we have reached the end
            if step == end and (min_path is None or min_path > score_next):
                min_path = score_next
            # check if the new step/score are acceptable
            if step != end and \
            (Seen_Score[step] == 0 or Seen_Score[step] > score_next) and \
            (min_path is None or min_path > score_next):
                Path_Next.append(step)
                Score_Next.append(score_next)
                Seen_Score[step] = score_next
    Path = Path_Next
    Score = Score_Next
print(min_path)

# part 2
D = set([(-1,0), (1,0), (0,-1), (0,1)])
nrow = 71
ncol = 71
start = (0,0)
end = (nrow-1, ncol-1)
for i in range(0,len(X)-1):
    Cor = set(X[:i+1])
    min_path = None
    done = False
    Path = [start]
    Score = [0]
    Seen_Score = defaultdict(int)
    while not all(path == end for path in Path) and not done:
        Path_Next = []
        Score_Next = []
        for path,score in zip(Path,Score):
            score_next = score+1
            for dc,dr in D:
                # setup the new step and score
                step = (path[0]+dc, path[1]+dr)
                if step == start or step in Cor or \
                not (0<=step[0]<ncol and 0<=step[1]<nrow):
                    continue
                # check if we have reached the end
                if step == end and (min_path is None or min_path > score_next):
                    min_path = score_next
                    done = True
                    break
                # check if the new step/score are acceptable
                if step != end and \
                (Seen_Score[step] == 0 or Seen_Score[step] > score_next) and \
                (min_path is None or min_path > score_next):
                    Path_Next.append(step)
                    Score_Next.append(score_next)
                    Seen_Score[step] = score_next
            if done:
                break
        Path = Path_Next
        Score = Score_Next
    if not done:
        print(X[i])
        break
