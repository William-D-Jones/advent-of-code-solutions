import sys
from collections import defaultdict
from copy import deepcopy

# parsing
X = [list(l.strip()) for l in open(sys.argv[1], 'r')]
# locate the starting position
nrow = len(X)
ncol = len(X[0])
for r in range(nrow):
    for c in range(ncol):
        if X[r][c] == 'S':
            start = (r,c)
        elif X[r][c] == 'E':
            end = (r,c)

D = set([(-1,0), (0,1), (1,0), (0,-1)])

# parts 1 and 2
Path = [(start, (0,1))]
Score = [0]
Seen = defaultdict(int)
ans1 = 0
Seen_Tile = [set(Path)]
Best_Score = []
Best_Tile = []
while not all(coord[0] == end for coord in Path):
    Path_Next = []
    Score_Next = []
    Seen_Next = []
    Coord_Next = []
    Seen_Tile_Next = []
    for path,score,seen_tile in zip(Path,Score,Seen_Tile):
        coord,d = path
        # check all possible directions
        for dr,dc in D:
            seen_tile_d = deepcopy(seen_tile)
            # get the new coordinate
            step = (coord[0]+dr, coord[1]+dc)
            path_next = (step, (dr,dc))
            # get the new score
            score_next = score + 1 + \
            1000 * max(abs(d[0]-dr), abs(d[1]-dc))
            # check that the new coordinate is acceptable
            if step != start and X[step[0]][step[1]] != '#' and \
            (ans1 == 0 or ans1 >= score_next):
                if Seen[path_next] == 0 or Seen[path_next] > score_next:
                    seen_tile_d.add(path_next)
                    if (ans1 == 0 or ans1 >= score_next) and step == end:
                        ans1 = score_next
                        Best_Tile.append(seen_tile_d)
                        Best_Score.append(score_next)
                    else:
                        Path_Next.append(path_next)
                        Score_Next.append(score_next)
                        Seen[path_next] = score_next
                        Seen_Tile_Next.append(seen_tile_d)
                elif Seen[path_next] == score_next:
                    for i in range(len(Seen_Tile_Next)):
                        if path_next in Seen_Tile_Next[i]:
                            Seen_Tile_Next[i] |= seen_tile_d
    Path = Path_Next
    Score = Score_Next
    Seen_Tile = Seen_Tile_Next
print(ans1)
Best_Set = set()
for best_tile,best_score in zip(Best_Tile,Best_Score):
    if best_score == ans1:
        Best_Set |= set(path[0] for path in best_tile)
print(len(Best_Set))

