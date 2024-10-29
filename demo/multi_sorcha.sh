#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --account=my_account
#SBATCH --partition=my_partition
#SBATCH --ntasks=10                  # Run a single task
#SBATCH --mem=40gb                   # Job Memory
#SBATCH --time=2:00:00             # Time limit hrs:min:sec
#SBATCH --output=log-%a.log    # Standard output and error log

python3 multi_sorcha.py --config my_config.ini --input_orbits my_orbits.csv --input_physical my_colors.csv --pointings my_pointings.db --path ./ --chunksize $(($1 * $2)) --norbits $1 --cores $2 --instance ${SLURM_ARRAY_TASK_ID} --cleanup --copy_inputs
