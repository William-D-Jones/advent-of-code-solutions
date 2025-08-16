import sys
import re
from collections import Counter

A = ord('a')
Z = ord('z')
A2Z = Z-A+1

def is_room(room):
    Cnt = Counter(list(''.join(room[0].split('-'))))
    Max_Cnt = set(list(reversed(sorted(Cnt.values())))[0:5])
    Max_Name = []
    for max_cnt in list(reversed(sorted(list(Max_Cnt)))):
        Max_Name_Next = []
        for name, n in Cnt.items():
            if n == max_cnt:
                Max_Name_Next.append(name)
        Max_Name += sorted(Max_Name_Next)
    checksum = ''.join(Max_Name[0:5])
    return checksum == room[2]

def decrypt_room(room):
    name = room[0]
    name_decrypt = ''
    for char in name:
        if char == '-':
            name_decrypt += ' '
        else:
            name_decrypt += chr(A + (ord(char)-A+room[1]) % A2Z)
    return name_decrypt

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Room = []
for x in X:
    match = re.match('^([a-z\\-]+)-([0-9]+)\\[([a-z]+)\\]$', x)
    Room.append( (match.group(1), int(match.group(2)), match.group(3)) )

# parts 1 and 2
ans1 = 0
for room in Room:
    if is_room(room):
        ans1 += room[1]
        if decrypt_room(room) == 'northpole object storage':
            ans2 = room[1]
print(ans1)
print(ans2)

