import sys
from collections import deque
from copy import deepcopy

def fight(Player, Boss, hard = False):
    Q_Player = deque([Player])
    Q_Boss = deque([Boss])
    Q_Up = deque(['player'])
    Q_Effect = deque([[]])
    Q_Spent = deque([0])
    min_spent = None
    while Q_Player:
        player = Q_Player.popleft()
        boss = Q_Boss.popleft()
        up = Q_Up.popleft()
        Effect = Q_Effect.popleft()
        spent = Q_Spent.popleft()
        if hard and up == 'player':
            player['Hit Points'] -= 1
            if player['Hit Points'] <= 0:
                continue
        # apply existing effects
        Effect_Next = []
        for effect in Effect:
            if effect[3] == 0:
                if effect[4] > 0:
                    player['Armor'] = 0
                continue
            effect[3] -= 1
            if effect[4] > 0:
                player['Armor'] = effect[4]
            if effect[5] > 0:
                boss['Hit Points'] -= max(1, effect[5])
            player['Mana'] += effect[6]
            Effect_Next.append(effect)
        # check if existing effects have killed the boss
        if boss['Hit Points'] <= 0:
            if min_spent is None or spent < min_spent:
                min_spent = spent
                continue
        # let the player or the boss take a turn
        if up == 'player':
            # cast a spell
            #spell_try = Try.popleft()
            for spell in Spell.values():
                if (any(spell[0] == effect[0] and \
                effect[3] > 0 for effect in Effect_Next)):
                    continue
                player_next = deepcopy(player)
                boss_next = deepcopy(boss)
                player_next['Mana'] -= spell[0]
                if player_next['Mana'] < 0:
                    continue
                spent_next = spent + spell[0]
                if min_spent is not None and spent_next > min_spent:
                    continue
                if spell[1] > 0:
                    boss_next['Hit Points'] -= max(1, spell[1])
                player_next['Hit Points'] += spell[2]
                if boss_next['Hit Points'] <= 0:
                    if min_spent is None or spent_next < min_spent:
                        min_spent = spent_next
                else:
                    Q_Player.append(player_next)
                    Q_Boss.append(boss_next)
                    Q_Up.append('boss')
                    if spell[3] > 0:
                        Q_Effect.append(deepcopy(Effect_Next) + [list(spell)])
                    else:
                        Q_Effect.append(deepcopy(Effect_Next))
                    Q_Spent.append(spent_next)
        elif up == 'boss':
            player['Hit Points'] -= max(1, boss['Damage'] - player['Armor'])
            if player['Hit Points'] > 0:
                Q_Player.append(player)
                Q_Boss.append(boss)
                Q_Up.append('player')
                Q_Effect.append(Effect_Next)
                Q_Spent.append(spent)
        else:
            assert False
    return min_spent

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Boss = {}
for x in X:
    item, num = x.split(': ')
    Boss[item] = int(num)
Spell = {}
# (cost, instant_damage, instant_heal, 
# effect_turns, effect_armor, effect_damage, effect_mana)
Spell['Magic Missile'] = (53, 4, 0, 0, 0, 0, 0)
Spell['Drain'] = (73, 2, 2, 0, 0, 0, 0)
Spell['Shield'] = (113, 0, 0, 6, 7, 0, 0)
Spell['Poison'] = (173, 0, 0, 6, 0, 3, 0)
Spell['Recharge'] = (229, 0, 0, 5, 0, 0, 101)

# part 1
Player = {'Hit Points': 50, 'Armor': 0, 'Mana': 500}
ans1 = fight(Player, Boss)
print(ans1)

# part 2
Player = {'Hit Points': 50, 'Armor': 0, 'Mana': 500}
ans2 = fight(Player, Boss, hard = True)
print(ans2)
