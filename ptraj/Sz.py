import string
import re

with open('heat.mdcrd', 'r') as file:
	data = file.read()

matches = re.findall("[\d\.]+\n  31\.077  31\.077 150\.000",data)
z = []

for s in matches:
	z.append(string.atof(string.split(s,"\n")[0]))

print("matches found")

time = 0
interval = 0.05

output = open('O2zcrds.csv', 'w')

print("writing values")

for crd in z:
	output.write("{time},{crd}\n".format(time=time, crd=crd))
	time += interval

output.close()


