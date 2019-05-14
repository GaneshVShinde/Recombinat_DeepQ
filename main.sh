#!/bin/bash
#
#SBATCH --job-name=m0104z1265
#SBATCH --output=600res_omp.txt
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=07
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=12288
#SBATCH --partition=long-q12
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

python3 main.py
