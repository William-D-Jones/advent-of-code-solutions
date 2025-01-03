import sys
from copy import deepcopy
from collections import defaultdict, Counter, deque

def run_wires(Signals, Gates):
    Signals = deepcopy(Signals)
    To_Do = deque(Gates.keys())
    while To_Do:
        key = To_Do.pop()
        in1, op, in2 = Gates[ key ]
        if in1 in Signals.keys() and in2 in Signals.keys():
            match op:
                case 'XOR':
                    Signals[ key ] = Signals[in1] ^ Signals[in2]
                case 'OR':
                    Signals[ key ] = Signals[in1] | Signals[in2]
                case 'AND':
                    Signals[ key ] = Signals[in1] & Signals[in2]
        else:
            To_Do.appendleft(key)
    return Signals

def add(bits, X, Y, Gates):
    Signals = Counter()
    for i in range(bits):
        name = '{:02}'.format(i)
        Signals['x'+name] = X[i]
        Signals['y'+name] = Y[i]
    Signals = run_wires(Signals, Gates)
    X = ''.join([ str( Signals['x'+'{:02}'.format(i)] ) \
    for i in reversed(range(bits)) ])
    Y = ''.join([ str( Signals['y'+'{:02}'.format(i)] ) \
    for i in reversed(range(bits)) ])
    Z = ''.join([ str( Signals['z'+'{:02}'.format(i)] ) \
    for i in reversed(range(bits+1)) ])
    ans = ('{0:0'+str(bits+1)+'b}').format( int(X,2)+int(Y,2) )
    return X, Y, Z, ans

# parsing
X = open(sys.argv[1], 'r').read().strip()
X1,X2 = X.split('\n\n')
# parse the X and Y inputs
Signals = Counter()
bits = 1
for x in X1.split('\n'):
    wire,signal = x.split()
    wire = wire[:-1]
    Signals[ wire ] = int(signal)
    if int(wire[1:]) > bits:
        bits = int(wire[1:]) + 1
# parse the gates
Gates = defaultdict(tuple)
for gate in X2.split('\n'):
    in1, op, in2, arrow, out = gate.split()
    Gates[ out ] = (in1, op, in2)

# part 1
# evaluate the wires
Signals1 = run_wires(Signals, Gates)
# get the z wires
Z = []
for i in reversed(range(bits+1)):
    name = 'z'+'{:02}'.format(i)
    Z.append(Signals1[name])
ans1 = int(''.join( map(str, Z) ), 2)
print(ans1)

# part 2
Switch = []
# invert the gates dictionary
iGates = { value:key for key,value in Gates.items() }
# check the base XOR inputs (no carry)
for i in range(bits):
    # produce the padded string version of this bit index
    ipad = '{:02}'.format(i)
    # test if non carry addition is correctly handled for this bit
    X_try = [ 1 if j == i else 0 for j in range(bits) ]
    Y_try = [ 0 for _ in range(bits) ]
    X, Y, Z, ans = add( bits, X_try, Y_try, Gates )
    if Z != ans:
        # (part A) trace the mismatch
        # (step 1) identify the input XOR gate and its signal
        gate_xor_in = ('x'+ipad, 'XOR', 'y'+ipad)
        gate_xor_in = gate_xor_in if gate_xor_in in iGates.keys() \
        else tuple(reversed(gate_xor_in))
        sig_xor_in = iGates[ gate_xor_in ]
        # (step 2) identify gate mapping to the output bit
        gate_z = Gates[ 'z'+ipad ]
        # (step 3) if the current bit is > 0, find the XOR gate containing the
        # signal from the input XOR gate
        gate_xor_out = None
        sig_xor_out = None
        for in1,op,in2 in iGates.keys():
            if ( in1==sig_xor_in or in2==sig_xor_in ) and op == 'XOR':
                gate_xor_out = (in1, op, in2)
                sig_xor_out = iGates[gate_xor_out]
        # (part B) identify and correct the mismatched pair
        if i==0:
            switch1 = sig_xor_in
            switch2 = 'z'+ipad
            Switch.append += [switch1,switch2]
            # fix the problem and check the result
            Gates[switch1], Gates[switch2] = Gates[switch2], Gates[switch1]
            iGates = { value:key for key,value in Gates.items() }
            X, Y, Z, ans = add( bits, X_try, Y_try, Gates )
            assert Z == ans
        else:
            if gate_xor_out is not None:
                assert gate_xor_out != gate_z
                switch1 = sig_xor_out
                switch2 = 'z'+ipad
                Switch += [switch1,switch2]
                # fix the problem and check the result
                Gates[switch1], Gates[switch2] = Gates[switch2], Gates[switch1]
                iGates = { value:key for key,value in Gates.items() }
                X, Y, Z, ans = add( bits, X_try, Y_try, Gates )
                assert Z == ans
            else:
                # since only a small number of wires are switched, we will
                # assume that Z is correctly mapped
                switch1 = sig_xor_in
                try2 = [ gate_z[0], gate_z[2] ]
                for switch2 in try2:
                    Gates[switch1], Gates[switch2] = \
                    Gates[switch2], Gates[switch1]
                    X, Y, Z, ans = add( bits, X_try, Y_try, Gates )
                    if Z == ans:
                        Switch += [switch1, switch2]
                        iGates = { value:key for key,value in Gates.items() }
                        break
                    else:
                        Gates[switch1], Gates[switch2] = \
                        Gates[switch2], Gates[switch1]
print(','.join(sorted(Switch)))

