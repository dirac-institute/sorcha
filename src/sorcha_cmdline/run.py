#
# The `sorcha run` subcommand implementation
#
import argparse
from sorcha_cmdline.sorchaargumentparser import SorchaArgumentParser


def main():
    parser = SorchaArgumentParser(
        prog="sorcha run",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Run a simulation.",
    )

    # parser = SorchaArgparse(parser)

    required = parser.add_argument_group("Required arguments")
    required.add_argument(
        "-c",
        "--config",
        help="Input configuration file name",
        type=str,
        dest="c",
        required=True,
    )
    required.add_argument(
        "-o",
        "--outfile",
        help="Path to store output and logs.",
        type=str,
        dest="o",
        required=True,
    )
    required.add_argument(
        "--ob",
        "--orbits",
        help="Orbit catalog file name",
        type=str,
        dest="ob",
        required=True,
    )
    required.add_argument(
        "-p",
        "--physical-parameters",
        help="Catalog of object physical parameters",
        type=str,
        dest="p",
        required=True,
    )
    required.add_argument(
        "--pd",
        "--pointing-db",
        help="Survey pointing information",
        type=str,
        dest="pd",
        required=True,
    )

    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "--er",
        "--ephem-read",
        help="Previously generated ephemeris simulation file name, required if ephemerides_type in config file is 'external'.",
        type=str,
        dest="er",
        required=False,
        default=None,
    )
    optional.add_argument(
        "--ew",
        "--ephem-write",
        help="Output file name for newly generated ephemeris simulation, required if ephemerides_type in config file is not 'external'.",
        type=str,
        dest="ew",
        required=False,
        default=None,
    )
    optional.add_argument(
        "--ar",
        "--ar-data-path",
        help="Directory path where Assist+Rebound data files where stored when running bootstrap_sorcha_data_files from the command line.",
        type=str,
        dest="ar",
        required=False,
    )
    optional.add_argument(
        "--cp",
        "--complex-physical-parameters",
        help="Catalog of object complex physical parameters",
        type=str,
        dest="cp",
    )
    optional.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing output file(s). Default False.",
        dest="f",
        action="store_true",
        default=False,
    )
    optional.add_argument(
        "-s", "--survey", help="Survey to simulate", type=str, dest="s", default="rubin_sim"
    )
    optional.add_argument(
        "-t", "--stem", help="Output file name stem.", type=str, dest="t", default="SSPPOutput"
    )
    optional.add_argument(
        "-v",
        "--verbose",
        help="Print additional information to log while running",
        dest="v",
        default=True,
        action="store_false",
    )

    optional.add_argument(
        "--st",
        "--stats",
        help="Output summary statistics table to this stem filename.",
        type=str,
        dest="st",
        default=None,
    )

    args = parser.parse_args()

    return execute(args)


def execute(args):
    #
    # NOTE: DO NOT MOVE THESE IMPORTS TO THE TOP LEVEL OF THE MODULE !!!
    #
    #       Importing sorcha from the function and not at the top-level of the module
    #       allows us to exit quickly and print the help/error message (in case there
    #       was a mistake on the command line). Importing sorcha can take 5 seconds or
    #       more, and making the user wait that long just to print out an erro message
    #       is poor user experience.
    #
    from sorcha.sorcha import (
        PPFindFileOrExit,
        PPGetLogger,
        PPCommandLineParser,
        PPConfigFileParser,
        runLSSTSimulation,
        sorchaArguments,
        sorchaConfigs,
        update_activity_subclasses,
        update_lc_subclasses,
    )
    import sys, os

    # Extract the output file path now in order to set up logging.
    outpath = PPFindFileOrExit(args.o, "-o, --outfile")
    pplogger = PPGetLogger(outpath, args.t)
    pplogger.info("Sorcha Start (Main)")
    pplogger.info(f"Command line: {' '.join(sys.argv)}")

    # update add-on subclasses before we parse the config file!
    update_lc_subclasses()
    update_activity_subclasses()

    # Extract and validate the remaining arguments.
    cmd_args = PPCommandLineParser(args)
    pplogger.info("Reading configuration file...")
    # configs = PPConfigFileParser(cmd_args["configfile"], cmd_args["surveyname"])
    sconfigs = sorchaConfigs(cmd_args["configfile"], cmd_args["surveyname"])
    pplogger.info("Configuration file read.")

    if sconfigs.input.ephemerides_type == "external" and cmd_args["input_ephemeris_file"] is None:
        pplogger.error("ERROR: A+R simulation not enabled and no ephemerides file provided")
        sys.exit("ERROR: A+R simulation not enabled and no ephemerides file provided")

    if sconfigs.lightcurve.lc_model and cmd_args["complex_physical_parameters"] is None:
        pplogger.error("ERROR: No complex physical parameter file provided for light curve model")
        sys.exit("ERROR: No complex physical parameter file provided for light curve model")

    if sconfigs.activity.comet_activity and cmd_args["complex_physical_parameters"] is None:
        pplogger.error("ERROR: No complex physical parameter file provided for comet activity model")
        sys.exit("ERROR: No complex physical parameter file provided for comet activity model")
    if "SORCHA_SEED" in os.environ:
        cmd_args["seed"] = int(os.environ["SORCHA_SEED"])
        pplogger.info(f"Random seed overridden via environmental variable, SORCHA_SEED={cmd_args['seed']}")

    if cmd_args["surveyname"] in ["rubin_sim", "RUBIN_SIM"]:
        try:
            args = sorchaArguments(cmd_args)
        except Exception as err:
            pplogger.error(err)
            sys.exit(err)
        try:
            args.validate_arguments()
        except Exception as err:
            pplogger.error(err)
            sys.exit(err)
        runLSSTSimulation(args, sconfigs)
    elif cmd_args["surveyname"] in ["LSST", "lsst"]:
        pplogger.error(
            "ERROR: The LSST has not started yet Current allowed surveys are: {}".format(
                ["rubin_sim", "RUBIN_SIM"]
            )
        )
        sys.exit(
            "ERROR: The LSST has not started. Current allowed surveys are: {}".format(
                ["rubin_sim", "RUBIN_SIM"]
            )
        )
    else:
        pplogger.error(
            "ERROR: Survey name not recognised. Current allowed surveys are: {}".format(
                ["rubin_sim", "RUBIN_SIM"]
            )
        )
        sys.exit(
            "ERROR: Survey name not recognised. Current allowed surveys are: {}".format(
                ["rubin_sim", "RUBIN_SIM"]
            )
        )


if __name__ == "__main__":
    main()
