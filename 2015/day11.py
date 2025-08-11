import sys
from copy import copy

A = ord('a')
Z = ord('z')
A2Z = Z-A+1
FORBID = set(['i','o','l'])

def increment_password(password):
    i = len(password)
    new = 0 # the value of the old character
    old = 1 # the value of the new character
    while new < old:
        i -= 1
        old = ord(password[i:i+1])
        new = (old + 1 - A) % A2Z + A
        password = password[:i] + chr(new) + password[(i+1):]
    return password

def check_password(password):
    # check for forbidden characters
    if any(f in password for f in FORBID):
        return False
    # check for repeats and straights
    repeat = []
    ix_repeat = []
    straight = []
    ix_straight = []
    for i in range(len(password)):
        if i < len(password)-1:
            check2 = password[i:i+2]
            if check2[0:1] == check2[1:2] and check2 not in repeat and \
            (len(ix_repeat) == 0 or i > ix_repeat[-1]+1):
                repeat.append(check2)
                ix_repeat.append(i)
        if i < len(password)-2:
            check3 = password[i:i+3]
            if ord(check3[0:1])+2 == ord(check3[1:2])+1 == ord(check3[2:3]):
                straight.append(check3)
                ix_straight.append(i)
    if len(repeat) >= 2 and len(straight) >= 1:
        return True
    else:
        return False

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
password = increment_password( copy(X) )
while not check_password(password):
    password = increment_password(password)
ans1 = password
print(ans1)

# part 2
password = increment_password( copy(ans1) )
while not check_password(password):
    password = increment_password(password)
ans2 = password
print(ans2)

