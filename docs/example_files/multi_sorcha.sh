#!/bin/bash
#SBATCH --job-name=the_best_job
#SBATCH --account=im_a_power_user
#SBATCH --partition=the_best_partition
#SBATCH --mem=all_of_it
#SBATCH --time=24:00:00
#SBATCH --output=log-%a.log

python3 multi_sorcha.py --config my_config.ini --input_orbits my_orbits.csv --input_physical my_colors.csv --pointings my_pointings.db --path ./ --chunksize $1 --cores $2 --instance ${SLURM_ARRAY_TASK_ID} --cleanup 