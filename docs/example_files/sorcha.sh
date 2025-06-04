#!/bin/bash
#SBATCH --job-name=three_jobs_in_one
#SBATCH --account=lazy_slurm_user
#SBATCH --partition=the_bestest_partition
#SBATCH --ntasks=3
#SBATCH --mem-per-cpu=1G
#SBATCH --time=24:00:00
#SBATCH --output=log-%a.log

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt Beginning Sorcha."

srun --exclusive -N1 -n1 sorcha run -c ./sorcha_config_demo.ini --pd ./baseline_v2.0_1yr.db --ob ./sspp_testset_orbits.des -p ./sspp_testset_colours.txt -o ./ -t testrun_e2e_1 -st testrun_e2e_stats_1 & 
srun --exclusive -N1 -n1 sorcha run -c ./sorcha_config_demo.ini --pd ./baseline_v2.0_1yr.db --ob ./sspp_testset_orbits.des -p ./sspp_testset_colours.txt -o ./ -t testrun_e2e_2 -st testrun_e2e_stats_2 & 
srun --exclusive -N1 -n1 sorcha run -c ./sorcha_config_demo.ini --pd ./baseline_v2.0_1yr.db --ob ./sspp_testset_orbits.des -p ./sspp_testset_colours.txt -o ./ -t testrun_e2e_3 -st testrun_e2e_stats_3 & 
wait

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt Sorcha complete."