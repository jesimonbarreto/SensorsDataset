#!/bin/bash
#SBATCH --qos=cpu
#SBATCH -o ./../2-residuals/slurm/%J.out
#SBATCH --mem=100GB 

if [ $# -lt 1 ]
  then
    echo "No sufficient arguments supplied."
    exit
fi


#conda remove --name frankdataset --all 
conda env create -f environment.yml
source activate frankdataset 
conda info --envs 

DEBUG=$1

srun python ./experimento_1.py --debug $DEBUG