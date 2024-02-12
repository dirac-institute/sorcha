import os
import argparse
from pathlib import Path
import shutil
import sys

from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit


def copy_demo_files(copy_location, force_overwrite):
    """
    Copies the files needed to run the Sorcha demo to a user-specified location.

    Parameters
    -----------
    copy_location : string
        String containing the filepath of the location to which the configuration files should be copied.

    force_overwrite: boolean
        Flag for determining whether existing files should be overwritten.

    Returns
    -----------
    None

    """

    _ = PPFindDirectoryOrExit(copy_location, "filepath")

    path_to_file = os.path.abspath(__file__)

    path_to_demo = os.path.join(str(Path(path_to_file).parents[3]), "demo")

    demo_files = [
        "sorcha_config_demo.ini",
        "sspp_testset_colours.txt",
        "sspp_testset_orbits.des",
        "baseline_v2.0_1yr.db",
    ]

    for filename in demo_files:
        if not force_overwrite and os.path.isfile(os.path.join(copy_location, filename)):
            sys.exit(
                "Identically named file exists at location. Re-run with -f or --force to force overwrite."
            )

        demo_path = os.path.join(path_to_demo, filename)
        shutil.copy(demo_path, copy_location)

    print("Demo files {} copied to {}.".format(demo_files, copy_location))


def main():
    """
    Copies demo files for Sorcha from the installation location
    to a user-specified location. Filepath to copy files to is specified by command-line
    flag.

    usage: sorcha_copy_demo_files [-h] [-p PATH]
        arguments:
          -h, --help                                  Show this help message and exit.
          [-p PATH, --path PATH]          Filepath where you want to copy the demo files. Default is current working directory.

    Parameters
    -----------
    None

    Returns
    -----------
    None

    """

    parser = argparse.ArgumentParser(
        description="Copies files for demo Sorcha run to a user-specified location."
    )

    parser.add_argument(
        "-p",
        "--path",
        help="Filepath where you want to copy the demo files. Default is current working directory.",
        type=str,
        default="./",
    )

    parser.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing demo file(s). Default False.",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    copy_location = os.path.abspath(args.path)
    copy_demo_files(copy_location, args.force)


if __name__ == "__main__":
    main()
