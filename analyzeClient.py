from numpy import *
from scipy import optimize
from Tkinter import Tk
from tkFileDialog import askopenfilename
import matplotlib.pyplot as plt
import sys

#our project files
import local as local
import timeAnalysis as timeA

#Written by Thomas Schouten
#
#This file is meant to be used post-processing. The array must have already
#been run, and a log file generated. This program will then run the 
#filtering and localization code on the data within the log file,
#providing a visual representation of data and the chance to save
#this data for other use in another text file

print '\nSelect a log file to analyze:'

Tk().withdraw() 
filename = askopenfilename(filetypes=[("Text files","*.txt")], title = 'Select a log file to analyze')
print 'opening ',filename
print ''
if filename == '':
	#user canceled the dialog, so just quit the program
	print 'input cancelled, exiting'
	sys.exit()
#send this filename to the filtration code, and determine when bird chirps occur
times = timeA.findTimes(filename)
#here, times is a (n)x(chirps) matrix
n = shape(times)[0]
its = shape(times)[1]
allTimes = zeros(its)
positions = empty((2,its))

for j in range(its):	#this interprets the data from the times matrix
	average = sum(times[:,j]) / float(n)
	time = times[:,j]
	time = transpose(time[newaxis, :])
	pos = local.getPosFromTimes(time)
	if len(pos) == 0:
		continue;	#no location found for this data set
	#print 'At time ', average
	#print 'Location detected at ' , pos[0]
	allTimes[j] = average
	positions[:,j] = pos[0]

for j in range(len(allTimes)):	#This gets rid of false positions
	if j == len(allTimes):
		break
	if allTimes[j] == 0:
		allTimes = delete(allTimes, j)
		positions = delete(positions, j, 1)
for j in range(len(allTimes)):
	print 'At time ', allTimes[j]
	print 'Location detected at ' , positions[:,j]
#locations found and printed, so now just properly record and display the data

fig = plt.figure()
plt.ion()
plt.title('Microphone Array detections')
plt.xlim([-20,20])
plt.ylim([-20,20])
plt.plot([-1,1,1,-1,-1],[0,0,-1,-1,0],'b-')	#draw a small box for the mic array
plt.plot(positions[0,:], positions[1,:], 'ro', picker=5)
anots = []

#set up the choosable data types
def onpick(event):
	ind = event.ind
	for i in anots:
		i.remove()
		anots.remove(i)
	for i in ind:
		anots.append(plt.annotate('Time: ' + str(allTimes[i])[:7],xy = (positions[0,i]+.5,positions[1,i]+.5)))
	plt.show()	

fig.canvas.mpl_connect('pick_event', onpick)
plt.show(block = True)

#finally, see if user wants the analysist saved
print 'Save data to "PosTimeData.txt"?   (y or n)'
input = raw_input()
if input == 'y':
	print 'Saving data...'
	data = open('PosTimeData.txt', 'w')
	data.truncate()
	data.write('Format:     birdX,birdY,Time\n\n')
	for i in range(its):
		line = str(positions[0,i]) + ',' + str(positions[1,i]) + ',' + str(allTimes[i]) + '\n'
		data.write(line)
	data.close()
elif input == 'n':
	print 'Exiting...'
else:
	print 'Input not understood, exiting program'








