# md_inputs

Heating file with comments:

```
Heating--Water nstlim default 150000
&cntrl
imin=0,
irest=0,
ntb=1, (ntb 1: constant V 2: constant P)
iwrap=1, (periodic boundary conditions)
ntx=1, (input coords are ascii)
ntxo=2, (output coords are NetCDF)
nstlim=200000, (number of steps)
dt=0.001, (dt in ns)
cut=8.0, (nonbonded cutoff Angstroms)
ntf=2,ntc=2, 
ntt=3, (Langevin thermostat)
ig=-1, (random seed)
gamma_ln=2.0, (collision frequency, only for t regulation)
tempi=0.0, 
temp0=300.0, 
ntpr=50, (save coords every 50 dt)
ntwx=50
/
```
