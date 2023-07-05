import sys
import numpy
import string

if (len(sys.argv)!=3):
	raise NameError("arguments must be input and output filenames")

input = sys.argv[1]
output = sys.argv[2]

with open(input, 'r') as csvfile:
	data=numpy.loadtxt(csvfile, delimiter=',')

retentiontimes=[]

state = {
	"top of waterbox": 0,
	"in vacuum": 1,
	"bottom of waterbox": 2
}

laststateindex=1
stateindex=1

iretention=0.0
fretention=0.0

for t in data:
	if (80<t[1]<95):
		stateindex = state.get("top of waterbox")
	elif (5<t[1]<20):
		stateindex = state.get("bottom of waterbox")
	elif (20<=t[1]<=80):
		stateindex = state.get("in vacuum")
	
	if (laststateindex == 1 and (stateindex==0 or stateindex==2)):
		iretention = t[0]
	elif ((laststateindex==0 or laststateindex==2) and stateindex==1):
		fretention = t[0]
		retention = fretention - iretention
		if (retention > 0.5):
			retentiontimes.append(fretention-iretention)
	
	laststateindex = stateindex

with open(output, 'w') as outfile:
	for time in retentiontimes:
		outfile.write(str(time)+"\n")

outfile.close()
