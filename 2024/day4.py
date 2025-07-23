import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

def extract_word(list_search, coord_start, coord_end):
    len_x = len(list_search)
    len_y = len(list_search[0])
    span_x = coord_end[0] - coord_start[0]
    span_y = coord_end[1] - coord_start[1]
    if not (0 <= coord_start[0] < len_x) or \
    not (0 <= coord_start[1] < len_y) or \
    not (0 <= coord_end[0] < len_x) or \
    not (0 <= coord_end[1] < len_y):
        # the coordinates are outside the wordsearch range
        return None
    elif span_x != 0 and span_y != 0 and abs(span_x) != abs(span_y):
        # if a diagonal extraction, the coordinates must be square
        return None
    else:
        word = ''
        step_x = span_x // abs(span_x) if span_x != 0 else 0
        step_y = span_y // abs(span_y) if span_y != 0 else 0
        for i in range(max(abs(span_x), abs(span_y)) + 1):
            ix_x = coord_start[0] + i * step_x
            ix_y = coord_start[1] + i * step_y
            c = X[ix_x][ix_y]
            word = ''.join([word, c])
        return word

ans1 = 0
ans2 = 0
for x in range(len(X)):
    for y in range(len(X[x])):
        if X[x][y:y+1] == 'X':
            # get XMAS word candidates
            words = [extract_word(X, (x,y), (x,y+3)),\
            extract_word(X, (x,y), (x,y-3)),\
            extract_word(X, (x,y), (x+3,y)),\
            extract_word(X, (x,y), (x-3,y)),\
            extract_word(X, (x,y), (x+3,y+3)),\
            extract_word(X, (x,y), (x+3,y-3)),\
            extract_word(X, (x,y), (x-3,y+3)),\
            extract_word(X, (x,y), (x-3,y-3))]
            # count XMAS word candidates
            ans1 += words.count('XMAS')
        if X[x][y:y+1] == 'A':
            words = [extract_word(X, (x-1,y-1), (x+1,y+1)),
            extract_word(X, (x-1,y+1), (x+1,y-1))]
            ans2 += 1 if words.count('MAS') + words.count('SAM') == 2 else 0
            
print(ans1)
print(ans2)

