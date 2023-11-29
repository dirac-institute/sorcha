import os
import sys
import logging
import glob
from .PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


def warn_or_remove_file(filepath, force_remove, pplogger):
    """Given a path to a file(s), first determine if the file exists. If it does not
    exist, pass through.

    If the file does exist check if the user has set `--force` on the command line.
    If the user set --force, log that the existing file will be removed.
    Otherwise, warn the user that the file exists and exit the program.

    Parameters
    ----------
    filepath : str
        The full file path to a given file. i.e. /home/data/output.csv
    force_remove : bool
        Whether to remove the file if it exists.
    pplogger : Logger
        Used to log the output.
    """
    file_exists = glob.glob(filepath)

    if file_exists and force_remove:
        pplogger.info(f"Existing file found at {filepath}. -f flag set: deleting existing file.")
        os.remove(file_exists[0])
    elif file_exists and not force_remove:
        pplogger.error(
            f"ERROR: existing file found at output location {filepath}. Set -f flag to overwrite this file."
        )
        sys.exit(
            f"ERROR: existing file found at output location {filepath}. Set -f flag to overwrite this file."
        )


def PPCommandLineParser(args):
    """
    Parses the command line arguments, error-handles them, then stores them in a single dict.

    Will only look for the comet parameters file if it's actually given at the command line.

    Parameters:
    -----------
    args (ArgumentParser object): argparse object of command line arguments

    Returns:
    ----------
    cmd_args_dict (dictionary): dictionary of variables taken from command line arguments

    """

    pplogger = logging.getLogger(__name__)

    cmd_args_dict = {}

    cmd_args_dict["paramsinput"] = PPFindFileOrExit(args.p, "-p, --params")
    cmd_args_dict["orbinfile"] = PPFindFileOrExit(args.ob, "-ob, --orbit")
    cmd_args_dict["configfile"] = PPFindFileOrExit(args.c, "-c, --config")
    cmd_args_dict["outpath"] = PPFindFileOrExit(args.o, "-o, --outfile")
    cmd_args_dict["pointing_database"] = PPFindFileOrExit(args.pd, "-pd, --pointing_database")

    if args.cp:
        cmd_args_dict["complex_physical_parameters"] = PPFindFileOrExit(
            args.cp, "-cp, --complex_physical_parameters"
        )

    # if the user didn't provide oifoutput on the CLI, this will default to None
    cmd_args_dict["oifoutput"] = args.er

    # if the user didn't provide output_ephemeris_file on the CLI, this will default to None
    cmd_args_dict["output_ephemeris_file"] = args.ew

    # if a value was provided, warn the user about overwriting if the file exists
    if cmd_args_dict["output_ephemeris_file"]:
        warn_or_remove_file(cmd_args_dict["output_ephemeris_file"], args.f, pplogger)

    cmd_args_dict["surveyname"] = args.s
    cmd_args_dict["outfilestem"] = args.t
    cmd_args_dict["verbose"] = args.v

    cmd_args_dict["ar_data_path"] = args.ar  # default value for args.ar is `None`.
    if cmd_args_dict["ar_data_path"]:
        PPFindDirectoryOrExit(cmd_args_dict["ar_data_path"], "-ar, --ar_data_path")

    warn_or_remove_file(
        os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*"), args.f, pplogger
    )

    # Log all the command line settings to INFO.
    for flag, value in cmd_args_dict.items():
        pplogger.info(f"Using commandline setting {flag} = {value}")

    return cmd_args_dict
