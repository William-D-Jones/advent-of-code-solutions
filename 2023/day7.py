import sys
# import math
# from copy import deepcopy
# from collections import defaultdict
# import re

def card2val(card):
    for i in range(len(CARDS)):
        if CARDS[i:i+1] == card:
            return i
def hand2dict(hand):
    hdict = {}
    for i in range(len(CARDS)):
        card = CARDS[i:i+1]
        hdict[card] = hand.count(card)
    return hdict
def hand2classJ(hand):
    """
    five of a kind: 6
    four of a kind: 5
    full house: 4
    three of a kind: 3
    two pair: 2
    one pair: 1
    high card: 0
    """
    d = hand2dict(hand)
    J = d['J']
    Val = list(d.values())
    sortVal = sorted(Val,reverse = True)
    if sortVal[0] == 5:
        return 6
    elif sortVal[0] == 4:
        if J > 0:
            return 6
        else:
            return 5
    elif sortVal[0] == 3 and sortVal[1] == 2:
        if J > 0:
            return 6
        else:
            return 4
    elif sortVal[0] == 3 and sortVal[1] < 2:
        if J > 0:
            return 5
        else:
            return 3
    elif sortVal[0] == 2 and sortVal[1] == 2:
        if J == 2:
            return 5
        if J == 1:
            return 4
        else:
            return 2
    elif sortVal[0] == 2 and sortVal[1] < 2:
        if J > 0:
            return 3
        else:
            return 1
    else:
        if J > 0:
            return 1
        else:
            return 0
def hand2class(hand):
    """
    five of a kind: 6
    four of a kind: 5
    full house: 4
    three of a kind: 3
    two pair: 2
    one pair: 1
    high card: 0
    """
    Val = list(hand2dict(hand).values())
    sortVal = sorted(Val,reverse = True)
    if sortVal[0] == 5:
        return 6
    elif sortVal[0] == 4:
        return 5
    elif sortVal[0] == 3 and sortVal[1] == 2:
        return 4
    elif sortVal[0] == 3 and sortVal[1] < 2:
        return 3
    elif sortVal[0] == 2 and sortVal[1] == 2:
        return 2
    elif sortVal[0] == 2 and sortVal[1] < 2:
        return 1
    else:
        return 0
def compare_hands(hand1, hand2):
    for i in range(len(hand1)):
        if card2val(hand1[i:i+1]) < card2val(hand2[i:i+1]):
            return False
        elif card2val(hand1[i:i+1]) > card2val(hand2[i:i+1]): 
            return True
    return False

X = [ l.strip() for l in open(sys.argv[1], 'r') ]

dbids = {}
for x in X:
    hand, bid = x.split()
    dbids[hand] = int(bid)

# part 1
CARDS = '23456789TJQKA'
dclass = {}
for hand in dbids.keys():
    if not(hand2class(hand) in dclass.keys()):
        dclass[hand2class(hand)] = []
    dclass[hand2class(hand)].append(hand)
AllHands = []
for cl in sorted(list(dclass.keys())):
    HandSort = []
    for hand in dclass[cl]:
        HandSort.append('')
    for hand1 in dclass[cl]:
        rank = 0
        for hand2 in dclass[cl]:
            if compare_hands(hand1, hand2):
                rank += 1
        HandSort[rank] = hand1
    AllHands = AllHands + HandSort
tot = 0
for i,hand in enumerate(AllHands):
    tot += (i + 1) * dbids[hand]
print(tot)

# part 2
CARDS = 'J23456789TQKA'
dclass = {}
for hand in dbids.keys():
    if not(hand2classJ(hand) in dclass.keys()):
        dclass[hand2classJ(hand)] = []
    dclass[hand2classJ(hand)].append(hand)
AllHands = []
for cl in sorted(list(dclass.keys())):
    HandSort = []
    for hand in dclass[cl]:
        HandSort.append('')
    for hand1 in dclass[cl]:
        rank = 0
        for hand2 in dclass[cl]:
            if compare_hands(hand1, hand2):
                rank += 1
        HandSort[rank] = hand1
    AllHands = AllHands + HandSort
tot = 0
for i,hand in enumerate(AllHands):
    tot += (i + 1) * dbids[hand]
print(tot)
 
