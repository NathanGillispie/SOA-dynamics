import os
import math
import sys
import string

number_of_runs = 29
number_of_digits = 2
#number_of_digits = int(math.ceil(math.log10(number_of_runs)))+1 

checks_dir = "chk_multi"
trajectories_dir = "ptj_multi"
pbs_dir = "pbs_multi"
queue_file = "MULTI_PROD.sh"

# DIRECTORIES

if (not os.path.exists(checks_dir)):
	os.mkdir(checks_dir)
else:
	print("checks directory exists.")

if (not os.path.exists(trajectories_dir)):
	os.mkdir(trajectories_dir)
else:
	print("trajectories directory exists.")

if (not os.path.exists(pbs_dir)):
	os.mkdir(pbs_dir)
else:
	print("pbs scripts directory exists.")

#
# QUEUE FILE
#
print("\nQueue files...")

generate_queue_file = True
if (os.path.exists(queue_file)):
	input = ""
	while (input != "y") and (input != "n"):
		input = raw_input("Queue file exists. Would you like to replace it? (y/n)\n")
	if input == "n":
		generate_queue_file = False
	else:
		os.remove(queue_file)
else:
	print("Queue file does not exist. Generating...")

if generate_queue_file:
	with open(queue_file, 'w') as outfile:
		for counter in range(number_of_runs):
			c_string = str(counter+1).zfill(number_of_digits)
			filename = os.path.join(pbs_dir,"4_PRODUCTION-NVT_{0}.pbs\n".format(c_string))
			outfile.write("qsub " + filename)
	os.system("chmod +x " + queue_file)

#
# CHECKPOINT FILES
#
print("\nCheck files...")

input = os.path.join('checkpoints','3_eq-so2.cdl')
output = os.path.join(checks_dir,'4.cdl')
rst_in = input.split('.')[0] + '.rst'
rst_out_str = output.split('.')[0] + "_"

if (not os.path.exists(input)):
	if (os.path.exists(rst_in)):
		os.system("ncdump " + rst_in + " > " + input)
	else:
		print("check input files")
		sys.exit()

position_line = 2281
velocity_line = 4526

overwrite_chk_files = False
counter = 0
for counter in range(number_of_runs):
	c_string = str(counter+1).zfill(number_of_digits)
	local_filename = "4_{0}.rst".format(c_string)
	filename = os.path.join(checks_dir, local_filename)
	answer = ""
	if os.path.exists(filename) and (not overwrite_chk_files):
		while (answer != "y") and (answer != "n"):
			answer = raw_input("Check file exists. Would you like to overwrite all check files? (y/n)\n")
		if answer == 'y':
			overwrite_chk_files = True
		else:
			break
	
	with open(input, 'r') as textfile:
		lines = textfile.readlines()
	
	velocity_string = str(-float(counter)/10 - 0.1)

	if len(lines) > velocity_line + 3:
		line1 = lines[velocity_line].split(',')
		line2 = lines[velocity_line + 1].split(',')
		line3 = lines[velocity_line + 2].split(',')
		xyS  = string.join(line1[:2], ',') + ','
		xyO1 = string.join(line2[:2], ',') + ','
		xyO2 = string.join(line3[:2], ',') + ','
		lines[velocity_line]     = xyS + velocity_string + ',\n'
		lines[velocity_line + 1] = xyO1 + velocity_string + ',\n'
		lines[velocity_line + 2] = xyO2 + velocity_string + ' ;\n'

	with open(output, 'w') as outfile:
		outfile.writelines(lines)

	os.system("ncgen -o " + rst_out_str + c_string + ".rst " + output)
	os.system("rm " + output)
os.system("rm " + input)

#
# PBS FILES
#
print("\nPBS files...")

overwrite_pbs_files = False
counter = 0
for counter in range(number_of_runs):
	c_string = str(counter+1).zfill(number_of_digits)
	local_filename = "4_PRODUCTION-NVT_{0}.pbs".format(c_string)
	filename = os.path.join(pbs_dir, local_filename)
	input = ""
	if os.path.exists(filename) and (not overwrite_pbs_files):
		while (input != "y") and (input != "n"):
			input = raw_input("PBS file exists. Would you like to overwrite all PBS files? (y/n)\n")
		if input == 'y':
			overwrite_pbs_files = True
		else:
			break
	with open(filename, 'w') as outfile:
		outfile.write("""#!/bin/bash
#PBS -l nodes=1:ppn=8,walltime=48:00:00
#PBS -o logs/job.out
#PBS -e logs/job.err
NCPU=`wc -l < $PBS_NODEFILE`
NNODES=`uniq $PBS_NODEFILE | wc -l`
cd $PBS_O_WORKDIR

""")
		chk_in = os.path.join(checks_dir,'4_{0}.rst'.format(c_string))
		chk_out = os.path.join(checks_dir,'4_{0}.rst'.format(c_string))
		ptraj_out = os.path.join(trajectories_dir,'4_{0}.mdcrd'.format(c_string))
		md_out = os.path.join(trajectories_dir, '4_{0}.out'.format(c_string))

		outfile.write("mpirun -n ${{NCPU}} /opt/amber14/bin/sander.MPI -O -i md_inputs/4_production.in -o {md_out} -p md_inputs/water_so2.prmtop -c {chk_in} -r {chk_out} -x {ptraj}".format(md_out=md_out, chk_in=chk_in, chk_out=chk_out, ptraj=ptraj_out))
