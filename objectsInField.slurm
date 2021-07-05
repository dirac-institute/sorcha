#!/bin/bash
#SBATCH --job-name=oif
#SBATCH --account=astro
#SBATCH --partition=astro
#SBATCH --nodes=1

## This amount of memory and time was enough for 10000 objects / core over 10 years
## Unknown how much leeway this gives

#SBATCH --ntasks-per-node=28
#SBATCH --time=10:00:00
#SBATCH --mem=120G

#SBATCH --chdir=/path-to-oif/

source activate oif-dev

## Feed the script a text file with config file names
## For multiple files include an integer in the file names
## that can be fed to the script with the --array option

config_list=astro_batch_lists/astro_slurm_batch_$(printf %02d ${SLURM_ARRAY_TASK_ID})
n=$(wc -l < "$config_list")

i=1
while [ $i -le $n ]
do
	config_name=$(head -$i $config_list | tail -1)
	oif -f all_configs/$config_name &
	((i++))
done
wait
