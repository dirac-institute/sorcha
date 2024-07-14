#
# The `sorcha run` subcommand implementation
#
import argparse


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="Run a simulation."
    )
    inputs = parser.add_argument_group("inputs")
    inputs.add_argument(
        "-c",
        "--config",
        help="Input configuration file name",
        type=str,
        required=True,
        # default="sorcha.ini"
    )
    inputs.add_argument(
        "--pointings",
        help="Survey pointing database.",
        type=str,
        required=True,
        # default="pointings.db"
    )
    inputs.add_argument(
        "--orbits",
        help="Orbit catalog.",
        type=str,
        required=True,
        # default="orbits.des"
    )
    inputs.add_argument(
        "--colors",
        help="Catalog of object colors.",
        type=str,
        required=True,
        # default="colors.txt"
    )

    outputs = parser.add_argument_group("outputs")
    outputs.add_argument("-o", "--output-dir", help="Path to store output and logs.", type=str, default=".")
    outputs.add_argument(
        "--prefix",
        help="Prefix of output files. Outputs will be written to <output-dir>/<prefix>-...",
        type=str,
        default="sorcha-results",
    )
    outputs.add_argument(
        "--stats",
        help="Output the summary statistics table into <output-dir>/<prefix>-stats.csv",
        action="store_true",
        default=False,
    )

    advanced = parser.add_argument_group("advanced")
    advanced.add_argument(
        "--process-subset",
        help="Process a subset of the input objects. Specify in form of <split>/<nsplits>, where <nsplits> is the number of chunks into which"
             " the input will be divided, and <split> is the (1-based) chunk for to be processed here. For example, writing 3/5 with a catalog"
             " of 100 objects will process objects with (0-based) indices [40, 60).",
        type=str,
        default="1/1"
    )
    advanced.add_argument(
        "--ephem-input",
        help="Previously generated ephemeris simulation file name, required if ephemerides_type in config file is 'external'.",
        type=str,
        required=False,
        default=None,
    )
    advanced.add_argument(
        "--ephem-output",
        help="Output file name for newly generated ephemeris simulation, required if ephemerides_type in config file is not 'external'.",
        type=str,
        required=False,
        default=None,
    )
    advanced.add_argument(
        "--integrator-data",
        help="Directory path where Assist+Rebound data files where stored when running bootstrap_sorcha_data_files from the command line.",
        type=str,
        required=False,
    )
    advanced.add_argument(
        "--extra-object-data",
        help="Catalog of additional object parameters used by sorcha and sorcha add-ons (e.g., data needed to simulate light-curves, activity, etc)",
        type=str,
    )
    advanced.add_argument(
        "--force",
        help="Force deletion/overwrite of existing output file(s).",
        action="store_true",
        default=False,
    )
    advanced.add_argument("-s", "--survey", help="Survey to simulate", type=str, default="rubin_sim")
    advanced.add_argument(
        "-v",
        "--verbose",
        help="Print additional information while running.",
        default=False,
        action="store_true",
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
    )
    import sys, os

    # Extract the output file path now in order to set up logging.
    outpath = PPFindFileOrExit(args.output_dir, "-o, --output-dir")
    args.log_file = f"{outpath}/{args.prefix}.log"
    pplogger = PPGetLogger(args.log_file)

    pplogger.info(f"Starting sorcha run, pid={os.getpid()}")
    pplogger.info(f"Command line: {' '.join(sys.argv)}")

    # Extract and validate the remaining arguments.
    cmd_args = PPCommandLineParser(args)
    pplogger.info("Reading configuration file...")
    configs = PPConfigFileParser(cmd_args["configfile"], cmd_args["surveyname"])
    pplogger.info("Configuration file read.")

    if configs["ephemerides_type"] == "external" and cmd_args["oifoutput"] is None:
        pplogger.error("ERROR: A+R simulation not enabled and no ephemerides file provided")
        sys.exit("ERROR: A+R simulation not enabled and no ephemerides file provided")

    if configs["lc_model"] and cmd_args["extra_objects_data"] is None:
        pplogger.error("ERROR: No extra object data catalog provided for light curve model")
        sys.exit("ERROR: No extra object data catalog provided for light curve model")

    if configs["comet_activity"] and cmd_args["extra_objects_data"] is None:
        pplogger.error("ERROR: No extra object data catalog provided for comet activity model")
        sys.exit("ERROR: No extra object data catalog provided for comet activity model")

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
        runLSSTSimulation(args, configs)
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
