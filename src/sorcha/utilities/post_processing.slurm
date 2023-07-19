#!/bin/bash
#SBATCH --job-name=postproc
#SBATCH --account=astro
#SBATCH --partition=astro
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=28
#SBATCH --time=30:00:00
#SBATCH --mem=250G
#SBATCH --chdir=/path/

source activate oif-dev

## same as objectsInField.slurm

config_list=pp_batch_lists/pp_slurm_batch_$(printf %03d ${SLURM_ARRAY_TASK_ID})
n=$(wc -l < "$config_list")

i=1
while [ $i -le $n ]
do
	config_name=$(head -$i $config_list | tail -1)
	python post_proc/sorcha.py -c PPconfigs/$config_name &
	((i++))
done
wait

