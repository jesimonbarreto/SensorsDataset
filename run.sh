#!/bin/bash
#SBATCH -N 1
#SBATCH --qos=Medium
#SBATCH -o ./../out_slurm/%J.out
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8

# comment SBATCH --partition=projects
# comment conda remove --name envi --all
conda info --envs
hostname
module load cuda/9.0
#module load cuda/8.0
module load cudnn/7.0.5
#module load cudnn/6.0.21
conda remove --name pix_hell --all
conda env create --force -f env_keras220.yml 
#conda env update -f jesienv.yml

source activate pix_hell2 

conda info --envs

srun python ./main.py /storage/datasets/sensors/WISDM_ar_v1.1/WISDM_ar_v1.1_raw.txt /storage/datasets/JB/sensors/wisdm/ /storage/datasets/JB/sensors/loso/