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

    _ = PPFindDirectoryOrExit(copy_location, "-f, --filepath")

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


def main():
    """
    Copies example configuration files for Sorcha from the installation location
    to a user-specified location.

    usage: sorcha_copy_configs [-h] [-f FILEPATH] [-c [{rubin,demo,all}]]
        arguments:
          -h, --help                                             Show this help message and exit.
          [-f FILEPATH, --filename FILEPATH]                     Filepath where you want to copy the config files. Default is current working directory.
          [-c [{rubin,demo,all}]],--configs [{rubin,demo,all}]   Which config files you want: options are "rubin", "demo" and "all". Default is "all".
    """

    parser = argparse.ArgumentParser(
        description="Copies example Sorcha configuration files to a user-specified location."
    )

    parser.add_argument(
        "-f",
        "--filepath",
        help="Filepath where you want to copy the config files. Default is current working directory.",
        type=str,
        default="./",
    )

    parser.add_argument(
        "-c",
        "--configs",
        help="Which config files you want: options are 'rubin', 'demo' and 'all'. Default is 'all'.",
        default="all",
        const="all",
        nargs="?",
        choices=["rubin", "demo", "all"],
    )

    args = parser.parse_args()

    copy_location = os.path.abspath(args.filepath)
    which_configs = args.configs

    copy_demo_configs(copy_location, which_configs)


if __name__ == "__main__":
    main()
