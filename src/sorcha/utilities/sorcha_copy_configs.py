import os
import argparse
from pathlib import Path
import shutil
import sys

from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit


def copy_demo_configs(copy_location, which_configs, force_overwrite):
    """
    Copies the example Sorcha configuration files to a user-specified location.

    Parameters
    -----------
    copy_location : string
        String containing the filepath of the location to which the configuration files should be copied.

    which_configs : string
        String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".

    force_overwrite: boolean
        Flag for determining whether existing files should be overwritten.

    Returns
    -----------
    None

    """

    _ = PPFindDirectoryOrExit(copy_location, "filepath")

    path_to_file = os.path.abspath(__file__)

    path_to_surveys = os.path.join(str(Path(path_to_file).parents[3]), "survey_setups")
    path_to_demo = os.path.join(str(Path(path_to_file).parents[3]), "demo")

    if which_configs == "rubin_circle":
        config_locations = [os.path.join(path_to_surveys, "Rubin_circular_approximation.ini")]
    elif which_configs == "rubin_footprint":
        config_locations = [os.path.join(path_to_surveys, "Rubin_full_footprint.ini")]
    elif which_configs == "all":
        config_locations = [
            os.path.join(path_to_surveys, "Rubin_circular_approximation.ini"),
            os.path.join(path_to_surveys, "Rubin_full_footprint.ini"),
        ]
    else:
        sys.exit(
            "String '{}' not recognised for 'configs' variable. Must be 'rubin_circle', 'rubin_footprint' or 'all'.".format(
                which_configs
            )
        )

    for config in config_locations:
        if not force_overwrite and os.path.isfile(config):
            sys.exit("Identical file exists at location. Re-run with -f or --force to force overwrite.")

        shutil.copy(config, copy_location)

    print("Example configuration files {} copied to {}.".format(config_locations, copy_location))


def parse_file_selection(file_select):
    """Turns the number entered by the user at the command line into a string
    prompt. Also performs error handling.

    Parameters
    -----------
    file_select : int
        Integer entered by the user at command line.

    Returns
    -----------
    which_configs : string
        String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".

    """

    try:
        file_select = int(file_select)
    except ValueError:
        sys.exit("Input could not be converted to a valid integer. Please try again.")

    if file_select not in [1, 2, 3]:
        sys.exit("Input could not be converted to a valid integer. Please input an integer between 1 and 3.")

    selection_dict = {1: "rubin_circle", 2: "rubin_footprint", 3: "all"}

    which_configs = selection_dict[file_select]

    return which_configs


def main():
    """
    Copies example configuration files for Sorcha from the installation location
    to a user-specified location. Filepath to copy files to is specified by command-line
    flag. Selection of configuration files is done via user input.

    usage: sorcha_copy_configs [-h] [-p PATH]
        arguments:
          -h, --help                                  Show this help message and exit.
          [-p PATH, --path PATH]          Filepath where you want to copy the config files. Default is current working directory.

    Parameters
    -----------
    None

    Returns
    -----------
    None

    """

    parser = argparse.ArgumentParser(
        description="Copies example Sorcha configuration files to a user-specified location."
    )

    parser.add_argument(
        "-p",
        "--path",
        help="Filepath where you want to copy the config files. Default is current working directory.",
        type=str,
        default="./",
    )

    parser.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing config file(s). Default False.",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    print("\nWhich configuration file(s) would you like to copy?:\n")
    print("1. Rubin-specific configuration file using circular approximation of camera footprint (faster).\n")
    print("2. Rubin-specific configuration file using full camera footprint (slower, but more accurate).\n")
    print("3. All.\n")
    file_select = input("Please enter a number and hit Return/Enter.\n")

    which_configs = parse_file_selection(file_select)

    copy_location = os.path.abspath(args.path)
    copy_demo_configs(copy_location, which_configs, args.force)


if __name__ == "__main__":
    main()
