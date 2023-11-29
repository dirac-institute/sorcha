#!/bin/bash
#SBATCH --job-name=test
#SBATCH --ntasks=2


mkdir ../data/orbits_test1
srun --exclusive -N1 -n1 -c1 sorcha -c ../data/test_PPConfig.ini -ob ../data/orbits_test1.txt -p ../data/params_test1.txt -pd ../data/baseline_10klines_2.0.db -o ../data/orbits_test1 -t SorchaOutput_orbits_test1 -ar ../data & 
mkdir ../data/orbits_test2
srun --exclusive -N1 -n1 -c1 sorcha -c ../data/test_PPConfig.ini -ob ../data/orbits_test2.txt -p ../data/params_test2.txt -pd ../data/baseline_10klines_2.0.db -o ../data/orbits_test2 -t SorchaOutput_orbits_test2 -ar ../data & 
wait
