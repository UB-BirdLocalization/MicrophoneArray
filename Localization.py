from numpy import *
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Written by Thomas Schouten
#
#The purpose here is to take a time-of-noise array, and return 
#an estimated position. Currently, a testPos method is available
#to generate time differences for testing other methods
#
#A few constants need to be set first
#micPos holds the x,y,z coordinates of each microphone
micPos = array([[-1.,1., 0.],
		[1. ,1., 0.],
		[-1.,-1.,0.],
		[1.,-1., 0.],
		[-1.,1., 1.],
		[1. ,1., 1.],
		[-1.,-1.,1.],
		[1.,-1., 1.]])
c = 340.29	#the speed of sound, in m/s
n = 8		#the number of microphones in total

#this is the testing method. Input an x,y,z coordinate and observe
#the final output to see if the methods work
def testPos(x,y,z):
	time = empty(n)
	for j in range(n):
		d = ((micPos[j,0]-x)**2+(micPos[j,1]-y)**2+(micPos[j,2]-z)**2)**.5
		time[j] = d/c
	pos = getPosFromTimes(time)
	print 'position equals ',pos
	
#returns an array of time differences between microphones
def getDeltaTime(time):
	A = empty((n,n))
	for i in range(n):
		for j in range(n):
			A[i,j] = time[i] - time[j]
	return A
	
#gets a collection of unit vectors toward bird from each microphone
def getDirections(dTimes):
	U = empty((3,n))
	for i in range(n):
		A = empty((n,3))
		for j in range(n):
			A[j,0] = -micPos[i,0] + micPos[j,0]
			A[j,1] = -micPos[i,1] + micPos[j,1]
			A[j,2] = -micPos[i,2] + micPos[j,2]
		B = empty(n)
		for j in range(n):
			B[j] = c*(dTimes[i,j])
		U[:,i] = linalg.lstsq(A,B)[0]
		#print linalg.lstsq(A,B)[1]
	return U

#function to be minimized in getPosFromTimes
def func(pos, U):
	Error = empty((3,n))
	for j in range(n):
		d = ((pos[0]-micPos[j,0])**2+(pos[1]-micPos[j,1])**2+(pos[2]-micPos[j,2])**2)**0.5
		Error[:,j] = pos[:] - micPos[j,:] - d*U[:,j]
	Error[:,:] = Error[:,:]**2
	#print sum(Error)
	return sum(Error)

#finds optimal position of bird to minimize error in above function		
def getPosFromTimes(time):			
	DT = getDeltaTime(time)		
	U = getDirections(DT)		
	#print U	
	X = micPos[:,0]
	Y = micPos[:,1]
	Z = micPos[:,2]
	Uu = X[:]+U[0,:]*100.
	V = Y[:]+U[1,:]*100.
	W = Z[:]+U[2,:]*100.
	#fig = plt.figure()	#this code prints 3D vectors, used for testing
	#ax = fig.add_subplot(111, projection='3d')
	#for j in range(n):
	#	ax.plot([X[j], Uu[j]],[Y[j],V[j]],[Z[j],W[j]])
	#plt.show()
	
	return optimize.fmin(func, array([0.,10.,0.]), args = (U,))[0:3]			




#actually test the code			
testPos(5.,10.,15.)
