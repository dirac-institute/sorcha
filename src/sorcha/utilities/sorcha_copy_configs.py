import os
import argparse
from pathlib import Path
import shutil
import sys

from sorcha.modules.PPConfigParser import PPFindDirectoryOrExit


def copy_demo_configs(copy_location, which_configs):
    """
    Copies the example Sorcha configuration files to a user-specified location.

    Parameters
    -----------
    copy_location : string
        String containing the filepath of the location to which the configuration files should be copied.

    which_configs : string
        String indicating which configuration files to retrieve. Should be "rubin", "demo" or "all".

    Returns
    -----------
    None

    """

    _ = PPFindDirectoryOrExit(copy_location, "filepath")

    path_to_file = os.path.abspath(__file__)

    path_to_surveys = os.path.join(str(Path(path_to_file).parents[3]), "survey_setups")
    path_to_demo = os.path.join(str(Path(path_to_file).parents[3]), "demo")

    if which_configs == "rubin":
        config_locations = [
            os.path.join(path_to_surveys, "Rubin_circular_approximation.ini"),
            os.path.join(path_to_surveys, "Rubin_full_footprint.ini"),
        ]
    elif which_configs == "demo":
        config_locations = [os.path.join(path_to_demo, "sorcha_config_demo.ini")]
    elif which_configs == "all":
        config_locations = [
            os.path.join(path_to_surveys, "Rubin_circular_approximation.ini"),
            os.path.join(path_to_surveys, "Rubin_full_footprint.ini"),
            os.path.join(path_to_demo, "sorcha_config_demo.ini"),
        ]
    else:
        sys.exit(
            "String '{}' not recognised for 'configs' variable. Must be 'rubin', 'demo' or 'all'.".format(
                which_configs
            )
        )

    for config in config_locations:
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

    selection_dict = {1: "rubin", 2: "demo", 3: "all"}

    which_configs = selection_dict[file_select]

    return which_configs


def main():
    """
    Copies example configuration files for Sorcha from the installation location
    to a user-specified location. Controlled via command-line input from the user.

    Parameters
    -----------
    None

    Returns
    -----------
    None

    """

    print("\nWhich configuration files would you like to copy?:\n")
    print("1. Rubin-specific configuration files.\n")
    print("2. Basic demo configuration file.\n")
    print("3. All.\n")
    file_select = input("Please enter a number and hit Return/Enter.\n")

    which_configs = parse_file_selection(file_select)

    print("\nWhere would you like the configuration files to be copied to?\n")
    copy_location = input("Enter a filepath, or simply . to copy to this location.\n")

    copy_location = os.path.abspath(copy_location)
    copy_demo_configs(copy_location, which_configs)


if __name__ == "__main__":
    main()
