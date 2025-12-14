import sys
import itertools

D = [(0,1), (1,0), (0,-1), (-1,0)]

# parsing
X = [tuple(map(int,l.strip().split(','))) for l in open(sys.argv[1], 'r')]
assert all(X.count(x)==1 for x in X)

# part 1
A = {tuple(sorted([(c0,r0), (c1,r1)])): (abs(c0-c1)+1) * (abs(r0-r1)+1) for \
(c0,r0), (c1,r1) in itertools.combinations(X, 2)}
ans1 = max(A.values())
print(ans1)

# part 2

# First, get some useful information regarding the shape.
# find the extrema of the shape
r_min = min(r for (c,r) in X)
r_max = max(r for (c,r) in X)
c_min = min(c for (c,r) in X)
c_max = max(c for (c,r) in X)
# find all the sides of the shape
S = [tuple(sorted( [X[i],X[(i+1)%len(X)]] )) for i in range(len(X))]
# find all the row-wise sides of the shape
SR = [((c0,r0),(c1,r1)) for ((c0,r0),(c1,r1)) in S if abs(r0-r1)>0 and c0-c1==0]
# find all the column-wise sides of the shape
SC = [((c0,r0),(c1,r1)) for ((c0,r0),(c1,r1)) in S if abs(c0-c1)>0 and r0-r1==0]

# Second, walk around the perimeter of the shape, looking in the clockwise and
# counterclockwise directions to identify the exterior and interior.
out = None
Out = {tuple(sorted([X[i],X[(i+1)%len(X)]])): None for i in range(len(X))}
i = -1
while any(val is None for val in Out.values()):
    i = (i+1) % len(X)
    c0,r0 = X[i]
    c1,r1 = X[(i+1)%len(X)]
    r,c = r0,c0
    # determine the direction of the walk
    dr = (r1-r0) // abs(r1-r0) if r1-r0 != 0 else 0
    dc = (c1-c0) // abs(c1-c0) if c1-c0 != 0 else 0
    di = D.index( (dr,dc) )
    # determine the directions clockwise and counterclockwise
    dra,dca = D[(di + 1) % len(D)]
    drb,dcb = D[(di - 1) % len(D)]
    # check if an outside direction has been determined
    if out is not None:
        Out[tuple(sorted([(c0,r0),(c1,r1)]))] = \
        (dra,dca) if out==1 else (drb,dcb)
        continue
    # walk along the side length
    for n in range(max(abs(r1-r0), abs(c1-c0)) + 1):
        nr = r + dr*n
        nc = c + dc*n
        # find the nearest sides parallel to the current side in each direction
        ii = 1 if dr!=0 else 0
        SP = SR if dr!=0 else SC
        SA = []
        SB = []
        for P0,P1 in SP:
            dp = P0[(ii+1)%2]-(nc,nr)[(ii+1)%2]
            if dp != 0:
                dp //= abs(dp)
            if dp != 0 and P0[ii]<=(nc,nr)[ii]<=P1[ii]:
                if (dca,dra)[(ii+1)%2] == dp:
                    SA.append( (P0,P1) )
                elif (dcb,drb)[(ii+1)%2] == dp:
                    SB.append( (P0,P1) )
        if len(SA)==0 and len(SB)>0:
            out = 1
            break
        elif len(SB)==0 and len(SA)>0:
            out = -1
            break

# Third, for each candidate rectangle, walk around the rectangle clockwise and
# determine if any point on the perimeter lies outside the shape. If any such
# point exists, reject the rectangle.
Accept = set()
Reject = set()
Seen = {}
Q = set(A.keys())
while Q:

    # setup the new rectangle
    (ac0,ar0),(ac1,ar1) = Q.pop()
    # construct the vertices of the test rectangle
    r_min_rect = min(ar0,ar1)
    r_max_rect = max(ar0,ar1)
    c_min_rect = min(ac0,ac1)
    c_max_rect = max(ac0,ac1)
    Rect_Vert = [ (c_min_rect,r_min_rect), (c_max_rect,r_min_rect), \
    (c_max_rect,r_max_rect), (c_min_rect,r_max_rect) ]
    # construct the sides of the test rectangle
    Rect_Side = [(Rect_Vert[i],Rect_Vert[(i+1)%len(Rect_Vert)]) for \
    i in range(len(Rect_Vert))]
    # sort the sides of the test rectangle
    Rect_Sort = [tuple(sorted(side)) for side in Rect_Side]

    # check the rectangle
    out = False
    # reject test rectangles with a side that is crossed by the shape
    for (tc0,tr0),(tc1,tr1) in Rect_Sort:
        if any( \
        (sc0<tc0<sc1 and sc0<tc1<sc1 and tr0<sr0<tr1 and tr0<sr1<tr1) or \
        (sr0<tr0<sr1 and sr0<tr1<sr1 and tc0<sc0<tc1 and tc0<sc1<tc1) for \
        (sc0,sr0),(sc1,sr1) in S ):
            out = True
            break
    # walk along the test rectangle, looking for points outside the shape
    i = -1
    while not out and i < len(Rect_Side)-1:
        i += 1
        # construct the side of the test rectangle
        (c0,r0),(c1,r1) = Rect_Side[i]
        (tc0,tr0),(tc1,tr1) = Rect_Sort[i]
        # walk along the side, searching for any points outside the shape
        # determine the direction of the walk
        dr = (r1-r0) // abs(r1-r0) if r1-r0 != 0 else 0
        dc = (c1-c0) // abs(c1-c0) if c1-c0 != 0 else 0
        if dr==0 and dc==0:
            continue
        di = D.index( (dr,dc) )
        # determine the directions clockwise and counterclockwise
        dra,dca = D[(di + 1) % len(D)]
        drb,dcb = D[(di - 1) % len(D)]
        # walk along the side length
        n = -1
        while n < max(abs(r1-r0), abs(c1-c0)):
            n += 1
            nr = r0 + dr*n
            nc = c0 + dc*n
            # if the point is on the perimeter, skip it
            skip = False
            for (sc0,sr0),(sc1,sr1) in S:
                if sc0<=nc<=sc1 and sr0<=nr<=sr1:
                    skip = True
                    if dr!=0 and abs(sr1-nr)>0 and (sr1-nr)//abs(sr1-nr)==dr:
                        n += abs(sr1-nr)
                        break
                    elif dr!=0 and abs(sr0-nr)>0 and (sr0-nr)//abs(sr0-nr)==dr:
                        n += abs(sr0-nr)
                        break
                    elif dc!=0 and abs(sc0-nc)>0 and (sc0-nc)//abs(sc0-nc)==dc:
                        n += abs(sc0-nc)
                        break
                    elif dc!=0 and abs(sc1-nc)>0 and (sc1-nc)//abs(sc1-nc)==dc:
                        n += abs(sc1-nc)
                        break
            if skip:
                continue
            # if the point has been seen, re-use the old result
            if (nr,nc,dr,dc) in Seen:
                out = Seen[(nr,nc,dr,dc)]
                continue
            # find nearest sides parallel to the current side in each direction
            ii = 1 if dr!=0 else 0
            SP = SR if dr!=0 else SC
            SA = []
            for P0,P1 in SP:
                dpn = P0[(ii+1)%2]-(nc,nr)[(ii+1)%2]
                if dpn != 0:
                    dp = dpn // abs(dpn)
                else:
                    dp = dpn
                DP = (0,-dp) if dr!=0 else (-dp,0)
                if P0[ii]<=(nc,nr)[ii]<=P1[ii]:
                    if (dca,dra)[(ii+1)%2] == dp or dp==0:
                        SA.append( (abs(dpn), DP, (P0,P1)) )
            SA = sorted(SA)
            # check if we are inside or outside the nearest sides
            if not SA or (SA[0][0] > 0 and Out[ SA[0][2] ] == SA[0][1]):
                out = True
                break
            if (nr,nc,dr,dc) not in Seen:
                Seen[(nr,nc,dr,dc)] = out
            # skip to the next point on the shape perimeter
            if not out:
                for (sc0,sr0),(sc1,sr1) in S:
                    if dr!=0 and abs(sr1-nr)>0 and (sr1-nr)//abs(sr1-nr)==dr:
                        n += abs(sr1-nr)
                        break
                    elif dr!=0 and abs(sr0-nr)>0 and (sr0-nr)//abs(sr0-nr)==dr:
                        n += abs(sr0-nr)
                        break
                    elif dc!=0 and abs(sc1-nc)>0 and (sc1-nc)//abs(sc1-nc)==dc:
                        n += abs(sc1-nc)
                        break
                    elif dc!=0 and abs(sc0-nc)>0 and (sc0-nc)//abs(sc0-nc)==dc:
                        n += abs(sc0-nc)
                        break
        Seen[(nr,nc,dr,dc)] = out

    # evaluate the rectangle
    if not out:
        # accept the current rectangle
        Accept.add( ((ac0,ar0),(ac1,ar1)) )
        # accept any rectangles that are enclosed by the current rectangle
        for (qc0,qr0),(qc1,qr1) in set(Q):
            if min(ac0,ac1)<=qc0<=max(ac0,ac1) and \
            min(ac0,ac1)<=qc1<=max(ac0,ac1) and \
            min(ar0,ar1)<=qr0<=max(ar0,ar1) and \
            min(ar0,ar1)<=qr1<=max(ar0,ar1):
                Q.remove( ((qc0,qr0),(qc1,qr1)) )
                Accept.add( ((qc0,qr0),(qc1,qr1)) )
    else:
        # reject the current rectangle
        Reject.add( ((ac0,ar0),(ac1,ar1)) )
        # reject any rectangles that enclose the current rectangle
        for (qc0,qr0),(qc1,qr1) in set(Q):
            if min(qc0,qc1)<=ac0<=max(qc0,qc1) and \
            min(qc0,qc1)<=ac1<=max(qc0,qc1) and \
            min(qr0,qr1)<=ar0<=max(qr0,qr1) and \
            min(qr0,qr1)<=ar1<=max(qr0,qr1):
                Q.remove( ((qc0,qr0),(qc1,qr1)) )
                Reject.add( ((qc0,qr0),(qc1,qr1)) )

# produce the final answer
ans2 = max(a for rect,a in A.items() if rect in Accept)
print(ans2)

