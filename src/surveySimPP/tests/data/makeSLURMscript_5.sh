#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=2


srun --exclusive -N1 -n1 -c1 oif -f ../../tests/data/config_test1.ini > ../../tests/data/oif_test1.txt &
srun --exclusive -N1 -n1 -c1 oif -f ../../tests/data/config_test2.ini > ../../tests/data/oif_test2.txt &
wait
rm -r ../../tests/data/_cache
wait
mkdir ../../tests/data/test1
srun --exclusive -N1 -n1 -c1 surveySimPP -c ../../tests/data/test_PPConfig.ini -p ../../tests/data/params_test1.txt -o ../../tests/data/orbits_test1.txt -e ../../tests/data/oif_test1.txt -u ../../tests/data/test1 -t test1 -dw -dl & 
mkdir ../../tests/data/test2
srun --exclusive -N1 -n1 -c1 surveySimPP -c ../../tests/data/test_PPConfig.ini -p ../../tests/data/params_test2.txt -o ../../tests/data/orbits_test2.txt -e ../../tests/data/oif_test2.txt -u ../../tests/data/test2 -t test2 -dw -dl & 
wait
