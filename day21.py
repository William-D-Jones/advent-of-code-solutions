import sys

# the numeric keypad
KNUM = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']]
# the directional keypad
KDIR = [['', '^', 'A'], ['<', 'v', '>']]
# dictionary to convert directional keypad presses to directions
OPS = {'^':(-1,0), 'v':(1,0), '<':(0,-1), '>':(0,1), 'A':'A'}
# ictionary to convert directions to directional keypad presses
iOPS = {value:key for key,value in OPS.items()}

def get_key_pair(pad, start, end):
    """
    Get the key-presses required to journey on PAD from the START character
    to the END character and press it.
    """
    if start == end:
        return [ 'A' ]
    for r,row in enumerate(pad):
        for c,char in enumerate(row):
            if char == start:
                coord_start = (r,c)
            if char == end:
                coord_end = (r,c)
            if char == '':
                coord_blank = (r,c)
    # there are two shortest paths between points
    # one path may need to be dropped if it contains a blank square
    # compute Manhattan distances
    dr = coord_end[0] - coord_start[0]
    dc = coord_end[1] - coord_start[1]
    keyr = iOPS[ (dr//abs(dr),0) ] * abs(dr) if dr!=0 else ''
    keyc = iOPS[ (0,dc//abs(dc)) ] * abs(dc) if dc!=0 else ''
    # in principle the keypresses can be either keyr+keyc or keyc+keyr
    # however, one of these orders may not be allowed if a blank is crossed
    keyrc = keyr+keyc+'A'
    keycr = keyc+keyr+'A'
    if coord_start[0]==coord_blank[0] and coord_end[1]==coord_blank[1]:
        return [ keyrc ]
    elif coord_start[1]==coord_blank[1] and coord_end[0]==coord_blank[0]:
        return [ keycr ]
    elif keyrc != keycr:
        return [ keyrc, keycr ]
    else:
        return [ keyrc ]

#for char1 in 'A<>^v':
#    for char2 in 'A<>^v':
#        print(char1+char2+': ', get_key_pair(KDIR, char1, char2))
#sys.exit('We are done')

def get_key_sequence(pad, sequence):
    for i in range(len(sequence)):
        if i == 0:
            Keys = get_key_pair(pad, 'A', sequence[i])
        else:
            Keys_New = get_key_pair(pad, sequence[i-1], sequence[i])
            # determine which of Keys_New is the best
            # case 1: Keys_New contains only one element, use it
            if len(Keys_New) == 1:
                Keys = [ Keys[0] + Keys_New[0] ]
            else:
                # need to resolve ambiguities based on the beginning character
                # v vs. <
                if ( Keys_New[0].startswith('v') and \
                Keys_New[1].startswith('<') ) \
                or ( Keys_New[1].startswith('v') and \
                Keys_New[0].startswith('<') ):
                    Keys = [ Keys[0] + ( Keys_New[0] \
                    if Keys_New[0].startswith('v') else Keys_New[1] ) ]
                # ^ vs. <
                elif ( Keys_New[0].startswith('^') and \
                Keys_New[1].startswith('<') ) \
                or ( Keys_New[1].startswith('^') and \
                Keys_New[0].startswith('<') ):
                    Keys = [ Keys[0] + ( Keys_New[0] \
                    if Keys_New[0].startswith('^') else Keys_New[1] ) ]
                # v vs. >
                elif ( Keys_New[0].startswith('v') and 
                Keys_New[1].startswith('>') ) \
                or ( Keys_New[1].startswith('v') and \
                Keys_New[0].startswith('>') ):
                    Keys = [ Keys[0] + ( Keys_New[0] \
                    if Keys_New[0].startswith('>') else Keys_New[1] ) ]
                else:
                    Keys = [prefix+suffix for suffix in Keys_New for prefix in Keys]
                    #Keys = [ Keys[0] + Keys_New[0] ]   
    return Keys

def extract_min_len(items):
    min_len = min([len(item) for item in items])
    stripped = []
    for item in items:
        if len(item) == min_len:
            stripped.append(item)
    return stripped

# parsing
X = [l.strip() for l in open(sys.argv[1], 'r')]

# part 1
ans1 = 0
ndir = 2
for x in X:
    # get the sequence to be inputted on the first directional keypad
    Keys = extract_min_len(get_key_sequence(KNUM, x))
    print('We are on the numerical robot')
    print('The number of keys is: ',len(Keys))
    print(Keys[0:10])
    for i in range(ndir):
        print('We are on directional robot: ',i)
        Keys_Next = []
        for buttons in Keys:
            Keys_Next += get_key_sequence(KDIR, buttons)
        Keys = extract_min_len(Keys_Next)
        print('The number of keys is: ',len(Keys))
        print(Keys[0:10])
    shortest = min([len(buttons) for buttons in Keys])
    ans1 += shortest * int(x[:-1])
print(ans1)
