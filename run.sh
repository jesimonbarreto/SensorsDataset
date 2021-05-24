#!/bin/bash
#SBATCH -N 1
#SBATCH --qos=cpu
#SBATCH -o ./../2-residuals/slurm/%J.out
#SBATCH --mem=100GB 

#conda remove --name frankdataset --all 
conda env create -f environment.yml
source activate frankdataset 
conda info --envs 


srun python ./experimento_1.py