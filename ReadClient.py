from numpy import *
import serial
import serial.tools.list_ports
import sys
from time import sleep
BAUDRATE = 250000
COM_PORT = 'read'	#change this to the attached COM number
print 'waiting for connection to microphone array...'

#detect attached device
ports = list(serial.tools.list_ports.comports())
for p in ports:
	print "found", p.device
	COM_PORT = p.device
	
if COM_PORT == 'read':
	print 'no attached microcontroller'
	sys.exit()
ser = serial.Serial(timeout = 1)

ser.baudrate = BAUDRATE
ser.port = COM_PORT

#actually open the connection to array
while not ser.is_open:
	ser.open()
if ser.is_open:
	print 'connection established'

print 'please reset the microcontroller, and then'
print 'enter the amount of time you want'
input = raw_input('the array to run for:  ')
input = int(float(input))
if input <= 0:
	print 'invalid time entered'
	sys.exit()
input = str(input) + '\n'
ser.write(input)

#first, erase the previous log data
log = open('dataLog.txt', 'w')
log.truncate()
log.close()

print 'Beginning Read...'
log = open('dataLog.txt', 'w')
response = ''
while True:
	#log = open('dataLog.txt', 'w')
	response = ser.readline()
	if ',' not in response:
		if response == '':
			print 'Error in communication. Try reseting the microcontroller'
			log.close()
			sys.exit()
		log.close()
		break
	if response.count(',') != 2:
		print response
	log.write(response)
print 'Finished reading'	
rate = int(float(ser.readline().strip()))
print response, str(rate)

#finally, append the sample rate to the end of the file
log = open('dataLog.txt', 'a')
log.write(str(rate))
log.close()
	
	
	
	
	
	
	
	