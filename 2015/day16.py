import sys
import re

# parsing
Tape = """\
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""
Target = {}
for line in Tape.strip().split('\n'):
    item, num = line.split(': ')
    Target[item] = int(num)
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Sue = [{} for x in X]
for x in X:
    match = re.search(r'^Sue ([0-9]+): (.+)$', x)
    ix = int(match.group(1))
    for pair in match.group(2).split(', '):
        item, num = pair.split(': ')
        Sue[ix-1][item] = int(num)

# part 1
for i, sue in enumerate(Sue):
    if all(item not in sue.keys() or \
    sue[item] == num for item, num in Target.items()):
        ans1 = i+1
        break
print(ans1)

# part 2
sue2 = None
for i, sue in enumerate(Sue):
    if all(item not in sue.keys() or \
    (item != 'cats' and item != 'trees' and item != 'pomeranians' and \
    item != 'goldfish' and sue[item] == num) or \
    ((item == 'cats' or item == 'cats') and sue[item] > num) or \
    ((item == 'pomeranians' or item == 'goldfish') and sue[item] < num) for \
    item, num in Target.items()):
        ans2 = i+1
        break
print(ans2)

