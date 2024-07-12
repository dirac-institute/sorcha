import os
import sys
import logging
import glob
from .PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


def warn_or_remove_file(filepath, force_remove, pplogger, exclude_remove=[]):
    """Given a path to a file(s), first determine if the file exists. If it does not
    exist, pass through.

    If the file does exist check if the user has set `--force` on the command line.
    If the user set --force, log that the existing file will be removed.
    Otherwise, warn the user that the file exists and exit the program.

    Parameters
    ----------
    filepath : string
        The full file path to a given file. i.e. /home/data/output.csv
    force_remove : boolean
        Whether to remove the file if it exists.
    pplogger : Logger
        Used to log the output.
    exclude_remove: list
        Files that shouldn't be removed (used to keep the log file)
    """
    exclude_remove = set([os.path.normpath(fn) for fn in exclude_remove])
    file_exists = set(map(os.path.normpath, glob.glob(filepath))) - exclude_remove

    if file_exists and force_remove:
        pplogger.info(f"Existing file(s) found at {file_exists}. --force flag set: deleting existing file.")
        for fn in file_exists:
            os.remove(fn)
    elif file_exists and not force_remove:
        msg = f"ERROR: files found that would be overwritten by output: {file_exists}. Set --force flag to overwrite this file."
        pplogger.error(msg)
        sys.exit(msg)


def PPCommandLineParser(args):
    """
    Parses the command line arguments, error-handles them, then stores them in a single dict.

    Will only look for the comet parameters file if it's actually given at the command line.

    Parameters
    -----------
    args : ArgumentParser object
        argparse object of command line arguments

    Returns
    ----------
    cmd_args_dict : dictionary
        dictionary of variables taken from command line arguments

    """

    pplogger = logging.getLogger(__name__)

    cmd_args_dict = {}

    cmd_args_dict["paramsinput"] = PPFindFileOrExit(args.colors, "--colors")
    cmd_args_dict["orbinfile"] = PPFindFileOrExit(args.orbits, "--orbits")
    cmd_args_dict["configfile"] = PPFindFileOrExit(args.config, "-c, --config")
    cmd_args_dict["outpath"] = PPFindFileOrExit(args.output_dir, "-o, --output-dir")
    cmd_args_dict["pointing_database"] = PPFindFileOrExit(args.pointings, "--pointings")

    if args.extra_object_data:
        cmd_args_dict["extra_object_data"] = PPFindFileOrExit(args.extra_object_data, "--extra-object-data")

    # if the user didn't provide oifoutput on the CLI, this will default to None
    cmd_args_dict["oifoutput"] = args.ephem_input

    # if the user didn't provide output_ephemeris_file on the CLI, this will default to None
    cmd_args_dict["output_ephemeris_file"] = args.ephem_output

    # if a value was provided, warn the user about overwriting if the file exists
    if cmd_args_dict["output_ephemeris_file"]:
        warn_or_remove_file(
            os.path.join(cmd_args_dict["outpath"], cmd_args_dict["output_ephemeris_file"] + ".*"),
            args.force,
            pplogger,
            [args.log_file],
        )

    cmd_args_dict["surveyname"] = args.survey
    cmd_args_dict["outfilestem"] = args.prefix
    cmd_args_dict["verbose"] = args.verbose
    cmd_args_dict["stats"] = args.prefix + "-stats" if args.stats else None

    if cmd_args_dict["stats"] is not None:
        warn_or_remove_file(
            os.path.join(cmd_args_dict["outpath"], cmd_args_dict["stats"] + ".csv"),
            args.force,
            pplogger,
            [args.log_file],
        )

    cmd_args_dict["ar_data_path"] = args.integrator_data  # default value for args.ar is `None`.
    if cmd_args_dict["ar_data_path"]:
        PPFindDirectoryOrExit(cmd_args_dict["ar_data_path"], "--integrator_data")

    warn_or_remove_file(
        os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*"),
        args.force,
        pplogger,
        [args.log_file],
    )

    # Log all the command line settings to INFO.
    for flag, value in cmd_args_dict.items():
        pplogger.info(f"Using commandline setting {flag} = {value}")

    return cmd_args_dict
