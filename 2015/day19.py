import sys
from collections import deque

a = ord('a')
z = ord('z')
A = ord('A')
Z = ord('Z')

def mol2atoms(Mol):
    s = ''
    atom = ''
    Mol_Spl = []
    for i in range(len(Mol)):
        char = Mol[i:i+1]
        if A<=ord(char)<=Z:
            if len(s) > 0:
                Mol_Spl.append(s)
                s = ''
        s += char
        if i == len(Mol)-1:
            Mol_Spl.append(s)
    return Mol_Spl

def nm_extract(Mol, atom_nm_first, atom_nm_2, atom_nm_middle, atom_nm_last):
    """
    Extract the first complete section of a molecule (from the left) that was
    generated from a single operation that generates non-modifiable atoms.
    """
    i0 = 0
    i1 = len(Mol)
    point = 0
    adj = 1
    Stop = set([atom_nm_last, atom_nm_first])
    while True:
        atom = Mol[point]
        if atom in Stop and adj == -1:
            if atom == atom_nm_2 or atom == atom_nm_middle:
                i0 = point+2
            else:
                i0 = point+1
            break
        if atom == atom_nm_last and adj == 1:
            i1 = point+1
            adj = -1
        if atom == atom_nm_2 and adj == -1:
            Stop.add(atom_nm_2)
            Stop.add(atom_nm_middle)
        point += adj
        if point < 0:
            i0 = 0
            break
    return Mol[i0:i1], i0, i1

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
X0, X1 = '\n'.join(X).split('\n\n')
Rep = {}
for x in X0.split('\n'):
    mol_in, mol_out = x.split(' => ')
    if mol_in not in Rep.keys():
        Rep[mol_in] = []
    Rep[mol_in].append(mol2atoms(mol_out))
Mol = mol2atoms(X1)
Rep_Inv = {}
for key, Val in Rep.items():
    for val in Val:
        Rep_Inv[tuple(val)] = key

# part 1
Mol_Rep_1 = set()
for i, atom in enumerate(Mol):
    if atom in Rep.keys():
        for rep in Rep[atom]:
            Mol_Rep_1.add( ''.join(Mol[:i] + rep + Mol[i+1:]) )
ans1 = len(Mol_Rep_1)
print(ans1)

# part 2

# I made the following observations about the problem:

# (1) Some atoms cannot be further modified once they are inserted
Atoms_In = set(list(Rep.keys()))
Atoms_Out = set()
for Out in Rep.values():
    for atoms_out in Out:
        Atoms_Out |= set(atoms_out)
Atoms_End = Atoms_Out - Atoms_In

# (2) Only certain operations can insert non-modifiable atoms, and these 
# operations insert non-modifiable atoms in a particular configuration. Here
# we define four non-modifiable atoms:
# atom_nm_first: the only non-modifiable atom which starts a replacement. If
#       present, it must be the first atom in the replacement.
# atom_nm_2: the second atom in every replacement, occuring always and only
#       in the second position.
# atom_nm_middle: the only non-modifiable atom that occur more than once. If
#       it occurs, it occurs at every 2nd atom after atom_nm_2 until 
#       atom_nm_final.
# atom_nm_last: the last atom in every replacement, occuring always and only
#       in the last position. It is an even number of atoms after atom_nm_2.
Final_Ops = []
Mod_Ops = []
for atom_in, Out in Rep.items():
    for atoms_out in Out:
        if len(set(atoms_out) & Atoms_End) > 0:
            Final_Ops.append(atoms_out)
        else:
            Mod_Ops.append(atoms_out)
atom_nm_first = list(set([op[0] for op in Final_Ops]) & Atoms_End)[0]
atom_nm_2 = Final_Ops[0][1]
atom_nm_last = Final_Ops[0][-1]
atom_nm_middle = \
list(Atoms_End - set([atom_nm_first, atom_nm_2, atom_nm_last]))[0]
assert(all(op[0] == atom_nm_first or \
atom_nm_first not in op for op in Final_Ops))
assert(all(op[1] == atom_nm_2 and op.count(atom_nm_2) == 1 for op in Final_Ops))
assert(all(op[-1] == atom_nm_last and \
op.count(atom_nm_last) == 1 for op in Final_Ops))

# (2a) We can use these rules to divide Final_Ops into groups.
Final_Ops_Grp = {'p': {}, '2': {}}
for op in Final_Ops:
    cnt = op.count(atom_nm_middle)
    if atom_nm_first in op:
        if cnt not in Final_Ops_Grp['p']:
            Final_Ops_Grp['p'][cnt] = []
        Final_Ops_Grp['p'][cnt].append(op)
    else:
        if cnt not in Final_Ops_Grp['2']:
            Final_Ops_Grp['2'][cnt] = []
        Final_Ops_Grp['2'][cnt].append(op)

# (2b) All the modifiable operations produce a replacement with length 2.
assert(all(len(op) == 2 for op in Mod_Ops))

# (3) The target molecule begins and ends with a non-modifiable atom.
assert(Mol[0] in Atoms_End and Mol[-1] in Atoms_End)

# To solve the problem, we will start on the left of the molecule and slide
# right, searching for atom_2 that is followed by atom_final, with no
# intervening atom_2 or atom_final. For each such sequence, determine which
# replacements in Final_Ops could have generated this 

ans2 = 0
while Mol:
    Ex, i0, i1 = \
    nm_extract(Mol, atom_nm_first, atom_nm_2, atom_nm_middle, atom_nm_last)
    # count the nonmodifiable operation
    ans2 += 1
    # count any modifiable operations within the nonmodifiable one
    num_middle = Ex.count(atom_nm_middle)
    op_len_pred = 4 + 2*num_middle
    ans2 += len(Ex) - op_len_pred
    Mol = Mol[:i0] + ['X'] + Mol[i1:]
    if len(Mol) == 2:
        ans2 += 1
        break
print(ans2)

