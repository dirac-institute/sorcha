import os
import sys
import tempfile

from shutil import copyfile

from sorcha.utilities.diffTestUtils import override_seed_and_run
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath

if __name__ == "__main__":
    # Create a goldens directory if it does not exist.
    golden_dir = get_demo_filepath("goldens")
    if not os.path.exists(golden_dir):
        os.mkdir(golden_dir)

    # Use a temporary directory to dump logs and results.
    with tempfile.TemporaryDirectory() as dir_name:
        override_seed_and_run(dir_name, arg_set="baseline")

        res_name = os.path.join(dir_name, "out_end2end.csv")
        if not os.path.exists(res_name):
            sys.exit(f"ERROR: Unable to find output file {res_name}")

        copyfile(res_name, os.path.join(golden_dir, "out_end2end.csv"))

        override_seed_and_run(dir_name, arg_set="with_ephemeris")

        res_name = os.path.join(dir_name, "sorcha_ephemeris.csv")
        if not os.path.exists(res_name):
            sys.exit(f"ERROR: Unable to find output file {res_name}")

        copyfile(res_name, os.path.join(golden_dir, "sorcha_ephemeris.csv"))
