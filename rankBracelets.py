
def subwords(w,i): # subowrds of w of length i in order
    setOfSubwords = []
    for t in range(len(w)):
        subword = None
        if t + i <= len(w):
            subword = w[t:t + i]
        else:
            subword = w[t:] + w[:(t + i) % len(w)]
        if subword not in setOfSubwords:
            for j in range(len(setOfSubwords)):
                if wIsSmallerThanv(subword,setOfSubwords[j]):
                    setOfSubwords = setOfSubwords[:j] + [subword] + setOfSubwords[j:]
        if subword not in setOfSubwords:
            setOfSubwords = setOfSubwords + [subword]
    return setOfSubwords

def BoundingSubword(v,w): # subword of w bounding v
    ret = None
    for s in setOfSubwords(w,len(v)):
        if wIsSmallerThanv(s,v):
            ret = s
        else:
            return ret
    return ret


def lyn(v): # length of the longest prefix of v that is a lyndon word
    ret = 1
    for i in range(1,len(v)):
        if v[i] < v[i - ret]:
            return ret
        elif v[i] > v[i - ret]:
            ret = i + 1
    return ret
        

def wordsEqual(w,v): # is w = v?
    if len(w) != len(v):
        return False
    for i in range(len(w)):
        if w[i] != v[i]:
            return False
    return True

def wIsSmallerThanv(w,v): # Is w smaller than v
    for i in range(len(w)):
        if w[i] < v[i]:
            return True
        elif w[i] > v[i]:
            return False
    return False

def reflect(w): # reflect w
    ret = []
    for x in w:
        ret = [x] + ret
    return ret

def rotate(w,i): # Rotate w by i
    return w[i:] + w[:i]

def smallestRotation(w): # Find the smallest rotation of w
    ret = w
    for i in range(len(w)):
        if wIsSmallerThanv(rotate(w,i), ret):
            ret = rotate(w,i)
    return ret

def BigJ(w,v): # Longest prefix of w that is a suffix of v
    for i in range(min(len(w),len(v))):
        if w[:i] != v[len(v) - i - 1:]:
            return i
    return min(len(w),len(v))

def isPalindromic(w): # Is w palindromic
    for i in range(len(w)):
        if w[i] != w[len(w) - i - 1]:
            return False
    return True

# GENERAL

def ComputeBoundingSubwords(w,q):
    XW = {}
    WX = {}
    for x in range(q):
        if x in w:
            XW[([],x)] = []
            WX[([],x)] = []
        else:
            XW[([],x)] = max([y for y in w if y < x])
            WX[([],x)] = max([y for y in w if y < x])
        for i in range(1,len(w) + 1)
            for s in subwords(w,i):
                XW[(s,x)] = None
                WX[(s,x)] = None
    # Compute XW and WX
    for i in range(len(w)):
        for s in subwords(w,i):
            for x in range(q):
                XW[(s,x)] = None
                for sprime in subwords(w,i + 1):
                    if wIsLessThanv(sprime, [x] + s):
                        XW[(s,x)] = sprime
                    if wIsLessThanv(sprime, s + [x]):
                        WX[(s,x)] = sprime
    return XW,WX

# PALINDROMIC

def rankOdd(v,q,XW,WX):
    SizeOfPO = {}
    # Initialise SizeOfPO
    for i in range((len(w) - 1)/ 2 + 1):
        for j in range(2 * i + 1):
            for s in subwords(v,2*i):
                SizeOfPO[(i,j,s)] = 0
    # Compute SizeOfPO
    if v[0] == v[1]:
        SizeOfPO[(1,2,v[:2])] = 1
    for x in range(v[0] + 1,q):
        SizeOfPO[(1,0,WX[(XW[([], x)],x)])] = SizeOfPO[(1,0,WX[(XW[([], x)],x)])] + 1
    for i in range((len(w) - 1)/ 2 + 1):
        for j in range(2 * i + 1):
            for s in subwords(v,2*i):
                sprime = XW[(WX[(s,v[j])],v[j])]
                SizeOfPO[(i+1,j+1,sprime)] = SizeOfPO[(i+1,j+1,sprime)] + SizeOfPO[(i,j,s)]
                for x in range(v[j] + 1,q):
                    sprime = XW[(WX[(s,x)],x)]
                    SizeOfPO[(i + 1, 0, sprime)] = SizeOfPO[(i + 1, 0, sprime)] + SizeOfPO[(i,j,s)]
                if j == 0 and isPalindromic(s):
                    J = BigJ(w,v)
                    sprime = WX[(XW[(s,v[BigJ(w,s)])], BigJ(w,s))]
                    SizeOfPO[(i + 1, J + 1, sprime)] =  SizeOfPO[(i + 1, J + 1, sprime)] + 1
                    for x in range(v[J] + 1,q):
                        sprime = WX[( XW[( s, x)], x)]
                        SizeOfPO[(i + 1,0, sprime)] = SizeOfPO[(i + 1, 0, sprime)] + SizeOfPO[(i,j,s)]
    SizeOfX = {}
    for j in range(len(v)):
        for s in subwords(v, len(v) - 1):
            SizeOfX[(j,s)] = 0
            for x in range(q):
                if wIsSmallerThanv(v,v[:j] + [x] + s) or wordsEqual(v,v[:j] + [x] + s):
                    SizeOfX[(j,s)] = SizeOfX[(j,s)] + 1
    TotalOdd = 0
    for s in subwords(v,len(v) - 1):
        for j in range(len(v)):
            TotalOdd = TotalOdd + SizeOfX[(j,s)] * SizeOfPO[((len(v) - 1)/2, j, s)]
        J = BigJ(v,s)
        if (not wordsEqual(s, v[J + 2, n + j])) and isPalindromic(s):
            TotalOdd = TotalOdd + SizeOfX[(J,s)]
        elif wordsEqual(s, v[J + 2, n + j]) and isPalindromic(s):
            TotalOdd = TotalOdd + SizeOfX[(J,s)] - 1
    return TotalOdd

def rankEven(v,q,XW,WX):
    SizeOfPE = {}
    # Initialise SizeOfPE
    for i in range(len(v)/2):
        for j in range(2 * i):
            for s in subwords(v, 2 * i - 1):
                SizeOfPE[(i,j,s)] = 0
    # Compute SizeOfPE
    for x in range(v[0] + 1,q + 1):
        SizeOfPE[(1,0,(XW[([],x))])] = SizeOfPE[(1,0,(XW[[],x)])] + 1
    for i in range(1,len(v)/2):
        for j in range(2*i):
            for s in subwords(v,2*i - 1):
                sprime = XW[(WX[(s,v[j])],v[j])]
                SizeOfPE[(i + 1, j + 1, sprime)] = SizeOfPE[(i + 1, j + 1, sprime)] + SizeOfPE[(i, j, s)]
                for x in range(v[j] + 1, q):
                    sprime = WX[(WX[(s,x)],x)]
                    SizeOfPE[(i + 1, 0, sprime)] = SizeOfPE[(i + 1, 0, sprime)] + SizeOfPE[(i, j, s)]
                if j == 0 and isPalindromic(s):
                    J = BigJ(v,s)
                    sprime = WX[(XW[(s,v[J])],v[J])]
                    SizeOfPE[i + 1,J,sprime] = SizeOfPE[i + 1,J,sprime] + 1
                    for x in range(v[J] + 1, q):
                    sprime = WX[(WX[(s,x)],x)]
                    SizeOfPE[i + 1, 0, sprime] = SizeOfPE[i + 1, 0, sprime] + 1
    TotalEven = 0
    for s in subwords(v, len(v) - 1):
        if isPalindromic(s):
            J = BigJ(v,s)
            for x in range(v[J], q):
                if wIsSmallerThanv(v,smallestRotation(s + [x])):
                    TotalEven = TotalEven + 1
    for j in range(len(v) - 1):
        for s in subwords(v,len(v) - 1):
            for x in range(v[j], q):
                if wIsSmallerThanv(v, v[:j] + [x] + s) and not wordsEqual(v, v[:j] + [x] + s):
                    TotalEven = TotalEven + SizeOfPE[(len(v)/2 - 1, j, s)]
    return TotalEven

def rankSymmetric(v,q,XW,WX):
    SizeOfPS = {}
    # Initialise SizeOfPS
    for i in range(len(v)/2):
        for j in range(2 * i + 1):
            for s in subwords(v, 2 * i):
                SizeOfPS[(i,j,s)] = 0
    # Compute SizeOfPS
    if v[0] == v[1]:
        SizeOfPS[(1,2,v[:2])] = 1
    for x in range(v[0] + 1,q):
        sprime = WX[ ( XW[ ( [], x) ] ) ]
        SizeOfPS[(1,0,sprime)] = SizeOfPS[(1,0,sprime)] + 1
    for i in range(2,len(v)/2):
        for j in range(2 * i + 1):
            for s in subwords(v, 2 * i):
                sprime = XW[(WX[(s,v[j])],v[j])]
                SizeOfPS[(i + 1, j + 1, sprime)] = SizeOfPS[(i,j,s)] + SizeOfPS[(i + 1, j + 1, sprime)]
                for x in range(v[j] + 1, q):
                    sprime = WX[(WX[(s,x)],x)]
                    SizeOfPS[(i + 1, 0, sprime)] = SizeOfPS[(i + 1, 0, sprime)] + SizeOfPS[(i, j, s)]
                if j == 0 and isPalindromic(s):
                    J = BigJ(v,s)
                    sprime = WX[(XW[(s,v[J])],v[J])]
                    SizeOfPS[(i + 1, J + 1, sprime)] = SizeOfPS[(i + 1, J + 1, sprime)] + 1
    TotalSymetric = 0
    for s in subwords(v, len(v) - 2):
        if isPalincromic(s):
            J = BigJ(v,s)
            for x in range(v[J], q):
                if wIsSmallerThanv(v,smallestRotation(s + [x,x])):
                    TotalSymetric = TotalSymetric + 1
    for j in range(len(v) - 2):
        for s in subwords(v, len(v) - 2):
            for x in range(v[j], q):
                if wIsSmallerThanv(v,v[:j] + [x,x] + s):
                    TotalSymetric = TotalSymetric + 1
    return TotalSymetric

# ENCLOSING

def rankEnclosing(v,q,XW,WX):
    SizeOfSE = {}
    # Initialise SizeOfSE
    for i in range(len(v) + 1):
        for x in range(q):
            for j in range(len(v) + 1):
                for t in range(len(v)):
                    for s in subwords(v,t):
                        SizeOfSE[(i,x,j,s)] = 0
    # Compute SizeOfSE
    for i in range(1,len(v) + 1):
        for x in range(q):
            for j in range(len(v) + 1):
                for s in subwords(v, len(v) - 1):
                    for z in range(q):
                        if z >= ( v[:i] + [x])[(j + 1) % (i + 1)] and wIsSmallerThanv(v, [x] + s):
                            SizeOfSE[(i,x,j,s)] = SizeOfSE[(i,x,j,s)] + 1
    for i in range(1,len(v)+1):
        for x in range(q):
            for j in range(len(v) + 1):
                for t in range(len(v)):
                    for s in subwords(v,t):
                        for z in range(v[j], q):
                            jprime = 0
                            if z == v[j]:
                                jprime = j + 1
                            sprime = XW[(s,z)]
                            SizeOfSE[(x,i,jprime,sprime)] = SizeOfSE[(x,i,jprime,sprime)] + SizeOfSE[(x,i,j,s)]
    TotalEnclosing = 0
    for i in range(1,len(v)):
        L = lyn(v[:i])
        for x in range(q):
            if not wIsSmallerThanv([x] + reflect(v[:i]), v):
                if v[i] >= x and x > v[i % l]:
                    s = BoundingSubword([x] + reflect(v[:j]),v)
                    TotalEnclosing = TotalEnclosing + SizeOfSE[(x,i,j,s)]
    return TotalEnclosing

def GE(w,q,XW,WX):
    totalEven = rankEven(w,q,XW,WX)
    if (len(w) / 2) % 2 == 1:
        totalEven = totalEven + rankOdd(w[:len(w) / 2],q,XW,WX)
    else:
        totalEven = totalEven + GE(w[:len(w) / 2],q,XW,WX)
    return totalEven / 2

def GS(w,q,XW,WX):
    totalSymetric = rankSymmetric(w,q,XW,WX)
    if (len(w) / 2) % 2 == 1:
        totalSymetric = totalSymetric + rankOdd(w[:len(w) / 2],q,XW,WX)
    else:
        totalSymetric = totalSymetric + GS(w[:len(w) / 2],q,XW,WX)
    return totalSymetric / 2
        

def rankPalindromic(w,q,XW,WX):
    if len(w) % 2 == 1:
        return q**((len(w) - 1)/2) - rankOdd(w,q,XW,WX)
    else:
        l = 0
        if (len(w)/2) % 2 == 1:
            l = (len(w) + 2) / 4
        else:
            l = len(w) / 4
        totalNecklaces = (((q**((len(w)/2) + 1)) + 2*(q**(len(w) / 2)) + (q**l))/2) - q
        totalEven = GE(w,q,XW,WX)
        totalSymetric = GS(w,q,XW,WX)
    return totalNecklaces - (totalEven + totalSymetric)

def rankNecklace(w,q):
    return None

def rankBracelet(w,q): # Return the rank of w amongst the set of q-ary bracelets of the same length as w
    XW , WX = ComputeBoundingSubwords(w,q)
    return (rankNecklace(w,q) + rankPalindromic(w,q,XW,WX) + rankEnclosing(w,q,XW,WX))/2































































