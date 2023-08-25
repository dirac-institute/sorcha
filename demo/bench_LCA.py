# A basic test case for the lightcurve model

import cProfile
import pstats

from pstats import SortKey
from sorcha.sorcha import runLSSTPostProcessing  # noqa: F401
import argparse

if __name__ == "__main__":  # pragma: no cover
    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--object_type", default="mba", help="The type of objects to test (mba or tno).")
    args = parser.parse_args()

    cmd_args_dict = {
        "paramsinput": f"./{args.object_type}_sample_1000_physical_lca.csv",
        "orbinfile": f"./{args.object_type}_sample_1000_orbit.csv",
        "oifoutput": f"./{args.object_type}_sample_1000_eph.csv",
        "configfile": "./OIFconfig_benchmark.ini",
        "pointing_database": "./baseline_v2.0_1yr.db",
        "outpath": "../data/out",
        "makeTemporaryEphemerisDatabase": False,
        "readTemporaryEphemerisDatabase": False,
        "deleteTemporaryEphemerisDatabase": False,
        "surveyname": "LSST",
        "outfilestem": f"out_{args.object_type}",
        "verbose": False,
    }

    cProfile.run("runLSSTPostProcessing(cmd_args_dict)", "../data/out/restats")

    p = pstats.Stats("../data/out/restats")
    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()
