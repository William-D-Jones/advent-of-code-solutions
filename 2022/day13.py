import sys

def get_order(pack1, pack2):
    i = 0
    while i < len(pack1) and i < len(pack2):
        if type(pack1[i]) is int and type(pack2[i]) is int:
            if pack1[i] < pack2[i]:
                return 1
            elif pack1[i] > pack2[i]:
                return -1
            else:
                i += 1
        elif type(pack1[i]) is list and type(pack2[i]) is int:
            order = get_order(pack1[i], [pack2[i]])
            if order == 0:
                i += 1
            else:
                return order
        elif type(pack1[i]) is int and type(pack2[i]) is list:
            order = get_order([pack1[i]], pack2[i])
            if order == 0:
                i += 1
            else:
                return order
        elif type(pack1[i]) is list and type(pack2[i]) is list:
            order = get_order(pack1[i], pack2[i])
            if order == 0:
                i += 1
            else:
                return order
        else:
            assert False
    if i == len(pack1) and i < len(pack2):
        return 1
    elif i < len(pack1) and i == len(pack2):
        return -1
    elif i == len(pack1) and i == len(pack2):
        return 0
    else:
        assert False

# parsing
X = [ list(l.strip()) for l in open(sys.argv[1], 'r') ]
Pack = [[]]
for x in X:
    if len(x) == 0:
        Pack.append([])
        continue
    pack = []
    depth = 0
    nums = ''
    for char in x:
        if char == '[':
            pack.append([])
            depth += 1
        elif char == ']' or char == ',':
            if nums != '':
                pack[-1].append(int(nums))
                nums = ''
            if char == ']':
                if depth > 1:
                    el = pack.pop()
                    pack[-1].append(el)
                depth -= 1
        elif char in '0123456789':
            nums += char
        else:
            assert False
    Pack[-1].append(pack.pop())

# part 1
ans1 = 0
for i, (pack1,pack2) in enumerate(Pack):
    order = get_order(pack1, pack2)
    if order == 1:
        ans1 += i+1
print(ans1)

# part 2
# collect all the packets in unsorted order
div1 = [[2]]
div2 = [[6]]
U = [div1, div2]
for packs in Pack:
    U += packs
# sort the packets
S = []
for pack2 in U:
    placed = False
    for i,pack1 in enumerate(S):
        order = get_order(pack1, pack2)
        if order == 1:
            continue
        elif order == -1:
            S = S[:i] + [pack2] + S[i:]
            placed = True
            break
        else:
            assert False
    if not placed:
        S.append(pack2)
# find the dividers
ans2 = 1
for i,pack in enumerate(S):
    if pack == div1 or pack == div2:
        ans2 *= i+1
print(ans2)

