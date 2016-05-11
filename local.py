from numpy import *
import scipy.linalg
import scipy.stats

#the math used in this is heavily inspired by the article:
#A Python Implementation of Chan's TDoA algorithm
#for Ultrasonic Positioning and Tracking

#otherwise, the methods and implementation are written by Thomas Schouten


micPos = array([[ 1., 0.],
		[-1., 0.],
		[-1.,-1.]])
c = 340.29
n = 3

def testPos(x,y):	#used to test the algorithm
	time = empty((n,1))
	for j in range(n):
		d = ((micPos[j,0]-x)**2+(micPos[j,1]-y)**2)**.5
		time[j,0] = d/c

	return  getPosFromTimes(time)

def getPosFromTimes(time):	#the main method to call, this takes a matrix of detected times, and return position data
	posT = concatenate((micPos, time),1)
	dD = getDeltaDistance(posT)
	pos = findPos(dD)
	if len(pos) == 2:
		r0 = pos[0][1]
		r1 = pos[1][1]
		if r0 < r1:
			pos = pos[1]
		else:
			pos = pos[0]
	elif len(pos) == 1:
		pos = pos[0]
	return pos
	
def findPos(dD):	#this is where the majority of the localization algorithm resides
	P = dD[1:3,0:2] - dD[0,0:2]
	A = -linalg.inv(P)
	R = dD[1:3,2]
	R2 = R[:]**2
	M = dD[:,0:2]
	K = dD[:,0]**2+dD[:,1]**2
	B = (R2 - K[1:3] + K[0]) / 2
	E = A.dot(R)
	F = A.dot(B)
	a = 1 - (E.dot(E))
	b = 2 * (M[0].dot(E) - F.dot(E))
	c = 2 * (M[0].dot(F)) - F.dot(F) - K[0]
	discr = b * b - 4 * a * c
	poslist = []
	if discr >= 0:
		h = discr**.5
		for i in (h, -h):
			R0 = (i - b) / (2 * a)
			if R0 >= 0:
				T = E * R0 + F
				poslist.append((squeeze(T), R0)) 	
	return poslist

def getDeltaDistance(posT):	#this establishes a proper matrix for the algorithm, by getting the change in distance rather than time
	A = posT[posT[:,2].argsort()]
	A[:,2] -= A[:,2].min()
	A[:,2]  = A[:,2]*c
	return A