from numpy import *
from scipy import optimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
micPos = array([[-1.,1., 0.],
		[1. ,1., 0.],
		[-1.,-1.,0.],
		[1.,-1., 0.],
		[-1.,1., 1.],
		[1. ,1., 1.],
		[-1.,-1.,1.],
		[1.,-1., 1.]])
c = 340.29
n = 8

def testPos(x,y,z):
	time = empty(n)
	for j in range(n):
		d = ((micPos[j,0]-x)**2+(micPos[j,1]-y)**2+(micPos[j,2]-z)**2)**.5
		time[j] = d/c
	pos = empty(3)
	pos[:] = getPosFromTimes(time)
	
	

def getDeltaTime(time):
	A = empty((n,n))
	for i in range(n):
		for j in range(n):
			A[i,j] = time[i] - time[j]
	return A
	
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
		print linalg.lstsq(A,B)[1]
	return U

def func(pos, U):
	Error = empty((3,n))
	for j in range(n):
		d = ((pos[0]-micPos[j,0])**2+(pos[1]-micPos[j,1])**2+(pos[2]-micPos[j,2])**2)**0.5
		Error[:,j] = pos[:] - micPos[j,:] - d*U[:,j]
	Error[:,:] = Error[:,:]**2
	#print sum(Error)
	return sum(Error)
		
def getPosFromTimes(time):			
	DT = getDeltaTime(time)		
	U = getDirections(DT)		
	print U	
	X = micPos[:,0]
	Y = micPos[:,1]
	Z = micPos[:,2]
	Uu = X[:]+U[0,:]*100.
	V = Y[:]+U[1,:]*100.
	W = Z[:]+U[2,:]*100.
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for j in range(n):
		ax.plot([X[j], Uu[j]],[Y[j],V[j]],[Z[j],W[j]])
	plt.show()
	
	print optimize.fmin(func, array([0.,10.,0.]), args = (U,))		
		
			
	return 0.,0.,0.		
			
testPos(5.,10.,15.)
