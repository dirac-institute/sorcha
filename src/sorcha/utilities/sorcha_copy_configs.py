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

    if which_configs == "rubin_circle":
        config_locations = ["Rubin_circular_approximation.ini"]
    elif which_configs == "rubin_footprint":
        config_locations = ["Rubin_full_footprint.ini"]
    elif which_configs == "all":
        config_locations = ["Rubin_circular_approximation.ini", "Rubin_full_footprint.ini"]
    else:
        sys.exit(
            "String '{}' not recognised for 'configs' variable. Must be 'rubin_circle', 'rubin_footprint' or 'all'.".format(
                which_configs
            )
        )

    for config in config_locations:
        config_path = os.path.join(path_to_surveys, config)

        if not force_overwrite and os.path.isfile(os.path.join(copy_location, config)):
            sys.exit(
                "Identically named file exists at location. Re-run with -f or --force to force overwrite."
            )

        shutil.copy(config_path, copy_location)

    print("Example configuration files {} copied to {}.".format(config_locations, copy_location))
