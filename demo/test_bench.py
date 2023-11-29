import cProfile
import pstats

from pstats import SortKey
from sorcha.sorcha import runLSSTSimulation  # noqa: F401
from sorcha.modules.PPConfigParser import PPConfigFileParser
import argparse

# Run this from the command line using:
# python .../demo/test_bench.py

if __name__ == "__main__":  # pragma: no cover
    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--object_type", default="mba", help="The type of objects to test (mba or tno).")
    args = parser.parse_args()

    cmd_args_dict = {
        "paramsinput": "./demo/mba_sample_1000_physical.csv",
        "orbinfile": "./demo/mba_sample_1000_orbit.csv",
        "output_ephemeris_file": "ephemeris_output.csv",
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

    debug = False
    if debug:
        runLSSTSimulation(cmd_args_dict, configs)
    else: # benchmark
        cProfile.run("runLSSTSimulation(cmd_args_dict, configs)", "./data/out/restats")

        p = pstats.Stats("./data/out/restats")
        p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(100)
