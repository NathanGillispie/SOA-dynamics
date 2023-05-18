#! /bin/bash
cpptraj ./md_inputs/water_solvated.prmtop ./ptraj/SO2.ptrajin
mv diffusion* ptraj
