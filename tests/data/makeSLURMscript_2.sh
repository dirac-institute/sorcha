#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=2


srun --exclusive -N1 -n1 -c1 oif -f ../data/config_test1.ini > ../data/oif_test1.txt &
srun --exclusive -N1 -n1 -c1 oif -f ../data/config_test2.ini > ../data/oif_test2.txt &
wait
rm -r ../data/_cache
wait
