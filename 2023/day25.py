import sys
from collections import deque

def trace_paths(Wires, Grp1, test):
    """
    Trace the independent paths between a group of components and a test
    component.

    Wires: the dictionary of wires (each key is a component and each value the
        set of components connected to the key
    Grp1: the set of components in group 1
    test: the component to be tested

    Returns the list of independent paths.
    """

    Path = deque([test])
    Path_Connections = deque([set()])
    Seen_Components = set([test]) # the components we have seen
    Seen_Connections = set() # the connections we have seen
    Ind = [] # the list of independent paths
    Ind_Connections = set()
    while Path:
        src = Path.popleft()
        con = Path_Connections.popleft()
        for tar in Wires[src]:
            # assemble the connection
            con_next = tuple(sorted( [src,tar] ))
            # check if the component or connection has been seen
            if (tar in Seen_Components and tar not in Grp1) or \
            con_next in Seen_Connections or \
            con_next in Ind_Connections or \
            any(c in Ind_Connections for c in con):
                continue
            # record the new component and connection
            Seen_Components.add(tar)
            Seen_Connections.add(con_next)
            # check if we have reached the group
            if tar in Grp1:
                ind = con | set([con_next])
                Ind.append(ind)
                Ind_Connections |= ind
                continue
            # if we have not reached the group, continue the path
            Path.append(tar)
            Path_Connections.append( con | set([con_next]) )
            #print('The paths are:')
            #print(Path)
            #print('The connections are:')
            #print(Path_Connections)
            #print('The seen components are:')
            #print(Seen_Components)
            #print('The seen connections are:')
            #print(Seen_Connections)
            #print('The independent connections are:')
            #print(Ind)
            #print('\n')
    return Ind

# parsing
X = [ l.strip() for l in open(sys.argv[1], 'r') ]
Wires = {}
for x in X:
    src, xtar = x.split(': ')
    Tar = xtar.split(' ')
    if src not in Wires.keys():
        Wires[src] = set()
    for tar in Tar:
        Wires[src].add(tar)
        if tar not in Wires.keys():
            Wires[tar] = set()
        Wires[tar].add(src)

# part 1
Wires_to_Place = deque(Wires.keys())
# assign the first wire to group 1
Grp1 = set([Wires_to_Place.pop()])
num_tested = 0
num_to_place = len(Wires_to_Place)
while num_tested < num_to_place:
    test = Wires_to_Place.popleft()
    # find the independent connections between the test component and Grp1
    Trace = trace_paths(Wires, Grp1, test)
    # check if we would need to break more than 3 connections
    if len(Trace) > 3:
        # If we would need to break more than 3 connections to separate the
        # component from the provisional Grp1, then the component must belong
        # in Grp1
        Grp1.add(test)
        num_tested = 0
        num_to_place = len(Wires_to_Place)
    else:
        # otherwise, we need to keep testing
        Wires_to_Place.append(test)
        num_tested += 1
ans1 = len(Grp1) * ( len(Wires) - len(Grp1) )
print(ans1)
        
