import sys

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]

# part 1
num_code_tot = 0
num_mem_tot = 0
for x in X:
    num_code = len(x)
    num_mem = 0
    escape = False
    i = 0
    while i < len(x):
        char = x[i:i+1]
        if char == '\\':
            if escape:
                num_mem += 1
                escape = False
            else:
                escape = True
        elif char == '"':
            if escape:
                num_mem += 1
                escape = False
            else:
                pass
        elif char == 'x' and escape:
            num_mem += 1
            escape = False
            i += 2
        else:
            num_mem += 1
        i += 1
    num_code_tot += num_code
    num_mem_tot += num_mem
ans1 = num_code_tot - num_mem_tot
print(ans1)

# part 2
num_code_tot = 0
num_mem_tot = 0
for x in X:
    num_mem = len(x)
    num_code = 2
    i = 0
    while i < len(x):
        char = x[i:i+1]
        if char == '\\':
            num_code += 2
        elif char == '"':
            num_code += 2
        else:
            num_code += 1
        i += 1
    num_code_tot += num_code
    num_mem_tot += num_mem
ans2 = num_code_tot - num_mem_tot
print(ans2)
