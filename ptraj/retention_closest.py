import sys
import numpy
import string

if (len(sys.argv)!=3):
	raise NameError("arguments must be input and output filenames")

input = sys.argv[1]
output = sys.argv[2]

def frametotime(frame):
	initialtime=0
	interval=0.05 #in picoseconds
	return (frame-1)*interval+initialtime

with open(input, 'r') as txtfile:
	data=numpy.loadtxt(txtfile)

# delete columns 2 and 4
data=numpy.delete(data, 3, 1)
data=numpy.delete(data, 1, 1)

#convert frame to time
for i in range(len(data)):
	data[i][0] = frametotime(data[i][0])

def movingaverage(list, n):
	window=numpy.ones(int(n))/float(n)
	return numpy.convolve(list, window, 'same')

y_values = data[:,1]
y_smoothed = movingaverage(y_values, 100) #averaging over 5.0ps
data[:,1] = y_smoothed


retentiontimes=[]

state = {
	"on surface": 0,
	"in vacuum": 1,
}

laststateindex=1
stateindex=1

iretention=0.0
fretention=0.0

for t in data:
	#if closest water molecule is less than 8 angstroms
	if (t[1]<8):
		stateindex = state.get("on surface")
	elif (8<=t[1]):
		stateindex = state.get("in vacuum")
	
	if (laststateindex == 1 and stateindex==0):
		iretention = t[0]
	elif (laststateindex==0 and stateindex==1):
		fretention = t[0]
		retention = fretention - iretention
		if (retention > 0.2):
			retentiontimes.append(retention)
	laststateindex = stateindex

#write times
with open(output, 'w') as outfile:
	for time in retentiontimes:
		outfile.write(str(time)+"\n")

#write smoothed distances
with open("water_smoothed.csv", 'w') as outfile:
	for line in data:
		outfile.write(str(line[0])+','+str(line[1])+'\n')

