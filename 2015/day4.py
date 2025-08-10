import sys
import hashlib

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ][0]

# part 1
ans1 = 0
hash_in = X + str(ans1)
hash_out = hashlib.md5(hash_in.encode()).hexdigest()
while hash_out[0:5] != '00000':
    ans1 += 1
    hash_in = X + str(ans1)
    hash_out = hashlib.md5(hash_in.encode()).hexdigest()
print(ans1)

# part 2
ans2 = ans1
hash_in = X + str(ans2)
hash_out = hashlib.md5(hash_in.encode()).hexdigest()
while hash_out[0:6] != '000000':
    ans2 += 1
    hash_in = X + str(ans2)
    hash_out = hashlib.md5(hash_in.encode()).hexdigest()
print(ans2)
