import sys
import string
import os

input = '2_eq.cdl'
output = '2_eq+so2.cdl'
rst_out = output.split('.')[0] + '.rst'

if (not os.path.exists(input)):
	if (os.path.exists("2_eq.rst")):
		os.system("ncdump 2_eq.rst > 2_eq.cdl")
	else:
		print("check input files")
		sys.exit()

atom_line = 3
position_line = 2278
velocity_line = 4522
lengths_line = 4531

with open(input, 'r') as textfile:
	lines = textfile.readlines()

if len(lines) > lengths_line: 
	lines[atom_line] = "	atom = 2245 ;\n"
	lines[position_line].split
	lines[position_line] = lines[position_line].split(";")[0][:-1] + ',' + """
  70.0000000000000, 1.18525500000000, -0.4171930000000,
  70.0000000000000, -0.93950900000000, 0.8343870000000,
  70.0000000000000, -0.24575500000000, -0.4171930000000 ;
"""
	lines[velocity_line] = lines[velocity_line].split(";")[0][:-1] + ',' + """
  0.0986198371867947, 0.176258975883912, 0.126565219156263,
  0.124721981646369, -0.109159348948368, -0.135879248014089,
  -0.152937279252986, -0.127448045307781, -0.185378047259104 ;
"""
	lengths_split = lines[lengths_line].split(" ")
	lengths_split[3] = '100.000000000000,'
	lines[lengths_line] = " ".join(lengths_split)

with open(output, 'w') as outfile:
	outfile.writelines(lines)


if (not os.path.exists(rst_out)):
	os.system("ncgen -o " + rst_out + " " + output)
else:
	print("not writing output!")

os.system("rm " + input)
os.system("rm " + output)
