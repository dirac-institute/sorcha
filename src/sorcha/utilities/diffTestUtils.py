import numpy as np
import os
import tempfile

from shutil import copyfile

from sorcha.sorcha import runLSSTPostProcessing
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath, get_data_out_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments


def compare_result_files(test_output, golden_output):
    """Compare the results in test_output to those in golden_output.

    Parameters
    ----------
    test_output (str): The path and file name of the test results.

    golden_output (str): The path and file name of the golden set results.

    Returns
    -------
    bool : Indicates whether the results are the same.
    """
    test_data = np.genfromtxt(test_output, delimiter=",", dtype=str, skip_header=1)
    golden_data = np.genfromtxt(golden_output, delimiter=",", dtype=str, skip_header=1)
    if np.shape(test_data) != np.shape(golden_data):
        return False
    print(np.shape(test_data))
    (num_rows, num_cols) = np.shape(test_data)

    # Check each column, casting to float and using 'close' matches when possible
    # and exact string matches otherwise.
    for c in range(num_cols):
        if np.can_cast(test_data[0][c], float):
            if not np.allclose(test_data[:, c].astype(float), golden_data[:, c].astype(float)):
                return False
        else:
            if not np.all(test_data[:, c] == golden_data[:, c]):
                return False
    return True


def override_seed_and_run(outpath):
    """Run the full Rubin sim on the demo data and a fixed seed.

    WARNING: Never use a fixed seed for scientific analysis. This is
    for testing purposes only.

    Parameters
    ----------
    outpath (str): The path for the output files.
    """

    cmd_args_dict = {
        "paramsinput": get_demo_filepath("sspp_testset_colours.txt"),
        "orbinfile": get_demo_filepath("sspp_testset_orbits.des"),
        "oifoutput": get_demo_filepath("example_oif_output.txt"),
        "configfile": get_demo_filepath("PPConfig_test.ini"),
        "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
        "outpath": outpath,
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": f"out_end2end",
        "verbose": False,
    }
    args = sorchaArguments(cmd_args_dict)

    # Override the random number generator seed.
    # WARNING: This is only accceptable in a test and should never be used for
    # science results.
    args._rng = np.random.RandomState(2023)
    runLSSTPostProcessing(args)
