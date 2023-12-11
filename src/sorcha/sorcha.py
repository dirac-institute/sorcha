#!/usr/bin/python

import sys
import time
import numpy as np
import argparse
import os

from sorcha.ephemeris.simulation_driver import create_ephemeris
from sorcha.ephemeris.simulation_setup import precompute_pointing_information

from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.modules.PPLinkingFilter import PPLinkingFilter
from sorcha.modules.PPTrailingLoss import PPTrailingLoss
from sorcha.modules.PPBrightLimit import PPBrightLimit
from sorcha.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude
from sorcha.modules.PPApplyFOVFilter import PPApplyFOVFilter
from sorcha.modules.PPSNRLimit import PPSNRLimit
from sorcha.modules import PPAddUncertainties, PPRandomizeMeasurements
from sorcha.modules import PPVignetting
from sorcha.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from sorcha.modules.PPConfigParser import PPConfigFileParser, PPPrintConfigsToLog, PPFindFileOrExit

from sorcha.modules.PPGetLogger import PPGetLogger
from sorcha.modules.PPCommandLineParser import PPCommandLineParser
from sorcha.modules.PPMatchPointingToObservations import PPMatchPointingToObservations
from sorcha.modules.PPMagnitudeLimit import PPMagnitudeLimit
from sorcha.modules.PPOutput import PPWriteOutput
from sorcha.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets
from sorcha.modules.PPFootprintFilter import Footprint

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.DatabaseReader import DatabaseReader
from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.OIFReader import OIFDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader

from sorcha.activity.activity_registration import update_activity_subclasses
from sorcha.lightcurves.lightcurve_registration import update_lc_subclasses

from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.citation_text import cite_sorcha


def cite():
    """Providing the bibtex, AAS Journals software latex command, and acknowledgement
    statements for Sorcha and the associated packages that power it.
    """
    cite_sorcha()


def runLSSTSimulation(args, configs, pplogger=None):
    """
    Runs the post processing survey simulator functions that apply a series of
    filters to bias a model Solar System small body population to what the
    Vera C. Rubin Observatory Legacy Survey of Space and Time would observe.

    Parameters:
    -----------
    args (dictionary or `sorchaArguments` object):
        dictionary of command-line arguments.

    pplogger : logging.Logger, optional
        The logger to use in this function. If None creates a new one.

    Returns:
    -----------
    None.

    """
    # Set up logging if it hasn't happened already.
    if pplogger is None:
        if type(args) is dict:
            pplogger = PPGetLogger(args["outpath"])
        else:
            pplogger = PPGetLogger(args.outpath)
    pplogger.info("Post-processing begun.")

    update_lc_subclasses()
    update_activity_subclasses()

    # Initialise argument parser, assign command line arguments, and validate.
    if type(args) is dict:
        try:
            args = sorchaArguments(args, pplogger)
        except Exception as err:
            pplogger.error(err)
            sys.exit(err)

    try:
        args.validate_arguments()
    except Exception as err:
        pplogger.error(err)
        sys.exit(err)

    # if verbosity flagged, the verboselog function will log the message specified
    # if not, verboselog does absolutely nothing
    verboselog = pplogger.info if args.verbose else lambda *a, **k: None

    verboselog("Reading configuration file...")
    configs = PPConfigFileParser(args.configfile, args.surveyname)

    verboselog("Configuration file successfully read.")

    configs["mainfilter"], configs["othercolours"] = PPGetMainFilterAndColourOffsets(
        args.paramsinput, configs["observing_filters"], configs["aux_format"]
    )

    PPPrintConfigsToLog(configs, args)

    # End of config parsing

    verboselog("Reading pointing database...")

    filterpointing = PPReadPointingDatabase(
        args.pointing_database, configs["observing_filters"], configs["pointing_sql_query"], args.surveyname
    )

    # if we are going to compute the ephemerides, then we should pre-compute all
    # of the needed values derived from the pointing information.
    if configs["ephemerides_type"].casefold() != "external":
        verboselog("Pre-computing pointing information for ephemeris generation")
        filterpointing = precompute_pointing_information(filterpointing, args, configs)

    # Set up the data readers.
    ephem_type = configs["ephemerides_type"]
    ephem_primary = False
    if ephem_type.casefold() == "external":
        ephem_primary = True
    reader = CombinedDataReader(ephem_primary=ephem_primary, verbose=True)

    # TODO: Once more ephemerides_types are added this should be wrapped in a EphemerisDataReader
    # That does the selection and checks. We are holding off adding this level of indirection until there
    # is a second ephemerides_type.
    if ephem_type.casefold() not in ["ar", "external"]:  # pragma: no cover
        pplogger.error(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
        sys.exit(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
    if ephem_type.casefold() == "external":
        reader.add_ephem_reader(OIFDataReader(args.oifoutput, configs["eph_format"]))

    reader.add_aux_data_reader(OrbitAuxReader(args.orbinfile, configs["aux_format"]))
    reader.add_aux_data_reader(CSVDataReader(args.paramsinput, configs["aux_format"]))
    if configs["comet_activity"] is not None or configs["lc_model"] is not None:
        reader.add_aux_data_reader(CSVDataReader(args.complex_parameters, configs["aux_format"]))

    # In case of a large input file, the data is read in chunks. The
    # "sizeSerialChunk" parameter in PPConfig.ini assigns the chunk.
    startChunk = 0
    endChunk = 0

    ii = -1
    with open(args.orbinfile) as f:
        for ii, l in enumerate(f):
            pass
    lenf = ii

    footprint = None
    if configs["camera_model"] == "footprint":
        verboselog("Creating sensor footprint object for filtering")
        footprint = Footprint(configs["footprint_path"])

    while endChunk < lenf:
        endChunk = startChunk + configs["size_serial_chunk"]
        verboselog("Working on objects {}-{}.".format(startChunk, endChunk))

        # Processing begins, all processing is done for chunks
        if configs["ephemerides_type"].casefold() == "external":
            verboselog("Reading in chunk of orbits and associated ephemeris from an external file")
            observations = reader.read_block(block_size=configs["size_serial_chunk"])
        else:
            verboselog("Ingest chunk of orbits")
            orbits_df = reader.read_aux_block(block_size=configs["size_serial_chunk"])
            verboselog("Starting ephemeris generation")
            observations = create_ephemeris(orbits_df, filterpointing, args, configs)
            verboselog("Ephemeris generation completed")

        verboselog("Start post processing for this chunk")
        verboselog("Matching pointing database information to observations on rough camera footprint")

        # If the ephemeris file doesn't have any observations for the objects in the chunk
        # PPReadAllInput will return an empty dataframe. We thus log a warning.
        if len(observations) == 0:
            pplogger.info(
                "WARNING: no ephemeris observations found for these objects. Skipping to next chunk..."
            )
            startChunk = startChunk + configs["size_serial_chunk"]
            continue

        observations = PPMatchPointingToObservations(observations, filterpointing)

        verboselog("Calculating apparent magnitudes...")
        observations = PPCalculateApparentMagnitude(
            observations,
            configs["phase_function"],
            configs["mainfilter"],
            configs["othercolours"],
            configs["observing_filters"],
            configs["comet_activity"],
            lightcurve_choice=configs["lc_model"],
            verbose=args.verbose,
        )

        if configs["trailing_losses_on"]:
            verboselog("Calculating trailing losses...")
            dmagDetect = PPTrailingLoss(observations, "circularPSF")
            observations["PSFMag"] = dmagDetect + observations["TrailedSourceMag"]
        else:
            observations["PSFMag"] = observations["TrailedSourceMag"]

        verboselog("Calculating effects of vignetting on limiting magnitude...")
        observations["fiveSigmaDepthAtSource"] = PPVignetting.vignettingEffects(observations)

        # Note that the below code creates observedTrailedSourceMag and observedPSFMag
        # as columns in the observations dataframe.
        # These are the columns that should be used moving forward for filters etc.
        # Do NOT use TrailedSourceMag or PSFMag, these are cut later.
        verboselog("Calculating astrometric and photometric uncertainties...")
        observations = PPAddUncertainties.addUncertainties(
            observations, configs, args._rngs, verbose=args.verbose
        )

        verboselog("Randomising astrometry...")
        observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
        observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
        observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(
            observations, args._rngs, sigName="AstrometricSigma(deg)", sigUnits="deg"
        )

        verboselog("Applying field-of-view filters...")
        observations = PPApplyFOVFilter(
            observations, configs, args._rngs, footprint=footprint, verbose=args.verbose
        )

        if configs["SNR_limit_on"]:
            verboselog(
                "Dropping observations with signal to noise ratio less than {}...".format(
                    configs["SNR_limit"]
                )
            )
            observations = PPSNRLimit(observations, configs["SNR_limit"])

        if configs["mag_limit_on"]:
            verboselog("Dropping detections fainter than user-defined magnitude limit... ")
            observations = PPMagnitudeLimit(observations, configs["mag_limit"])

        if configs["fading_function_on"]:
            verboselog("Applying detection efficiency fading function...")
            observations = PPFadingFunctionFilter(
                observations,
                configs["fading_function_peak_efficiency"],
                configs["fading_function_width"],
                args._rngs,
                verbose=args.verbose,
            )

        if configs["bright_limit_on"]:
            verboselog("Dropping observations that are too bright...")
            observations = PPBrightLimit(observations, configs["observing_filters"], configs["bright_limit"])

        if len(observations) == 0:
            verboselog("No observations left in chunk. Skipping to next chunk...")
            startChunk = startChunk + configs["size_serial_chunk"]
            continue

        if configs["SSP_linking_on"]:
            verboselog("Applying SSP linking filter...")
            verboselog("Number of rows BEFORE applying SSP linking filter: " + str(len(observations.index)))

            observations = PPLinkingFilter(
                observations,
                configs["SSP_detection_efficiency"],
                configs["SSP_number_observations"],
                configs["SSP_number_tracklets"],
                configs["SSP_track_window"],
                configs["SSP_separation_threshold"],
                configs["SSP_maximum_time"],
            )

            observations.reset_index(drop=True, inplace=True)
            verboselog("Number of rows AFTER applying SSP linking filter: " + str(len(observations.index)))

        pplogger.info("Post processing completed for this chunk")

        pplogger.info("Output results for this chunk")

        # write output
        PPWriteOutput(args, configs, observations, endChunk, verbose=args.verbose)

        startChunk = startChunk + configs["size_serial_chunk"]
        # end for

    pplogger.info("Sorcha process is completed.")


def main():
    """
    A post processing survey simulator that applies a series of filters to bias a
    model Solar System small body population to what the specified wide-field
    survey would observe.

    usage: sorcha [-h] -c C -o O -ob OB -p P -pd PD [-er E] [-ew E] [-cp CP] [-dw [DW]] [-dr DR] [-dl] [-f] [-s S] [-t T] [-v]

    options:
      -h, --help            show this help message and exit

    Required arguments:
      -c C, --config C      Input configuration file name (default: None)
      -o O, --outfile O     Path to store output and logs. (default: None)
      -ob OB, --orbit OB    Orbit file name (default: None)
      -p P, --params P      Physical parameters file name (default: None)
      -pd PD, --pointing_database PD
                            Survey pointing information (default: None)

    Optional arguments:
      -er E, --ephem_read E Existing ephemeris simulation output file name (default: None)
      -ew E, --ephem_write E
                            Output file name for newly generated ephemeris simulation (default: None)
      -cp CP, --complex_physical_parameters CP
                            Complex physical parameters file name (default: None)
      -dw [DW]              Make temporary ephemeris database. If no filepath/name supplied, default name and ephemeris input location used. (default: None)
      -dr DR                Location of existing/previous temporary ephemeris database to read from if wanted. (default: None)
      -dl                   Delete the temporary ephemeris database after code has completed. (default: False)
      -f, --force           Force deletion/overwrite of existing output file(s). (default: False)
      -s S, --survey S      Survey to simulate (default: LSST)
      -t T, --stem T        Output file name stem. (default: SSPPOutput)
      -v, --verbose         Verbosity. Default currently true; include to turn off verbosity. (default: True)
    """

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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
        "-ob",
        "--orbit",
        help="Orbit file name",
        type=str,
        dest="ob",
        required=True,
    )
    required.add_argument(
        "-p",
        "--params",
        help="Physical parameters file name",
        type=str,
        dest="p",
        required=True,
    )
    required.add_argument(
        "-pd",
        "--pointing_database",
        help="Survey pointing information",
        type=str,
        dest="pd",
        required=True,
    )

    optional = parser.add_argument_group("Optional arguments")
    optional.add_argument(
        "-er",
        "--ephem_read",
        help="Previously generated ephemeris simulation file name, required if ephemerides_type in config file is 'external'.",
        type=str,
        dest="er",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-ew",
        "--ephem_write",
        help="Output file name for newly generated ephemeris simulation, required if ephemerides_type in config file is not 'external'.",
        type=str,
        dest="ew",
        required=False,
        default=None,
    )
    optional.add_argument(
        "-ar",
        "--ar_data_path",
        help="Directory path where Assist+Rebound data files where stored when running bootstrap_sorcha_data_files from the command line.",
        type=str,
        dest="ar",
        required=False,
    )
    optional.add_argument(
        "-cp",
        "--complex_physical_parameters",
        help="Complex physical parameters file name",
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
    optional.add_argument("-s", "--survey", help="Survey to simulate", type=str, dest="s", default="LSST")
    optional.add_argument(
        "-t", "--stem", help="Output file name stem.", type=str, dest="t", default="SSPPOutput"
    )
    optional.add_argument(
        "-v",
        "--verbose",
        help="Verbosity. Default currently true; include to turn off verbosity.",
        dest="v",
        default=True,
        action="store_false",
    )

    args = parser.parse_args()

    # Extract the output file path now in order to set up logging.
    outpath = PPFindFileOrExit(args.o, "-o, --outfile")
    pplogger = PPGetLogger(outpath)
    pplogger.info("Sorcha Start (Main)")
    pplogger.info(f"Command line: {' '.join(sys.argv)}")

    # Extract and validate the remaining arguments.
    cmd_args = PPCommandLineParser(args)
    configs = PPConfigFileParser(cmd_args["configfile"], cmd_args["surveyname"])

    if configs["ephemerides_type"] == "external" and cmd_args["oifoutput"] is None:
        pplogger.error("ERROR: A+R simulation not enabled and no ephemerides file provided")
        sys.exit("ERROR: A+R simulation not enabled and no ephemerides file provided")

    if configs["lc_model"] and cmd_args["complex_physical_parameters"] is None:
        pplogger.error("ERROR: No complex physical parameter file provided for light curve model")
        sys.exit("ERROR: No complex physical parameter file provided for light curve model")

    if configs["comet_activity"] and cmd_args["complex_physical_parameters"] is None:
        pplogger.error("ERROR: No complex physical parameter file provided for comet activity model")
        sys.exit("ERROR: No complex physical parameter file provided for comet activity model")

    if "SORCHA_SEED" in os.environ:
        cmd_args["seed"] = int(os.environ["SORCHA_SEED"])
        pplogger.info(f"Random seed overridden via environmental variable, SORCHA_SEED={cmd_args['seed']}")

    if cmd_args["surveyname"] in ["LSST", "lsst"]:
        try:
            args = sorchaArguments(cmd_args, pplogger)
        except Exception as err:
            pplogger.error(err)
            sys.exit(err)
        try:
            args.validate_arguments()
        except Exception as err:
            pplogger.error(err)
            sys.exit(err)
        runLSSTSimulation(args, configs, pplogger)
    else:
        pplogger.error(
            "ERROR: Survey name not recognised. Current allowed surveys are: {}".format(["LSST", "lsst"])
        )
        sys.exit(
            "ERROR: Survey name not recognised. Current allowed surveys are: {}".format(["LSST", "lsst"])
        )


if __name__ == "__main__":
    main()
