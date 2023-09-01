from sorcha.sorcha import runAll  # noqa: F401
from sorcha.modules.PPConfigParser import PPConfigFileParser
import argparse

if __name__ == "__main__":  # pragma: no cover
    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--object_type", default="mba", help="The type of objects to test (mba or tno).")
    args = parser.parse_args()

    cmd_args_dict = {
        "paramsinput": "./data_files/mpcorb_physical.csv",
        "orbinfile": "./data_files/mpcorb_orbits.csv",
        "orbinfile": "./data_files/mpcorb_orbits_small.csv",
        "oifoutput": "./data/out/ephemeris_output.csv",
        "configfile": "./demo/test_bench_config.ini",
        "pointing_database": "./demo/baseline_v2.0_1yr.db",
        "outpath": "./data/out",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": "out_mpcorb",
        "verbose": False,
    }

    configs = PPConfigFileParser("./demo/test_bench_config.ini", "LSST")

    runAll(cmd_args_dict, configs)