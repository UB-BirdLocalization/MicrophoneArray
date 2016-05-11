from numpy import *
from scipy import optimize
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write
from scipy.fftpack import fft




def getStartTimes(dataa,rate):
	#first, low-pass filter
	dataa = abs(dataa-average(dataa))
	#plt.plot(dataa)
	fuzz = 5
	data = empty(len(dataa)-fuzz)
	for i in range(len(data)):
		data[i] = average(dataa[i:i+fuzz])
	#plt.plot(data)			#these are useful for checking the data being filtered, to properly
	#plt.ylim([0,600])		#setup the filtering algorithm to specific data.
	#plt.show()
		
	birdSounding = False		#if in a state of active or not
	minLengthForDetect = 5		#consecutive samples must be greater to detect sound
	maxLengthBeforeBreak = 30	#allowed points below cutoff before sound is considered over
	cutoff = 55					#sounds above this are considered active and will be located
	
	time = []
	
	for j in range(len(data)):
		value = data[j]
		if birdSounding:
			if value >= cutoff:
				continue
			if len(data) - j < maxLengthBeforeBreak:
				continue
			if max(data[j:j+maxLengthBeforeBreak]) > cutoff:
				continue
			birdSounding = False
			continue
		if value < cutoff:
			continue
		if len(data) - j < minLengthForDetect:
			if min(data[j:len(data)]) < cutoff:
				continue
		if min(data[j:j+minLengthForDetect]) < cutoff:
			continue
		#start of birdsong detected
		time.append(float(j)/rate)
		birdSounding = True
	return time


def findTimes(filename):
	#this takes log data from the file, turns it into lists of values, then passes everything into the 
	#filtering method
	data1 = []
	data2 = []
	data3 = []
	log = open(filename, 'r')
	rate = 0
	for line in log.readlines():		#parse file for info
		if ',' not in line:
			#final line here, containing the rate info
			rate = int(line)
			break
		vals = line.split(',')
		if len(vals) != 3:
			print 'invalid file given'
			sys.exit()
		data1.append(int(vals[0]))
		data2.append(int(vals[1]))
		data3.append(int(vals[2]))
	log.close()
	if rate == 0:
		#something bad happened
		print 'Error occured while reading file'
		sys.exit()
		
	#at this point, all data is fully parsed. 
	
	time = linspace(0, len(data1) / rate, len(data1))
	plt.plot(time, data1, 'b')
	plt.plot(time, data2, 'r')
	plt.plot(time, data3, 'g')
	plt.ylim([0,600])
	plt.show()		#display microphone data
	
	time1 = getStartTimes(data1, rate)	#these filter over the data and find sound times
	time2 = getStartTimes(data2, rate)
	time3 = getStartTimes(data3, rate)
	
	#now, need to remove extra time data that doesn't fit with the rest of the data
	window = .01	#times must be at least this close together, or be removed
	time1ind = 0
	time2ind = 0
	time3ind = 0
	while time1ind < len(time1) and time2ind < len(time2) and time3ind < len(time3):
		minim = min([time1[time1ind], time2[time2ind],time3[time3ind]])
		maxim = max([time1[time1ind], time2[time2ind],time3[time3ind]])
		if maxim - minim > window:		
			#time lapse detected. kill smallest terms, they have no partners
			if minim == time1[time1ind]:
				del time1[time1ind]
			if minim == time2[time2ind]:
				del time2[time2ind]
			if minim == time3[time3ind]:
				del time3[time3ind]
			continue
		#here, a full set in window is good to go. Advance the indexes
		time1ind += 1
		time2ind += 1
		time3ind += 1
	minim = min([len(time1), len(time2), len(time3)])	#now cut off remaining stuff
	while len(time1) != minim:
		del time1[-1]
	while len(time2) != minim:
		del time2[-1]
	while len(time3) != minim:
		del time3[-1]
	
	#finally, create the array to return, 3xn of sounds
	A = empty((3,len(time1)))
	for i in range(len(time1)):
		A[0,i] = time1[i]
		A[1,i] = time2[i]
		A[2,i] = time3[i]
	return A
	
	
if __name__ == "__main__":
	#this is used for testing. Typically, this file should not be run directly.
	chunk = 2048
	n = 3

	rate, x = wavfile.read('birdLo/bird.wav')
	print rate
	time = []	#save detected birdSong chirps here

	x = abs(x-average(x))
	fuzz = 5
	xx = empty(len(x)-fuzz)
	for i in range(len(xx)):
		xx[i] = average(x[i:i+fuzz])

	#at this point, take xx and find dem times

	time = getStartTimes(xx, rate)
	print time
	timeIndex = 0

	for j in range(10,x.size,chunk):
		if j+chunk > x.size:
			break #avoid overflow
		data = x[j:j+chunk]
		dataa =xx[j:j+chunk] 
		#this block is to visualize a certain block at a time, as well as listen to what it represents
		f, axarr = plt.subplots(2, sharex=True)
		axarr[0].plot(data,'r')
		axarr[0].plot(dataa,'b')
		axarr[0].set_ylim(ymin = 0, ymax = 5000)
		axarr[1].plot(fft(data))
		#here, display the times detected for comparison
		if timeIndex != len(time):
			while time[timeIndex] > float(j)/rate and time[timeIndex] < float(j+chunk)/rate:
				axarr[0].plot([time[timeIndex]*rate - j,time[timeIndex]*rate - j],[0,5000],'g-')
				timeIndex += 1
				if timeIndex == len(time):
					break
	plt.show()