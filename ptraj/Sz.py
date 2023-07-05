import sys
import string
import re

if (len(sys.argv)!=3):
	raise NameError("arguments must be input and output filenames")

input = sys.argv[1]
output = sys.argv[2]

with open(input, 'r') as file:
	data = file.read()

matches = re.findall("[\d\.]+\n  63\.000  63\.000 63\.000",data)
z = []

for s in matches:
	z.append(string.atof(string.split(s,"\n")[0]))

print("matches found")

time = 0
interval = 0.05

print("writing values")
#write times
with open(output, 'w') as outfile:
	for crd in z:
		outfile.write("{time},{crd}\n".format(time=time, crd=crd))
		time += interval



