#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=2


srun --exclusive -N1 -n1 -c1 oif -f ../../tests/data/config_test1.ini > ../../tests/data/oif_test1.txt &
srun --exclusive -N1 -n1 -c1 oif -f ../../tests/data/config_test2.ini > ../../tests/data/oif_test2.txt &
wait
rm -r ../../tests/data/_cache
wait
