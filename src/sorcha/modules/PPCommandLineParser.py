import os
import sys
import logging
import glob
from .PPConfigParser import PPFindFileOrExit, PPFindDirectoryOrExit


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
    cmd_args_dict["orbinfile"] = PPFindFileOrExit(args.o, "-o, --orbit")
    cmd_args_dict["oifoutput"] = PPFindFileOrExit(args.e, "-e, --ephem")
    cmd_args_dict["configfile"] = PPFindFileOrExit(args.c, "-c, --config")
    cmd_args_dict["outpath"] = PPFindFileOrExit(args.u, "-u, --outfile")

    if args.cp:
        cmd_args_dict["complex_physical_parameters"] = PPFindFileOrExit(
            args.cp, "-cp, --complex_physical_parameters"
        )

    if args.dw == "default":
        oifpath_split = os.path.split(cmd_args_dict["oifoutput"])
        stem_name = oifpath_split[1].split(".")[0] + ".db"
        cmd_args_dict["makeTemporaryEphemerisDatabase"] = os.path.join(oifpath_split[0], "temp_" + stem_name)
    elif args.dw:
        _ = PPFindDirectoryOrExit(os.path.dirname(args.dw), "-dw")
        cmd_args_dict["makeTemporaryEphemerisDatabase"] = args.dw
    else:
        cmd_args_dict["makeTemporaryEphemerisDatabase"] = False

    cmd_args_dict["readTemporaryEphemerisDatabase"] = args.dr
    cmd_args_dict["deleteTemporaryEphemerisDatabase"] = bool(args.dl)
    cmd_args_dict["surveyname"] = args.s
    cmd_args_dict["outfilestem"] = args.t
    cmd_args_dict["verbose"] = args.v

    file_exists = glob.glob(os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*"))

    if file_exists and args.f:
        pplogger.info(
            "Existing file found at {}. -f flag set: deleting existing file.".format(
                os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*")
            )
        )
        os.remove(file_exists[0])
    elif file_exists and not args.f:
        pplogger.error(
            "ERROR: existing file found at output location {}. Set -f flag to overwrite this file.".format(
                os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*")
            )
        )
        sys.exit(
            "ERROR: existing file found at output location {}. Set -f flag to overwrite this file.".format(
                os.path.join(cmd_args_dict["outpath"], cmd_args_dict["outfilestem"] + ".*")
            )
        )

    if args.dr and args.dw:
        pplogger.error("ERROR: both -dr and -dw flags set at command line. Please use only one.")
        sys.exit("ERROR: both -dr and -dw flags set at command line. Please use only one.")

    if args.dl and not args.dr and not args.dw:
        pplogger.error("ERROR: -dl flag set without either -dr or -dw.")
        sys.exit("ERROR: -dl flag set without either -dr or -dw.")

    if args.dr and not os.path.exists(args.dr):
        pplogger.error(
            "ERROR: temporary ephemeris database not found at "
            + args.dr
            + ". Rerun with command line flag -dw to create one."
        )
        sys.exit(
            "ERROR: temporary ephemeris database not found at "
            + args.dr
            + ". Rerun with command line flag -dw to create one."
        )

    if args.dw and os.path.exists(cmd_args_dict["makeTemporaryEphemerisDatabase"]) and args.f:
        pplogger.info(
            "Existing file found at {}. -f flag set: deleting existing file.".format(
                cmd_args_dict["makeTemporaryEphemerisDatabase"]
            )
        )
        os.remove(file_exists[0])
    elif args.dw and os.path.exists(cmd_args_dict["makeTemporaryEphemerisDatabase"]) and not args.f:
        pplogger.error(
            "ERROR: existing file found at output location {}. Set -f flag to overwrite this file.".format(
                cmd_args_dict["makeTemporaryEphemerisDatabase"]
            )
        )
        sys.exit(
            "ERROR: existing file found at output location {}. Set -f flag to overwrite this file.".format(
                cmd_args_dict["makeTemporaryEphemerisDatabase"]
            )
        )

    # Log all the command line settings to INFO.
    for flag, value in cmd_args_dict.items():
        pplogger.info(f"Using commandline setting {flag} = {value}")

    return cmd_args_dict
