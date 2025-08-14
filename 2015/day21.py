import sys
import itertools
from copy import deepcopy

def fight(Player, Boss):
    Player = deepcopy(Player)
    Boss = deepcopy(Boss)
    attack = Player
    defend = Boss
    while Player['Hit Points'] > 0 and Boss['Hit Points'] > 0:
        hit = attack['Damage']
        armor = defend['Armor']
        hit = max(1, hit-armor)
        defend['Hit Points'] -= hit
        attack, defend = defend, attack
    if Player['Hit Points'] > 0:
        return True
    else:
        return False

def equip(HP, Equipment):
    Player = {'Hit Points': HP, 'Damage': 0, 'Armor': 0}
    cost = 0
    for item in Equipment:
        cost += item[0]
        Player['Damage'] += item[1]
        Player['Armor'] += item[2]
    return cost, Player

# parsing
S = """\
Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""
Weapon = {}
Armor = {}
Ring = {}
W, A, R = S.strip().split('\n\n')
for ix, item in enumerate(W.split('\n')):
    if ix == 0:
        continue
    name, cost, damage, armor = item.split()
    Weapon[name] = (int(cost), int(damage), int(armor))
for ix, item in enumerate(A.split('\n')):
    if ix == 0:
        continue
    name, cost, damage, armor = item.split()
    Armor[name] = (int(cost), int(damage), int(armor))
for ix, item in enumerate(R.split('\n')):
    if ix == 0:
        continue
    name, stat, cost, damage, armor = item.split()
    Ring[' '.join([name, stat])] = (int(cost), int(damage), int(armor))
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Boss = {}
for x in X:
    item, num = x.split(': ')
    Boss[item] = int(num)

# part 1
HP = 100
min_cost = None
for weapon_combo in itertools.combinations(Weapon.values(), 1):
    for num_armor in range(2):
        for armor_combo in itertools.combinations(Armor.values(), num_armor):   
            for num_ring in range(3):
                for ring_combo in \
                itertools.combinations(Ring.values(), num_ring):
                    Equipment = \
                    list(weapon_combo) + list(armor_combo) + list(ring_combo)
                    cost, Player = equip(HP, Equipment)
                    if fight(Player, Boss) and \
                    (min_cost is None or cost < min_cost):
                        min_cost = cost
ans1 = min_cost
print(ans1)

# part 2
HP = 100
max_cost = None
for weapon_combo in itertools.combinations(Weapon.values(), 1):
    for num_armor in range(2):
        for armor_combo in itertools.combinations(Armor.values(), num_armor):   
            for num_ring in range(3):
                for ring_combo in \
                itertools.combinations(Ring.values(), num_ring):
                    Equipment = \
                    list(weapon_combo) + list(armor_combo) + list(ring_combo)
                    cost, Player = equip(HP, Equipment)
                    if not fight(Player, Boss) and \
                    (max_cost is None or cost > max_cost):
                        max_cost = cost
ans2 = max_cost
print(ans2)

