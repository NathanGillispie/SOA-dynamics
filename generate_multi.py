import string
import os
import math

number_of_runs = 10
number_of_digits = int(math.ceil(math.log10(number_of_runs)))+1 

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
		outfile.write("mpirun -n ${{NCPU}} /opt/amber14/bin/sander.MPI -O -i md_inputs/4_production.in -o {md_out} -p md_inputs/water_so2.prmtop -c {chk_in} -r {chk_out} -x {ptraj}".format(md_out="md_outputs/4.out",chk_in="checkpoints/4.rst",chk_out="checkpoints/4.rst",ptraj="ptraj/4.mdcrd"))
		
