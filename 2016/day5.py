import sys
import hashlib

# parsing
X = ''.join([ l.strip() for l in open(sys.argv[1], 'r') ])

# parts 1 and 2
num_char = 8
i = 0
Password1 = []
Password2 = [None for _ in range(num_char)]
while len(Password1) < num_char or any(char is None for char in Password2):
    hash_in = X + str(i)
    hash_out = hashlib.md5(hash_in.encode()).hexdigest()
    if hash_out[0:5] == '00000':
        if len(Password1) < num_char:
            Password1.append(hash_out[5:6])
        if hash_out[5:6] in '0123456789':
            ix = int(hash_out[5:6])
            if 0<=ix<len(Password2) and Password2[ ix ] is None:
                Password2[ ix ] = hash_out[6:7]
    i += 1
ans1 = ''.join(Password1)
print(ans1)
ans2 = ''.join(Password2)
print(ans2)

