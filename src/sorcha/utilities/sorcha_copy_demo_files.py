import os
import argparse
from pathlib import Path
import shutil
import sys
from importlib.resources import files

from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit
from sorcha.utilities.sorcha_demo_command import print_demo_command


def copy_demo_files(copy_location, force_overwrite):
    """
    Copies the files needed to run the Sorcha demo to a user-specified location.

    Parameters
    -----------
    copy_location : string
        String containing the filepath of the location to which the configuration files should be copied.

    force_overwrite : boolean
        Flag for determining whether existing files should be overwritten.

    Returns
    -----------
    None

    """

    _ = PPFindDirectoryOrExit(copy_location, "filepath")

    demo_data_root = files("sorcha.data.demo")

    demo_files = [
        "sorcha_config_demo.ini",
        "sspp_testset_colours.txt",
        "sspp_testset_orbits.des",
        "baseline_v2.0_1yr.db",
    ]

    for fn in demo_files:
        if not force_overwrite and os.path.isfile(os.path.join(copy_location, fn)):
            sys.exit(
                "Identically named file exists at location. Re-run with -f or --force to force overwrite."
            )

        demo_path = demo_data_root.joinpath(fn)
        shutil.copy(demo_path, copy_location)

    print("Demo files {} copied to {}.".format(demo_files, copy_location))

    print_demo_command(printall=False)
