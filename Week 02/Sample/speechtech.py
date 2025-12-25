'''Various functions for Speech Tech

Some of these require additional files as
indicated for each function.

Version: 1.2

Mike Hammond, U. of Arizona, 3/2019
'''

import math,re,sys,urllib.request
import numpy as np
import sounddevice as sd
import scipy.linalg as la
import scipy.signal as ss
import matplotlib.mlab as ml
import matplotlib.pyplot as plt
import random as r
import matplotlib.cm as cm
import numpy.matlib as nm
import pomegranate as p
import matplotlib.patches as mpatch
import python_speech_features as psf
from hmmlearn import hmm
from scipy.io import wavfile
from sklearn.cluster import KMeans
from sklearn.linear_model import Perceptron
import functools as f

#parabolic function
def _pb(f,x):
	xv = 1/2.0*(f[x-1]-f[x+1])/(f[x-1]-2*f[x]+f[x+1])+x
	yv = f[x]-1/4.0*(f[x-1]-f[x+1])*(xv-x)
	return xv,yv

def getpitch(sig,fs):
	'''calculate pitch from autocorrelation

	Args:
		sig: the wave
		fs:  sample rate

	Returns:
		pitch rate
	'''
	corr = ss.fftconvolve(sig,sig[::-1],mode='full')
	corr = corr[len(corr)//2:]
	d = np.diff(corr)
	start = ml.find(d > 0)[0]
	peak = np.argmax(corr[start:])+start
	px,py = _pb(corr,peak)
	return fs/px

#adapting from lpc2 in non-working scikits.talkbox
def lpc(signal,order):
	'''Linear Predictive coding

	Args:
		signal: the wave
		order:  order of the LPC

	Returns:
		the LPC
	'''
	#order must be an integer
	order = int(order)
	#signal must have just 1 dimension
	if signal.ndim > 1:
		raise ValueError("array rank > 1 not supported")
	#order can't exceed number of samples
	if order > signal.size:
		raise ValueError("signal length must be >= order")
	#do the math
	if order > 0:
		p = order + 1
		r = np.zeros(p,signal.dtype)
		nx = np.min([p,signal.size])
		x = np.correlate(signal,signal,'full')
		r[:nx] = x[signal.size-1:signal.size+order]
		#added first clause, 3/13/19
		if np.linalg.det(la.toeplitz(r[:-1])) == 0:
			phi = np.dot(np.linalg.pinv(la.toeplitz(r[:-1])),-r[1:])
		else:
			phi = np.dot(la.inv(la.toeplitz(r[:-1])),-r[1:])
		return np.concatenate(([1.],phi))
	else:
		return np.ones(1, dtype = signal.dtype)

def spec(y,Fs):
	'''Compute a spectrogram

	This does not display the spectrogram.

	Args:
		y:  the wave
		Fs: the sample rate

	Returns:
		m: magnitudes
		f: frequencies
	'''
	#Compute length of sound
	Ns = len(y)/Fs
	#Compute FFT
	x = np.fft.fft(y)
	#x = fft(y)
	#Get response until Fs/2
	x = x[:math.floor(Ns*Fs/2)]
	#return frequencies and magnitudes
	m = np.abs(x)
	f = np.arange(0,len(x)) * (Fs/2)/len(x)
	return m,f

def record(seconds=2):
	'''Record a wave

	Args:
		seconds: how many seconds

	Returns:
		rate: sample rate
		w2:   wave
	'''
	print("recording...")
	rate=44100
	wave = sd.rec(
		int(seconds * rate),
		samplerate=rate,
		channels=1,
		dtype='int16',
		blocking=True
	)
	print("finished recording")
	#convert matrix to array!
	w2 = np.squeeze(np.asarray(wave))
	return rate,w2

#same as matlab code
def psolapitchdemo(w,fs,shift):
	'''PSOLA pitch demo

	Args:
		w:	the wave
		fs	sample rate
		shift:	values between -1 and 1

	The last argument specifies how much of a pitch
	shift to perform.

	Returns:
		the new wave with altered pitch
	'''
	f0 = getpitch(w,fs)
	wavesize = math.ceil(fs/f0)
	newwave = np.zeros(len(w)*2)
	i = 0
	j = 1
	wmax = len(w) - wavesize
	while i < wmax:
		wxstart = (i + 1) - round(wavesize/2)
		if wxstart < 0: wxstart = 0
		wxend = wxstart + wavesize + round(wavesize/2)
		if wxend >= len(w): wxend = len(w) - 1
		win = w[wxstart:wxend]
		h = np.hanning(len(win))
		win2 = win * h
		w2end = j + (wxend-wxstart)
		newwave[j:w2end] = newwave[j:w2end] + win2
		i += wavesize
		j = j + round(wavesize+(shift*wavesize))
	newwave = newwave[:wxend]
	return newwave

def ed(s1,s2):
	'''Calculates edit distance between two strings

	Args:
		s1: first string
		s2: second string

	Returns:
		the edit distance
	'''
	n1 = len(s1)
	n2 = len(s2)
	mygrid = np.zeros([n1+1,n2+1])
	for i in range(n1):
		mygrid[i+1,0] = mygrid[i,0]+1
	for j in range(n2):
		mygrid[0,j+1] = mygrid[0,j]+1
	for i in range(n1):
		for j in range(n2):
			if s1[i] == s2[j]:
				r = 0
			else:
				r = 1
			mygrid[i+1,j+1] = min(
				[mygrid[i,j]+r,mygrid[i+1,j]+1,mygrid[i,j+1]+1]
			)
	d = mygrid[n1,n2]
	return d

def wlengthtrn(w,fs):
	'''Gets the length of a wave

	This is for the digits test set

	Args:
		w:  the wave
		fs: sample rate (not used)

	Returns:
		the length of the wave
	'''
	return len(w)

#length test function
def wlengthtst(w1,w2):
	'''compare the difference between the lengths of two waves

	This is for the digits test set

	Args:
		w1:	length of the first wave
		w2:	length of the second wave
	'''
	return abs(w1-w2)

def trn(d,subs,f):
	'''digits training function

	Uses some function to create a matrix of representations
	for the wave files in the digits dataset

	Args:
		d:	string rep of where digits files are
		subs:	number of subjects
		f:	training function

	Returns:
		a matrix of wave representations
	'''
	#names of individual files
	names = 'zero one two three four five six seven eight nine'
	names = names.split()
	#put results here
	allres = []
	for i in range(1,subs+1):
		currentres = []
		s = str(i)
		if len(s) == 1:
			s = '0' + s
		s = '/s' + s + '/'
		for i in range(len(names)):
			filename = d + s + names[i] + '.wav'
			fs,w = wavfile.read(filename)
			res = f(w,fs)
			currentres.append(res)
		allres.append(currentres)
	return allres

#checks if something is unique in a list
def _onlyinlist(x,ys):
	xfound = False
	xunique = True
	for y in ys:
		if x == y:
			if xfound:
				return False
			else:
				xfound = True
	return True

#general testing function
def tst(d,f):
	'''general testing function for digits dataset

	Applies a specified function to the wave
	representations produced by the trn()
	function and does a cross-validation test.

	This is inefficient and should be parallelized!

	Args:
		d:	matrix of wave file representations
		f:	testing function
	'''
	matches = 0
	subs = set(range(len(d)))
	total = 0
	#go through each subject
	for s in range(len(d)):
		therest = list(range(s+1,len(d)))
		#compare to all other subjects
		for t in therest:
			#do that comparison for each digit
			for i in range(10):
				#compare d[s][i] to d[t]
				current = []
				for x in d[t]:
					current.append(f(d[s][i],x))
				#THIS ISN'T RIGHT!
				if min(current) == current[i]:
					if _onlyinlist(min(current),current):
						matches += 1
				total += 1
	res = '{}/{} ({:1.4})'
	res = res.format(matches,total,matches/total)
	print(res)

def fbdemo(w,fs,n):
	'''Filterbank demo

	This takes a wave and displays a filterbank
	representation of the wave with a specified
	number of filterbanks.

	Args:
		w:	the wave
		fs:	sample rate
		n:	number of filterbanks to use
	'''
	m,ws = spec(w,fs)
	binsize = math.floor(len(m)/n)
	wnew = np.zeros(len(m))
	wvec = np.zeros(n)
	i = 0
	inum = 0
	while i+binsize < len(m):
		startpoint = i
		endpoint = i + binsize
		#get the mean value for the bank
		meanval = np.mean(m[startpoint:endpoint])
		#set corresponding new segment to that value
		wnew[startpoint:endpoint] = meanval
		#add mean to vector of means
		wvec[inum] = meanval
		i += binsize
		inum += 1
	#plot them both
	plt.subplot(2,1,1)
	plt.plot(ws,m)
	plt.subplot(2,1,2)
	plt.plot(wnew,'r')
	plt.show()

def filterbank(w,fs,winsize,banknum):
	'''filterbanks for trn() function

	Function to be used with trn() to create
	filterbank representations. Can be invoked
	in two ways.

	If winsize is a fraction less than 1, then
	every wave is divided into the same number
	of filterbanks.

	If winsize is a number greater than 1, then
	it specifies the number of milliseconds in
	each window.

	Args:
		w:		the wave
		fs:		sample rate
		winsize:	size of window
		banknum:	number of filterbanks
	'''
	if winsize > 1:
		winsamples = math.floor(fs * winsize * .001)
	else:
		winsamples = math.floor(len(w) * winsize)
	#total number of windows
	numwindows = math.floor(len(w)/winsamples)
	#create a matrix for the result
	res = np.zeros([banknum,numwindows])	
	i = 0
	inum = 0
	while i+winsamples < len(w):
		#get current window
		currentwin = w[i:(i+winsamples)]
		#calculate fft
		ns = len(currentwin)/fs
		x = np.fft.fft(currentwin)
		x = x[:math.floor(ns*fs/2)]
		currentfft = abs(x)
		#bin into banknum windows
		banksize = math.floor(len(currentfft)/banknum)
		j = 0
		jnum = 0
		while j+banksize < len(currentfft)+1:
			res[jnum,inum] = np.mean(currentfft[j:(j+banksize)])
			j = j + banksize
			jnum = jnum + 1
		#compute average for each window
		#put result in res
		i += winsamples
		inum += 1
	return res

def fbdiff(w1,w2):
	'''filterbank function for tst()

	Computes the absolute value of the difference
	between the matrix representations of two
	waves.

	The matrices must have the same dimensions.

	Args:
		w1:	wave 1
		w2:	wave 2
	'''
	return sum(sum(abs(w1-w2)))

def dtw(t,r):
	'''Dynamic time warping algorithm

	DTW algorithm for simple vectors.

	Args:
		t:	first vector
		r:	second vector

	Returns:
		pairs:	each pair of values
		path:	the path in terms of indices
			in the vectors
	'''
	ta = np.array([t])
	ra = np.array([r])
	N = ta.size
	M = ra.size
	tax = np.matlib.repmat(ta,M,1)
	rax = np.matlib.repmat(ra.transpose(),1,N)
	d = (tax-rax)**2
	D = np.zeros(d.shape)
	D[0,0] = d[0,0]
	for m in range(1,M):
		D[m,0] = d[m,0] + D[m-1,0]
	for n in range(1,N):
		D[0,n] = d[0,n] + D[0,n-1]
	for n in range(1,N):
		for m in range(1,M):
			D[m,n] = d[m,n] + min([D[m,n-1],D[m-1,n-1],D[m-1,n]])
	Dist = D[M-1,N-1]
	path = [(M-1,N-1)]
	while path[-1] != (0,0):
		left = path[-1][0]
		right = path[-1][1]
		if left == 0:
			path.append((left,right-1))
		elif right == 0:
			path.append((left-1,right))
		else:
			loc = np.argmin(
				[D[left-1,right],D[left,right-1],D[left-1,right-1]]
			)
			if loc == 0:
				path.append((left-1,right))
			elif loc == 1:
				path.append((left,right-1))
			else:
				path.append((left-1,right-1))
	pairs = []
	for p in path:
		pair = (r[p[0]],t[p[1]])
		pairs.append(pair)
	pairs.reverse()
	return pairs,path

def dtwdemo():
	'''Dynamic time warping demo'''
	a = []
	for x in range(7): a.append(r.randint(1,9))
	b = []
	for x in range(11): b.append(r.randint(1,9))
	pairs,path = dtw(a,b)
	plt.plot(range(len(a)),np.ones(len(a)),'g.')
	for i in range(len(a)): plt.text(i,.8,str(a[i]))
	plt.plot(range(len(b)),np.ones(len(b))+2,'b.')
	for i in range(len(b)): plt.text(i,3.1,str(b[i]))
	for p in path: plt.plot(p,[3,1],'r-')
	plt.axis([-1,len(b)+2,0,4])
	plt.show()

def dtwvec(t,r):
	'''dynamic time warping for digits set

	This computes the best cost for aligning
	two vectors

	Args:
		t:	matrix for first wave
		r:	matrix for second wave

	Returns:
		the cost of the best alignment
	'''
	ta = np.array(t)
	ra = np.array(r)
	N = ta.shape[1]
	M = ra.shape[1]
	d = np.zeros([N,M])
	for n in range(N):
		for m in range(M):
			d[n,m] = math.sqrt(sum((ta[:,n] - ra[:,m])**2))
	D = np.zeros(d.shape)
	for n in range(1,N):
		D[n,0] = d[n,0] + D[n-1,0]
	for m in range(1,M):
		D[0,m] = d[0,m] + D[0,m-1]
	for n in range(1,N):
		for m in range(1,M):
			D[n,m] = d[n,m] + min([D[n-1,m],D[n-1,m-1],D[n,m-1]])
	val = D[N-1,M-1]
	return val

def melfbdemo(w,n):
	'''demo of MEL filterbanks

	This displays a normal filterbank and
	then a MEL-scaled filterbank for some
	wave.

	Args:
		w:	string location of the wave file
		n:	number of filterbanks
	'''
	fsx,wx = wavfile.read(w)
	mx,fx = spec(wx,fsx)
	binsize = np.floor(len(mx)/n)
	wnew = np.zeros(len(mx))
	i = 0
	while i+binsize < len(mx):
		startpoint = int(i)
		endpoint = int(i + binsize)
		#get the mean value for the bank
		meanval = np.mean(mx[startpoint:endpoint])
		#set corresponding new segment to that value
		wnew[startpoint:endpoint] = meanval
		i = i + binsize
	#compute mel values from frequency f
	mel = 2595 * np.log10(1 + fx/700)
	#mels per bank
	melnum = math.floor(mel[-1]/n)
	#create new spectrum for filterbank
	wnewmel = np.zeros(len(mel))
	for i in range(1,n):
		curbinstartval = ((i-1)*melnum)+1
		curbinendval = i*melnum
		#find start
		j = 0
		while mel[j] < curbinstartval:
			j += 1
		curstart = j
		#find end
		j = len(mel)-1
		while mel[j] > curbinendval:
			j -= 1
		curend = j
		#find mean of that span
		meanval = np.mean(mx[curstart:curend])
		#assign that mean to relevant span of wnewmel
		wnewmel[curstart:curend] = meanval
	plt.figure(figsize=(6,10))
	plt.subplot(3,1,1)
	plt.plot(mx)
	plt.title('Linear spectrum')
	plt.subplot(3,1,2)
	plt.plot(wnew,'r')
	plt.title('Bins for linear spectrum')
	plt.subplot(3,1,3)
	plt.plot(wnewmel,'g')
	plt.title('Bins for mel spectrum')
	plt.subplots_adjust(hspace=1)
	plt.show()

def cepdemo(w,fs):
	'''cepstrum demo

	This displays a wave in various
	ways including a cepstrum

	Args:
		w:	the wave
		fs:	the sample rate
	'''
	#scale x-axis using sampling rate
	t = np.array(list(range(len(w))))/fs
	plt.figure(figsize=(6,15))
	plt.subplot(4,1,1)
	plt.plot(t,w)
	plt.legend(['waveform'])
	plt.xlabel('Time (s)')
	plt.ylabel('Amplitude')
	plt.ylim(-15000,15000)
	h = np.hanning(len(w))
	x = np.fft.fft(w*h)
	#plot log-scaled spectrum of lower 5000 Hz
	#calculate index for 5000 Hz
	hz5000 = math.floor(5000*len(x)/fs)
	#scale frequencies using sampling rate
	f = np.array(list(range(hz5000)))*fs/len(x)
	eps = sys.float_info.epsilon
	plt.subplot(4,1,2)
	plt.plot(f,abs(x[:len(f)]+eps),'g')
	plt.legend(['spectrum'])
	plt.xlabel('Frequency (Hz)')
	plt.ylabel('Magnitude (dB)')
	plt.subplot(4,1,3)
	plt.plot(f,20*np.log10(abs(x[:len(f)])+eps),'c')
	plt.legend(['log-scaled spectrum'])
	plt.xlabel('Frequency (Hz)')
	plt.ylabel('Magnitude (dB)')
	C = np.fft.fft(np.log(abs(x)+eps))
	#maximum 5000Hz
	ms1 = round(fs/5000)
	#minimum 50Hz
	ms20 = round(fs/50)
	q = np.array(range(ms1,ms20+1))/fs
	plt.subplot(4,1,4)
	plt.plot(abs(C[ms1:ms20]),'r')
	plt.legend(['cepstrum'])
	plt.xlabel('Quefrency')
	plt.ylabel('Amplitude')
	plt.show()

def lpcrep(w,fs,winsize,order):
	'''computes an LPC

	The size of the window is entered as
	either an integer or a fraction of 1.
	If it's entered as an integer, then
	it specifies the number of miliseconds
	in each window. If it's entered as a
	fraction, then it's that fraction of
	the total wave duration.

	Args:
		w:		wave
		fs:		sample rate
		winsize:	size of windows
		order:		order of the LPC

	Returns:
		the LPC matrix
	'''
	#number of samples per window
	if winsize > 1:
		winsamples = math.floor(fs * winsize * .001)
	else:
		winsamples = math.floor(len(w) * winsize)
	#total number of windows
	numwindows = math.floor(len(w)/winsamples)
	#create a matrix for the result
	res = np.zeros([order+1,numwindows])
	i = 0
	inum = 0
	while i+winsamples < len(w):
		#get current window
		currentwin = w[i:(i+winsamples)]
		#do lpc
		curlpc = lpc(currentwin,order)
		#add to res
		res[:,inum] = curlpc
		#update counters
		i = i + winsamples
		inum = inum + 1
	return res

def kmeansdemo(points,clusters):
	'''K-means demo

	Plots 10 steps of a k-means process

	Args:
		points:		number of points to cluster
		clusters:	number of clusters
	'''
	cmap = cm.rainbow(np.linspace(0.0,1.0,clusters))
	a = np.random.randint(0,100,[points,2])
	kmeans = KMeans(
		n_clusters=clusters,
		max_iter=1,
		init='random',
		n_init=1
	).fit(a)
	idx = kmeans.labels_
	c = kmeans.cluster_centers_
	for i in range(points):
		plt.plot(a[i,0],a[i,1],'.',color=cmap[idx[i]])
	plt.title('Plot 1')
	plt.show()
	for j in range(2,11):
		kmeans = KMeans(
			n_clusters=clusters,
			max_iter=1,
			init=c,
			n_init=1
		).fit(a)
		idx = kmeans.labels_
		c = kmeans.cluster_centers_
		for i in range(points):
			plt.plot(a[i,0],a[i,1],'.',color=cmap[idx[i]])
		plt.title('Plot ' + str(j))
		plt.show()

def allvecs(frames,vqcount):
	'''vector quantization for digits set

	This converts a matrix to a quantized
	matrix.

	Args:
		frames:		frame matrix
		vqcount:	number of quantities

	Returns:
		quantized matrix
	'''
	veclength = len(frames[0][0])
	alldigits = list(
		map(
			np.array,
			[digit for subj in frames for digit in subj]
		)
	)
	allofthem = np.hstack(alldigits)
	allofthem = allofthem.T
	kmeans = KMeans(n_clusters=vqcount).fit(allofthem)
	idx = kmeans.labels_
	c = kmeans.cluster_centers_
	allcentroids = np.array([c[i,:] for i in idx]).T
	#put those into something like frames and return it
	newframes = []
	frametotal = 0
	i = 0
	for subj in frames:
		cursubj = []
		for digit in subj:
			curcount = len(digit[0])
			frametotal += curcount
			j = i + curcount
			j -= 1
			curdigit = allcentroids[:,i:j].tolist()
			i = j + 1
			cursubj.append(curdigit)
		newframes.append(cursubj)
	return newframes

def makeran(seed,nouns='nouns.txt',verbs='verbs.txt'):
	'''randomization for nouns/verbs project

	This creates two random lists of 1100 integers
	for the nouns/verbs project.

	Args:
		seed:	random seed
		nouns:	location of nouns.txt file
		verbs:	location of verbs.txt file

	Returns:
		tuple of two integer lists
	'''
	f = open(nouns,'r')
	ns = f.read()
	f.close()
	ns = ns.split('\n')
	f = open(verbs,'r')
	vs = f.read()
	f.close()
	vs = vs.split('\n')
	r.seed(seed)
	ns = r.sample(range(len(ns)-1),1100)
	vs = r.sample(range(len(vs)-1),1100)
	return (ns,vs)

def _tonums(w):
	return list(
		map(
			lambda x: [ord(x)-97],
			list(w)
		)
	)

def nounsverbs(tr,e,r,ns='nouns.txt',vs='verbs.txt'):
	#read in nouns and verbs
	f = open(ns,'r')
	nouns = f.read()
	f.close()
	nouns = nouns.lower()
	nouns = nouns.split('\n')
	f = open(vs,'r')
	verbs = f.read()
	f.close()
	verbs = verbs.lower()
	verbs = verbs.split('\n')
	#get random samples
	nidx = r[0]
	vidx = r[1]
	rnouns = []
	for n in nidx:
		rnouns.append(nouns[n])
	rverbs = []
	for v in vidx:
		rverbs.append(verbs[v])
	#100 nouns for testing
	nt = rnouns[0:100]
	#1000 nouns for training
	ns = rnouns[101:]
	#100 verbs for testing
	vt = rverbs[0:100]
	#1000 verbs for training
	vs = rverbs[101:]
	nlets = len(set(list(''.join(ns))))
	vlets = len(set(list(''.join(vs))))
	if vlets != 26 or nlets != 26:
		print('Bad letter distribution, resample.')
	else:
		letters = 'abcdefghijklmnopqrstuvwxyz'
		letters = list(letters)
		#HMM for nouns
		#make distributions
		states = []
		for row in e:
			d = p.DiscreteDistribution(
				dict(list(zip(letters,row)))
			)
			states.append(p.State(d))
		nounmodel = p.HiddenMarkovModel()
		nounmodel.add_states(states)
		nounmodel.add_transition(nounmodel.start,states[0],1.0)
		for row in range(len(tr)):
			for col in range(len(tr[row])):
				nounmodel.add_transition(states[row],states[col],tr[row,col])
		nounmodel.bake()
		#HMM for verbs
		#make distributions
		states = []
		for row in e:
			d = p.DiscreteDistribution(
				dict(list(zip(letters,row)))
			)
			states.append(p.State(d))
		verbmodel = p.HiddenMarkovModel()
		verbmodel.add_states(states)
		verbmodel.add_transition(verbmodel.start,states[0],1.0)
		for row in range(len(tr)):
			for col in range(len(tr[row])):
				verbmodel.add_transition(states[row],states[col],tr[row,col])
		verbmodel.bake()
		#train nouns (ns)
		nounmodel.fit(map(list,ns))
		#train verbs (vs)
		verbmodel.fit(map(list,vs))
		#check nouns
		success = 0
		for n in nt:
			nscore = nounmodel.probability(n)
			vscore = verbmodel.probability(n)
			if nscore > vscore:
				success += 1
		print('nouns correctly idendified: ',success,'/100',sep='')
		#check verbs
		success = 0
		for v in vt:
			nscore = nounmodel.probability(v)
			vscore = verbmodel.probability(v)
			if vscore > nscore:
				success += 1
		print('verbs correctly idendified: ',success,'/100',sep='')

def nvs(tr,e,r,ns='nouns.txt',vs='verbs.txt'):
	'''hmmlearn version of nounsverbs()'''
	#read in nouns and verbs
	f = open(ns,'r')
	nouns = f.read()
	f.close()
	nouns = nouns.lower()
	nouns = nouns.split('\n')
	f = open(vs,'r')
	verbs = f.read()
	f.close()
	verbs = verbs.lower()
	verbs = verbs.split('\n')
	#get random samples
	nidx = r[0]
	vidx = r[1]
	rnouns = []
	for n in nidx:
		rnouns.append(nouns[n])
	rverbs = []
	for v in vidx:
		rverbs.append(verbs[v])
	#100 nouns for testing
	nt = rnouns[0:100]
	#1000 nouns for training
	ns = rnouns[101:]
	#100 verbs for testing
	vt = rverbs[0:100]
	#1000 verbs for training
	vs = rverbs[101:]
	nlets = len(set(list(''.join(ns))))
	vlets = len(set(list(''.join(vs))))
	if vlets != 26 or nlets != 26:
		print('Bad letter distribution, resample.')
	else:
		#HMM for nouns
		nodes = len(tr)
		startprobs = nm.repmat(0,1,nodes)
		startprobs[0] = 1
		mns = hmm.MultinomialHMM(nodes)
		mns.transmat_ = tr
		mns.emissionprob_ = e
		ns = list(map(_tonums,ns))
		nslens = list(map(len,ns))
		ns = np.concatenate(ns)
		mns.fit(ns,nslens)
		#HMM for verbs
		mvs = hmm.MultinomialHMM(nodes)
		mvs.transmat_ = tr
		mvs.emissionprob_ = e
		vs = list(map(_tonums,vs))
		vslens = list(map(len,vs))
		vs = np.concatenate(vs)
		mvs.fit(vs,vslens)
		#check nouns
		nt = list(map(_tonums,nt))
		success = 0
		for n in nt:
			nscore = np.exp(mns.score(n))
			vscore = np.exp(mvs.score(n))
			if nscore > vscore:
				success += 1
		print('nouns correctly idendified: ',success,'/100',sep='')
		#check verbs
		vt = list(map(_tonums,vt))
		success = 0
		for v in vt:
			nscore = np.exp(mns.score(v))
			vscore = np.exp(mvs.score(v))
			if vscore > nscore:
				success += 1
		print('verbs correctly idendified: ',success,'/100',sep='')

def _rand_jitter(arr):
	'''Add jitter to a set of points
	
	pulled from the web somewhere
	
	Args:
		arr: an array of points
	
	Returns:
		jittered points
	'''
	stdev = .01*(max(arr)-min(arr))
	return arr + np.random.randn(len(arr)) * stdev

def firstlast(name,namefile='names.txt'):
	'''covariance demo
	
	Calculates the covariance between the lengths
	of a random sample of firstname - lastname
	pairs, displays the relationship, and then
	calculates the probability of a specific
	firstname - lastname pair.
	
	Args:
		name:		a name
		namefile:	location of a sample of pairs
	'''
	#read in names document
	f = open(namefile,'r')
	n = f.read()
	f.close()
	n = n.split('\n')
	#get rid of final return
	n = n[:-1]
	#split each line into two names
	n = list(map(lambda x: x.split(' '),n))
	#get the length of all first names
	firstnames = np.array(list(map(lambda x: len(x[0]),n)))
	#get the length of all last names
	lastnames = np.array(list(map(lambda x: len(x[1]),n)))
	#plot both with a little jitter
	fj = _rand_jitter(firstnames)
	lj = _rand_jitter(lastnames)
	plt.plot(fj,lj,'r.',markersize=10)
	plt.xlabel('first names')
	plt.ylabel('last names')
	plt.show()
	#histogram of first names
	plt.hist(firstnames)
	plt.xlabel('first names')
	plt.show()
	#histogram of last names
	#plt.subplot(3,1,3)
	plt.hist(lastnames)
	plt.xlabel('last names')
	plt.show()
	#split up the current name
	thisfirstname,thislastname = name.split(' ')
	#get the lengths for the current name
	thisfirst = len(thisfirstname)
	thislast = len(thislastname)
	#compute the covariance matrix
	mysig = np.cov(firstnames,lastnames)
	#determinant of the matrix
	mydet = np.linalg.det(mysig)
	#do all the math in 9.32 on page 162
	leftside = (1/(mydet**(1/2) * (2*math.pi)**(2/2)))
	themeans = np.array([np.mean(firstnames),np.mean(lastnames)])
	thispair = np.array([thisfirst,thislast])
	thisdiff = thispair - themeans
	mysiginv = np.linalg.inv(mysig)
	rightside = np.exp(
		np.matmul(np.matmul(-thisdiff,mysiginv),thisdiff)/2
	)
	total = leftside * rightside
	print('UA linguist probability: {:1.4f}'.format(total))

def perceptrondemo():
	link = 'http://dingo.sbs.arizona.edu/~hammond/lsasummer11/newdic'
	f = urllib.request.urlopen(link)
	#read the page
	rawtext = f.read()
	#decode page
	n = rawtext.decode('UTF-8')
	n = n.split('\n')
	n = n[:-1]
	n = list(map(lambda x: x.split('\t'),n))
	#extract and massage relevant data for
	#specified number of training items
	howmany = 500
	words = list(map(lambda x: x[3],n))
	frequencies = list(map(lambda x: int(x[4]),n))
	letters = list(map(len,words))
	syltargets = list(map(lambda x: int(x[2][1:]),n))
	traindata = np.vstack((letters,frequencies))
	traindata = traindata.T
	trainlabels = np.array(syltargets)
	#make the perceptron net
	net = Perceptron(tol=1e-3)
	net.fit(traindata[:howmany],trainlabels[:howmany])
	score = net.score(
		traindata[howmany+1:howmany+100],
		trainlabels[howmany+1:howmany+100]
	)
	print('Accuracy: {:0.4f}'.format(score))
	#plot and show linear separation problem
	#have to convert to logs for freqs
	cmap = cm.rainbow(np.linspace(
		0.0,
		1.0,
		len(set(syltargets))
	))
	#only plot a subset
	for i in range(2000):
		let = letters[i]
		freq = frequencies[i] + 1
		syl = syltargets[i]
		plt.plot([0,let],[0,np.log(freq)],color=cmap[syl])
	patches = []
	for p in range(max(syltargets)):
		patches.append(mpatch.Patch(label=str(p+1),color=cmap[p]))
	plt.legend(handles=patches)
	plt.show()

def mymfcc(w,fs):
	res = psf.mfcc(w,fs,nfft=1103,numcep=12)
	d = psf.delta(res,1)
	d2 = psf.delta(res,2)
	final = np.hstack([res,d,d2])
	return final.transpose()

def glottal(cycles=100):
	'''create a terrible glottal pulse

	Args:
		cycles:	how many cycles

	Returns:
		the pulse
	'''
	#make a sequence of 50 numbers from 0 to 1
	t = np.linspace(0,1,50)
	#make a single sawtooth shape over that
	s = ss.sawtooth(2*np.pi*t,1)
	#set baseline to 0
	s += 1
	#make 50 zeros
	z = np.array([0 for i in range(100)])
	#make a pulse train
	p = z
	#make it 100 cycles long
	for i in range(cycles):
		#add the sawtooth
		p = np.append(p,s)
		#add zeros
		p = np.append(p,z)
	return p

def rgcd(numlist):
	'''recursive greatest common denominator

	Args:
		numlist: a list of numbers

	Returns:
		the greatest common denominator
	'''
	return f.reduce(math.gcd,numlist)

