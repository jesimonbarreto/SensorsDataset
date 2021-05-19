#!/bin/bash
#SBATCH -N 1
#SBATCH --qos=cpu
#SBATCH -o ./../2-residuals/slurm/%J.out
#SBATCH --mem=15GB 

conda env create env_keras220.yml 

source activate frankdataset 


srun python ./experimento_1.py