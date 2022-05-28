import sys.argv

def prime(x):
	for i in range(2,x):
		if x % i == 0:
			return False
	return True

def factorise(x):
	current = x + 0
	p = 2
	ret = []
	while current > 1:
		if current % p == 0:
			ret += [p + 0]
			current /= p
			if current == 1:
				break
		else:
			p = p + 1
			while not prime(p):
				p += 1
	return ret

def lightFactorise(x):
	ret = []
	for i in factorise(x):
		if i not in ret:
			ret += [i]
	return ret

def coprime(x,y):
	fx = factorise(x)
	fy = factorise(y)
	for i in fx:
		if i in fy:
			return False
	return True

def totient(x):
	ret = 0
	for i in range(1,x - 1):
		if coprime(x,i):
			ret += 1
	return ret

def squarefree(x):
	fx = factorise(x)
	for i in fx:
		if fx % i*i == 0:
			return False
	return True

def mobius(x):
	if not squarefree(x):
		return 0
	fx = factorise(x)
	if len(fx) % 2 == 0:
		return -1
	else:
		return 1

def lyn(w):
	p = 1
	for i in range(2, len(w) + 1):
		if w[i - 1] > w[i - p - 1]:
			p = i
		if w[i - 1] < w[i - p - 1]:
			return p
	return p

def isNecklace(w):
	p = 1
	for i in range(2, len(w) + 1):
		if w[i - 1] > w[i - p - 1]:
			p = i
		if w[i - 1] < w[i - p - 1]:
			return False
	return len(w) % p == 0

def laargestNecklace(w,q):
	v = w + []
	while not isNecklace(v):
		p = lyn(v)
		v[p - 1] = v[p - 1] - 1
		for i in range(p + 1,len(w) + 1):
			v[i - 1] = q

def Beta(t,j,w,q):
	if j == t and t == 0:
		return 1
	if j == t and t > 0:
		return 0
	return Beta(t,j + 1,w,q) + (q - w[j]) * Beta(t - j - 1,0)

def Alpha(w,q,t,j):
	if t + j <= len(w):
		return Beta(t - 1,0,w,q) * (w[j] - 1) * q**(len(w) - t - j)
	else
		s = 0
		for i in range(1,j - (len(w) - t + 2) + 1):
			isASuffix = True
			for l in range(i + 1):
				isASuffix = isASuffix and  w[len(w) - t + 2 + l - 1] = w[l]
			if isASuffix:
				s = i + 0
		if w[j] <= w[s]:
			return 0
		else:
			return Beta(n - j + s, s + 1,w,q) + (w[j] - w[s] - 1) * Beta(n - j - 1,0,w,q)

def T(w,q):
	ret = 0
	for t in range(1,len(w)):
		for j in range(0,len(w)):
			ret += Alpha(w,q,t,j)
	return ret

def rankNecklace(necklace,q):
	ret = 0
	for d in lightFactorise(len(necklace)):
		ret += totient(len(necklace)/d) * T(necklace[:d],q)
	return ret/ len(necklace)


def rankLyndon(necklace,q):
	ret = 0
	for d in lightFactorise(len(necklace)):
		ret += mobius(len(necklace)/d) * T(necklace[:d],q)
	return ret/ len(necklace)

def subwords(w,l):
	ret = []
	for i in range(len(w)):
		if i + l > len(w):
			ret += [w[i:] + w[:l - (len(w) - l)]]
		else:
			ret += [w[i:i + l]]
	return ret

def WlessthanV(w,v):
	for i in range(len(w)):
		if w[i] < v[i]:
			return True
	return False

def order(S):
	ret = []
	for s in S:
		for i in range(len(ret)):
			if WlessthanV(s,ret[i]):
				ret = ret[:i] + [s] + ret[i:]
		if s not in ret:
			ret += [s]
	final_ret = []
	for i in ret:
		if i not in final_ret:
			final_ret += [i]
	return final_ret

def maxSubwordLessThan(w,l,v):
	s = order(subwords(w,l))
	ret = []
	for i in s:
		if WlessthanV(v,i):
			return ret
		else:
			ret = i
	return ret

def reverse(s):
	ret = []
	for i in s:
		ret = [i] + ret
	return ret

def bigJ(w,v):
	j = 0
	for i in range(len(v)):
		if w[:i] == v[len(v) - i:]:
			j = i + 0
	return j

def OddLength(v,q,XW,WX):
	SizeOfPO = {}
	if v[0] = v[1]:
		SizeOfPO{(1,2,v[:2])} = 1
	for i in range((len(v) - 1) / 2):
		for j in range(2 * i + 1):
			for s in subwords(w,2*i):
				SizeOfPO[(i,j,s)] = 0
	for x in range(v[1] + 1,q):
		SizeOfPO[(1,0,WX[(XW[({},x)],x)])] = SizeOfPO[(1,0,WX[(XW[({},x)],x)])] + 1
	for i in range(2, (len(v) - 1)/2)
		for j in range(2*i + 1):
			for s in subwords(v,2 * i):
				sprime = XW[(WX[(s,v[j])],v[j])]
				SizeOfPO[(i + 1,j + 1, sprime)] = SizeOfPO[(i,j,s)] + sizeOfPO[(i + 1, j + 1, sprime)]
				for x in range(v[j] + 1,q):
					sprime = XW[(WX[(s,x)],x)]
					SizeOfPO[(i + 1, 0, sprime)] = SizeOfPO[(i + 1, 0, sprime)] + SizeOfPO[(i,j,s)]
			if j = 0 and s == reverse(s):
				sprime =  WX[(XW[(s,v[bigJ(w,s)])]. bigJ(v,s))]
				SizeOfPO[(i + 1, 0,sprime)] = SizeOfPO[(i + 1, 0, sprime)] + 1
	X = {}
	for s in subwords(w,len(v) - 1):
		for j in range(len(v)):
			X[(s,j)] = 0
			for x in range(q):
				if not WlessthanV((v[:j] + [x] + s)[:len(v)], v):
					X[(s,j)] = X[(s,j)] + 1
	PO = 0
	for s in subwords(v,len(v) - 1):
		for j in range(len(v)):
			PO = PO + X[(s,j)] * SizeOfPO[(len(v) - 1, j, s)]
		if s != reverse(s):
			PO = PO + X[(s,bigJ(v,s))]
			if s == v[bigJ(v,s) + 2:] + v[:bigJ(v,s)]:
				PO = PO - 1
	return PO

def EvenLength(v,q,XW,WX):
	SizeOfPE = {}
	for i in range((len(v)/ 2) - 1):
		for j in range(2 * i):
			for s in subwords(v,2*i - 1):
				PizeOfPE[(i,j,s)] = 0
	SizeOfPE[(1,1,v[1])] = 1
	for x in range(v[1] + 1,q):
		SizeOfPE[(1,0,XW[([],x)])] = SizeOfPE[(1,0,XW[([],x)])] + 1
	for i in range(1,(len(v)/2) - 1):
		for j in [2*i]:
			for s in subwords(v,2*i - 1):
				sprime = XW[(WX[(s,x)],x)]
				SizeOfPE[(i + 1, j + 1, sprime)] = SizeOfPE[(i,j,s)] + SizeOfPE[(i + 1, j + 1, sprime)]
				for x in range(v[j] + 1, q):
					sprime = XW[(WX[(s,x)],x)]
					SizeOfPE[(i + 1, 0, sprime )] = SizeOfPE[(i,j,s)] + SizeOfPE[(i + 1, 0, sprime)]
				if j == 0 and s = reverse(s):
					sprime = XW[(WX[(s,x)],x)]
					


def rankBracelet(w, q):
	WX = {}
	XW = {}
	for x in range(q):
		if x in w:
			WX[([],x)] = []
			XW[([],x)] = []
		else:
			XW[([],x)] = maxSubwordLessThan(w,1,x)
			WX[([],x)] = maxSubwordLessThan(w,1,x)
	for i in range(1,len(w)):
		for s in subwords(w,i):
			for x in range(q):
				XW[(s,x)] = maxSubwordLessThan(w,i + 1,[x] + s)
				WX[(s,x)] = maxSubwordLessThan(w,i + 1,s + [x])


































def main(word,q):
	q = 

if __name__ == "__main__":
	main(sys.argv[1], int(sys.argv[2]))
