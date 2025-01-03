import sys

def ix_increment(ix_current, length, ix_exclude):
    """
    Systematically increments a set of indices, such that the resulting 
    indices are unique.
    
    ix_current: the list of indices to be incremented
    length: the length of the list to be indexed (in other words, the maximum
        allowed index + 1)
    ix_exclude: a list of indices that must be skipped

    Returns an incremented list of indices, or None if the indices cannot
    be incremented within the allowed criteria.
    """

    if len(ix_current) > 0:
        increment = len(ix_current) - 1
        # find and increment the appropriate index to avoid overflow
        while ix_current[increment] + 1 >= \
        length + 1 - len(ix_current) + increment:
            if increment < 1:
                return None
            increment -= 1
        # implement the increments
        ix_current[increment] += 1
        for j in range(increment + 1, len(ix_current)):
            ix_current[j] = ix_current[j - 1] + 1
        if any(ix in ix_exclude for ix in ix_current):
            return ix_increment(ix_current, length, ix_exclude)
        else:
            return ix_current
    else:
        return None

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Result = []
Input = []
for x in X:
    str_result, str_input = x.split(': ')
    Result.append(int(str_result))
    Input.append(list(map(int, str_input.split())))

# part 1
ans1 = 0
Ops = []
for i,Vals in enumerate(Input):
    poss = False
    Ops.append([])
    for num_mul in range(len(Vals)):
        Mul = [i for i in range(num_mul)] # indices of multiplication
        overflow = False
        while not overflow:
            # produce the operations
            Ops[-1] = ['*' if i in Mul else '+' for i in range(len(Vals) - 1)]
            # compute and check the result
            res = Vals[0]
            for m,op in enumerate(Ops[-1]):
                if op == '+':
                    res += Vals[m+1]
                elif op == '*':
                    res *= Vals[m+1]
                else:
                    assert False
            if res == Result[i]:
                poss = True
                break
            # increment the indices of multiplication
            if len(Mul) > 0:
                increment = len(Mul) - 1
                # find and increment the appropriate index to avoid overflow
                while Mul[increment] + 1 >= len(Vals) - len(Mul) + increment:
                    if increment < 1:
                        overflow = True
                        break
                    increment -= 1
                # implement the increments
                if not overflow:
                    Mul[increment] += 1
                    for j in range(increment + 1, len(Mul)):
                        Mul[j] = Mul[j - 1] + 1
            else:
                overflow = True
        if poss:
            break
    if poss:
        ans1 += Result[i]
print(ans1)

# part 2
ans2 = 0
Ops = []
for i,Vals in enumerate(Input):
    poss = False
    Ops.append([])
    for num_mul in range(len(Vals)):
        Mul = [i for i in range(num_mul)] # indices of multiplication
        overflowM = False
        while not overflowM:
            for num_cat in range(len(Vals) - num_mul):
                overflow = False
                Cat = [i for i in range(num_cat)]
                if any(ix in Mul for ix in Cat):
                    Cat = ix_increment(Cat, len(Vals) - 1, Mul)
                if Cat == None:
                    break
                    overflow = True
                while not overflow:
                    # produce the operations
                    Ops[-1] = []
                    for j in range(len(Vals) - 1):
                        if j in Mul:
                            Ops[-1].append('*')
                        elif j in Cat:
                            Ops[-1].append('||')
                        else:
                            Ops[-1].append('+')
                    # compute and check the result
                    res = Vals[0]
                    for m,op in enumerate(Ops[-1]):
                        if op == '+':
                            res += Vals[m+1]
                        elif op == '*':
                            res *= Vals[m+1]
                        elif op == '||':
                            res = int(''.join([str(res), str(Vals[m+1])]))
                        else:
                            assert False
                    if res == Result[i]:
                        poss = True
                        break
                    Cat = ix_increment(Cat, len(Vals) - 1, Mul)
                    if Cat is None:
                        overflow = True
                        break
                if poss:
                    break
            if poss:
                break
            # increment the indices of multiplication
            Mul = ix_increment(Mul, len(Vals) - 1, [])
            if Mul is None:
                overflowM = True
                continue
        if poss:
            break
    if poss:
        ans2 += Result[i]
print(ans2)
