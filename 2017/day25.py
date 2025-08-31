import sys
import re
from collections import defaultdict, Counter

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
State = defaultdict(dict)
for x in X:
    if not x:
        continue
    # parse the beginning state
    M_Begin = re.match('^Begin in state ([A-Z]+)\\.$', x)
    if M_Begin:
        begin = M_Begin.group(1)
    # parse the checksum command
    M_Check = re.match('^Perform a diagnostic checksum after '+\
    '([0-9]+) steps\\.$', x)
    if M_Check:
        check = int(M_Check.group(1))
    # parse the state
    M_State = re.match('^In state ([A-Z]+):$', x)
    if M_State:
        state = M_State.group(1)
    # parse the value
    M_Val = re.match('^If the current value is ([01]):$', x)
    if M_Val:
        val = int(M_Val.group(1))
    # parse the write command
    M_Write = re.match('^- Write the value ([01])\\.$', x)
    if M_Write:
        write = int(M_Write.group(1))
    # parse the movement
    M_Move = re.match('^- Move one slot to the (right|left)\\.$', x)
    if M_Move:
        dx = M_Move.group(1)
        if dx == 'right':
            move = 1
        elif dx == 'left':
            move = -1
        else:
            assert False
    # parse the next state
    M_Next = re.match('^- Continue with state ([A-Z]+)\\.$', x)
    if M_Next:
        nxt = M_Next.group(1)
        State[state][val] = (write, move, nxt)

# part 1
Tape = Counter()
point = 0
state = begin
for _ in range(check):
    val = Tape[point]
    write, move, nxt = State[state][val]
    Tape[point] = write
    point += move
    state = nxt
ans1 = sum(Tape.values())
print(ans1)

