import sys

KNUM = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']]
KDIR = [['', '^', 'A'], ['<', 'v', '>']]
OPS = {'^':(-1,0), 'v':(1,0), '<':(0,-1), '>':(0,1), 'A':'A'}
EFF = {}
for r in range(len(KDIR)):
    for c in range(len(KDIR[r])):
        press = KDIR[r][c]
        if press != '':
            EFF[press] = (r,c)
print(EFF)

def get_paths(start, pad, target):
    nrow = len(pad)
    ncol = len(pad[0])
    Keys = [''] # what keys we have pressed
    Paths = [[start]] # what coordinates we have taken
    Outs = [''] # what outputs we have produced
    Seen = [set([start])] # what coordinates we have seen since the last A
    Eff = [0] # the efficiency to get to the next button press
    shortest = None
    typed = '' # the best output we have so far
    while not all(out == target for out in Outs) \
    and (shortest is None or all(len(path) == shortest for path in Paths)):
        Keys_Next = []
        Paths_Next = []
        Outs_Next = []
        Seen_Next = []
        Eff_Next = []
        for key,path,out,seen,eff in zip(Keys,Paths,Outs,Seen,Eff):
            # check if we have typed the target string
            if out == target:
                if len(path) == shortest:
                    Keys_Next.append(key)
                    Paths_Next.append(path)
                    Outs_Next.append(out)
                    Seen_Next.append(seen)
                continue
            # check if we can add another operation to the current path
            elif shortest is not None and len(path) + 1 > shortest:
                continue
            # check all available operations
            for press,op in OPS.items():
                if out != typed and op != 'A':
                    # do not translate the arm if we must type to keep up
                    continue
                if op != 'A': # the key press translates the arm
                    # compute the next coordinate
                    dr,dc = op
                    coord = (path[-1][0]+dr, path[-1][1]+dc)
                    # check if the coordinate is valid
                    if 0 <= coord[0] < nrow and 0 <= coord[1] < ncol \
                    and pad[coord[0]][coord[1]] != '' \
                    and (shortest is None or shortest > len(path)+1) \
                    and coord not in seen:
                        Keys_Next.append(key + press)
                        Paths_Next.append(path + [coord])
                        Outs_Next.append(out)
                        Seen_Next.append(seen | set([coord]))
                else: # the key press extends the arm
                    # add a character to the output
                    out += pad[ path[-1][0] ][ path[-1][1] ]
                    # check if the output is valid
                    if target.startswith(out):
                        Keys_Next.append(key + press)
                        Paths_Next.append(path + [path[-1]])
                        Outs_Next.append(out)
                        Seen_Next.append(set([path[-1]]))
                        # check if the target has been found
                        if target == out:
                            if shortest is None or shortest > len(path)+1:
                                shortest = len(path)+1
                        # if target not found, remember what is typed so far
                        else:
                            typed = out
        Keys = Keys_Next
        Paths = Paths_Next
        Outs = Outs_Next
        Seen = Seen_Next
    return Keys
                   
# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]

# part 1
for x in X:
    # find the shortest paths for the numerical robot
    Keys_Num = get_paths((3,2),KNUM,x)
    # find the shortest paths for the first directional robot
    Keys_Dir1 = get_paths((0,2),KDIR,Keys_Num[0])
    # find the shortest paths for the second directional robot
    Keys_Dir2 = get_paths((0,2),KDIR,Keys_Dir1[0])
    #Keys_Dir2 = []
    #for key in Keys_Dir1:
    #    Keys_Dir2 += get_paths((0,2),KDIR,key)
print(len('v<<A>>^A<A>AvA<^AA>A<vAAA>^A'))
print(len(Keys_Dir1[0]))
print(len('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'))
print(len(Keys_Dir2[0]))


