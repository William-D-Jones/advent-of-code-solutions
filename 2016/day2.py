import sys

D = {'U': (-1,0), 'R': (0,1), 'D': (1,0), 'L': (0,-1)}

def parse_buttons(txt):
    Buttons = {}
    Txt = [list(line) for line in txt.split('\n')]
    for r, Line in enumerate(Txt):
        c = 0
        while c < (len(Line)+1) // 2:
            char = Line[c*2]
            if char != ' ':
                Buttons[ (r,c) ] = char
            c += 1
    return Buttons

def get_button(inst, start, Buttons):
    r, c = start
    for i in range(len(inst)):
        dr, dc = D[ inst[i:i+1] ]
        if (r+dr,c+dc) in Buttons.keys():
            r += dr
            c += dc
    return Buttons[ (r,c) ], (r,c)

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
B1 = """\
1 2 3
4 5 6
7 8 9
"""
Button1 = parse_buttons(B1)
iButton1 = {value: key for key, value in Button1.items()}
ans1 = ''
start = iButton1['5']
for inst in X:
    code_next, start = get_button(inst, start, Button1)
    ans1 += str(code_next)
print(ans1)

# part 2
B2 = """\
    1
  2 3 4
5 6 7 8 9
  A B C
    D
"""
Button2 = parse_buttons(B2)
iButton2 = {value: key for key, value in Button2.items()}
ans2 = ''
start = iButton2['5']
for inst in X:
    code_next, start = get_button(inst, start, Button2)
    ans2 += str(code_next)
print(ans2)

