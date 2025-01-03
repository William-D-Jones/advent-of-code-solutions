import sys
from copy import deepcopy
from collections import Counter

# parsing
X = [int(l) for l in open(sys.argv[1], 'r')]

# part 1
Ans1 = []
for num in X:
    for _ in range(2000):
        res1 = ( (num * 64) ^ num ) % 16777216
        res2 = ( (res1 // 32) ^ res1 ) % 16777216
        res3 = ( (res2 * 2048) ^ res2 ) % 16777216
        num = res3
    Ans1.append(num)
print(sum(Ans1))

# part 2
Number_of_Bananas = Counter()
for i,secret in enumerate(X):
    Diff = []
    Seen = set()
    for _ in range(2000): #2000
        # compute the next secret number
        res1 = ( (secret * 64) ^ secret) % 16777216
        res2 = ( (res1 // 32) ^ res1 ) % 16777216
        res3 = ( (res2 * 2048) ^ res2 ) % 16777216
        # compute the difference in the ones place
        price = res3 % 10 #int( str(res3)[-1] )
        last_price = secret % 10 #int( str(secret)[-1] )
        Diff.append(price - last_price)
        # calculate the sequence
        if len(Diff) >= 4:
            diff_sequence = tuple(Diff[-4:])
            if diff_sequence not in Seen:
                Number_of_Bananas[diff_sequence] += price
                Seen.add(diff_sequence)
        # reset for the next secret number
        secret = res3
# calculate the best sequence
max_bananas = 0
max_key = None
for key in Number_of_Bananas.keys():
    if Number_of_Bananas[key] > max_bananas:
        max_bananas = Number_of_Bananas[key]
        max_key = key
print(max_bananas)
