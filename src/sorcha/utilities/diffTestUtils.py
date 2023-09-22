import numpy as np
import pandas as pd

from pandas.api.types import is_numeric_dtype

from sorcha.modules.PPModuleRNG import PerModuleRNG
from sorcha.sorcha import runLSSTSimulation
from sorcha.utilities.dataUtilitiesForTests import get_demo_filepath
from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.modules.PPConfigParser import PPConfigFileParser


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
    test_data = pd.read_csv(test_output)
    golden_data = pd.read_csv(golden_output)

    if test_data.shape != golden_data.shape:
        return False

    # for each column, check the data type. If it's a string, do a true comparison
    # if it's a numeric type use numpy's `allclose` method to ignore machine
    # precision error.
    for col in test_data.columns.to_list():
        if is_numeric_dtype(test_data[col]):
            if not np.allclose(test_data[col], golden_data[col]):
                return False
        else:
            if not np.all(test_data[col] == golden_data[col]):
                return False
    return True


BASELINE_ARGS = {
    "paramsinput": get_demo_filepath("sspp_testset_colours.txt"),
    "orbinfile": get_demo_filepath("sspp_testset_orbits.des"),
    "oifoutput": get_demo_filepath("example_oif_output.txt"),
    "configfile": get_demo_filepath("PPConfig_test.ini"),
    "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
    "makeTemporaryEphemerisDatabase": False,
    "readTemporaryEphemerisDatabase": False,
    "deleteTemporaryEphemerisDatabase": False,
    "surveyname": "LSST",
    "outfilestem": f"out_end2end",
    "verbose": False,
}

WITH_EPHEMERIS_ARGS = {
    "paramsinput": get_demo_filepath("params_small_random_mpcorb.csv"),
    "orbinfile": get_demo_filepath("orbits_small_random_mpcorb.csv"),
    "configfile": get_demo_filepath("config_for_ephemeris_unit_test.ini"),
    "pointing_database": get_demo_filepath("baseline_v2.0_1yr.db"),
    "output_ephemeris_file": "sorcha_ephemeris.csv",
    "makeTemporaryEphemerisDatabase": False,
    "readTemporaryEphemerisDatabase": False,
    "deleteTemporaryEphemerisDatabase": False,
    "surveyname": "LSST",
    "outfilestem": f"out_end2end_with_ephemeris_generation",
    "verbose": False,
}


def override_seed_and_run(outpath, arg_set="baseline"):
    """Run the full Rubin sim on the demo data and a fixed seed.

    WARNING: Never use a fixed seed for scientific analysis. This is
    for testing purposes only.

    Parameters
    ----------
    outpath (str): The path for the output files.
    """

    if arg_set == "baseline":
        cmd_args_dict = BASELINE_ARGS
    elif arg_set == "with_ephemeris":
        cmd_args_dict = WITH_EPHEMERIS_ARGS
    else:
        raise ValueError(f"Unknown arg set name, {arg_set}. Must be one of: 'baseline', 'with_ephemeris'.")

    cmd_args_dict["outpath"] = outpath

    args = sorchaArguments(cmd_args_dict)

    # Override the random number generator seed.
    # WARNING: This is only acceptable in a test and should never be used for
    # science results.
    configs = PPConfigFileParser(args.configfile, args.surveyname)
    args._rngs = PerModuleRNG(2023)
    runLSSTSimulation(args, configs)
