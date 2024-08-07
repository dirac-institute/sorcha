# A basic script Jeremy hacked together to run cProfile on a subset of
# 1000 TNOs.

import cProfile
import pstats
import os
from pathlib import Path

from pstats import SortKey
from sorcha.sorcha import runLSSTSimulation  # noqa: F401
from sorcha.modules.PPConfigParser import PPConfigFileParser
from sorcha.utilities.sorchaArguments import sorchaArguments
import argparse

if __name__ == "__main__":  # pragma: no cover
    # Parse the command line arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument("--object_type", default="mba", help="The type of objects to test (mba or tno).")
    args = parser.parse_args()

    # get path to Sorcha top-level folder
    path_to_file = os.path.abspath(__file__)
    path_to_sorcha = str(Path(path_to_file).parents[1])
    
    print(path_to_sorcha)

    cmd_args_dict = {
        "paramsinput": os.path.join(path_to_sorcha, f"demo/{args.object_type}_sample_1000_physical.csv"),
        "orbinfile": os.path.join(path_to_sorcha, f"demo/{args.object_type}_sample_1000_orbit.csv"),
        "oifoutput": os.path.join(path_to_sorcha, f"demo/{args.object_type}_sample_1000_eph.csv"),
        "configfile": os.path.join(path_to_sorcha, "benchmarks/test_bench_config.ini"),
        "pointing_database": os.path.join(path_to_sorcha, "demo/baseline_v2.0_1yr.db"),
        "outpath": os.path.join(path_to_sorcha, "tests/out"),
        "outfilestem": os.path.join(path_to_sorcha, f"out_{args.object_type}"),
        "verbose": False,
        "surveyname": "rubin_sim",
        "stats": None
    }

    args_obj = sorchaArguments(cmd_args_dict)

    configs = PPConfigFileParser(os.path.join(path_to_sorcha, "benchmarks/test_bench_config.ini"), "LSST")

    cProfile.run("runLSSTSimulation(args_obj, configs)", os.path.join(path_to_sorcha, "tests/out/restats"))

    p = pstats.Stats(os.path.join(path_to_sorcha, "tests/out/restats"))
    p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats()
