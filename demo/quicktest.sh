#!/bin/bash
#
# A quick test run to check the newly built code works as expected.
#
# It's lightweight and intented to be packaged with the binaries (e.g., in
# conda packages) so it can be automatically run during package builds and
# on the end-user's system (to test the install).
#

set -e

trap '{ rm -f quicktest-result.*; } ' EXIT

test -d demo || { echo "$0 must be run from the top-level source code directory"; exit -1; }

rm -f quicktest-result.*

sorcha bootstrap
sorcha run -c ./demo/sorcha_config_demo.ini -p ./demo/sspp_testset_colours.txt -ob ./demo/sspp_testset_orbits.des -pd ./demo/baseline_v2.0_1yr.db -o ./ -t quicktest-result -st quicktest-result.stats

# check that the output file size is larger than ~10k
# (NOTE: this is just a rough check, we should test against known output here!)
filesize=$(wc -c quicktest-result.csv | awk '{print $1}')
test $filesize -gt 10000

# check that the stats file exists
test -f quicktest-result.stats.csv

echo "Quick test succesful!"
