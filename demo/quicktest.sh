#!/bin/bash
#
# A quick test run to check the newly built code works as expected.
#
# It's lightweight and intented to be packaged with the binaries (e.g., in
# conda packages) so it can be automatically run during package builds and
# on the end-user's system (to test the install).
#

set -e

trap "{ rm -rf \"$PWD/temp-demo-dir\"; }" EXIT

mkdir temp-demo-dir
cd temp-demo-dir

sorcha bootstrap
sorcha demo prepare

# Let's get the most recent demo command line
# (the `sed` part strips out ANSI escape sequences, see https://stackoverflow.com/a/43627833)
sorcha_demo=$(sorcha demo howto | grep 'sorcha run' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g")
echo "runnin demo command:"
echo "  $sorcha_demo"
$sorcha_demo

# check that the output file size is larger than ~10k
# (NOTE: this is just a rough check, we should test against known output here!)
filesize=$(wc -c testrun_e2e.csv | awk '{print $1}')
test $filesize -gt 10000

# check that the stats file exists
test -f testrun_stats.csv

echo "Quick test succesful!"
