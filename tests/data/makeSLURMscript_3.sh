#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=2


rm -r ../data/_cache
wait
mkdir ../data/test1
srun --exclusive -N1 -n1 -c1 sorcha -c ../data/test_PPConfig.ini -p ../data/params_test1.txt -o ../data/orbits_test1.txt -e ../data/oif_test1.txt -u ../data/test1 -t test1 & 
mkdir ../data/test2
srun --exclusive -N1 -n1 -c1 sorcha -c ../data/test_PPConfig.ini -p ../data/params_test2.txt -o ../data/orbits_test2.txt -e ../data/oif_test2.txt -u ../data/test2 -t test2 & 
wait
