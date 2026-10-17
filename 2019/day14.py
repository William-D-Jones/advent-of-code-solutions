import sys
import math
from collections import deque, Counter

def make_fuel(fuel, fractional = False):
    Total = Counter()
    Inventory = Counter()
    Make = deque([('FUEL', fuel)])
    while Make:
        # identify the next product to make
        prod, n_prod = Make.popleft()
        # determine the amount of product needed
        n_prod -= Inventory[prod]
        Inventory[prod] = 0
        if prod == 'ORE':
            Total[prod] += n_prod
            continue
        if not fractional:
            rep = math.ceil(n_prod / Quantity[prod])
        else:
            rep = n_prod / Quantity[prod]
        n_made = rep * Quantity[prod]
        Total[prod] += n_made
        Inventory[prod] += n_made - n_prod
        # determine the required reactants to make that product
        for reac, n_reac in Reactant[prod]:
            Make.append( (reac, n_reac * rep) )
    return Total['ORE']

# parsing
X = [tuple(l.strip().split(' => ')) for l in open(sys.argv[1], 'r')]
Reactant = {}
Quantity = {}
for str_react, str_prod in X:
    T_React = tuple(tuple(str_chem.split(' ')) for \
    str_chem in str_react.split(', '))
    L_Prod = [tuple(str_chem.split(' ')) for \
    str_chem in str_prod.split(', ')]
    assert len(T_React) >= 1
    assert len(L_Prod) == 1
    prod_quant, prod_name = L_Prod.pop()
    assert prod_name not in Reactant and prod_name not in Quantity
    Reactant[prod_name] = tuple((react, int(quant)) for quant, react in T_React)
    Quantity[prod_name] = int(prod_quant)
assert 'FUEL' in Reactant and 'FUEL' in Quantity
# find the maximum amount of each reactant consumed in any reaction
Ceiling = {}
for Consumed in Reactant.values():
    for chem, num in Consumed:
        if chem not in Ceiling:
            Ceiling[chem] = num
        Ceiling[chem] = max(Ceiling[chem], num)

# part 1
ans1 = make_fuel(1, fractional = False)
print(ans1)

# part 2
cargo = 1000000000000
lower = cargo // ans1
upper = int(cargo / make_fuel(1, fractional = True))
assert make_fuel(upper + 1, fractional = False) > cargo
fuel = (lower + upper) // 2
while not (make_fuel(fuel) <= cargo and make_fuel(fuel + 1) > cargo):
    if make_fuel(fuel) <= cargo:
        if lower == fuel:
            lower += 1
        else:
            lower = fuel
    else:
        upper = fuel
    fuel = (lower + upper) // 2
ans2 = fuel
print(ans2)
