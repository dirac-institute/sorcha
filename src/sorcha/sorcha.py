#!/usr/bin/python

import sys
import time
import numpy as np
import argparse
import os

from sorcha.modules.PPReadPointingDatabase import PPReadPointingDatabase
from sorcha.modules.PPLinkingFilter import PPLinkingFilter
from sorcha.modules.PPTrailingLoss import PPTrailingLoss
from sorcha.modules.PPBrightLimit import PPBrightLimit
from sorcha.modules.PPMakeTemporaryEphemerisDatabase import PPMakeTemporaryEphemerisDatabase
from sorcha.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude
from sorcha.modules.PPApplyFOVFilter import PPApplyFOVFilter
from sorcha.modules.PPSNRLimit import PPSNRLimit
from sorcha.modules import PPAddUncertainties, PPRandomizeMeasurements
from sorcha.modules import PPVignetting
from sorcha.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from sorcha.modules.PPConfigParser import PPConfigFileParser, PPPrintConfigsToLog
from sorcha.modules.PPGetLogger import PPGetLogger
from sorcha.modules.PPCommandLineParser import PPCommandLineParser
from sorcha.modules.PPMatchPointingToObservations import PPMatchPointingToObservations
from sorcha.modules.PPMagnitudeLimit import PPMagnitudeLimit
from sorcha.modules.PPOutput import PPWriteOutput
from sorcha.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.DatabaseReader import DatabaseReader
from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.OIFReader import OIFDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader

# Author: Samuel Cornwall, Siegfried Eggl, Grigori Fedorets, Steph Merritt, Meg Schwamb


def runLSSTPostProcessing(cmd_args):
    """
    Runs the post processing survey simulator functions that apply a series of
    filters to bias a model Solar System small body population to what the
    Vera C. Rubin Observatory Legacy Survey of Space and Time would observe.

    Parameters:
    -----------
    cmd_args (dictionary): dictionary of command-line arguments.

    Returns:
    -----------
    None.

    """

    # Initialise argument parser and assign command line arguments

    pplogger = PPGetLogger(cmd_args["outpath"])
    pplogger.info("Post-processing begun.")

    # if verbosity flagged, the verboselog function will log the message specified
    # if not, verboselog does absolutely nothing
    verboselog = pplogger.info if cmd_args["verbose"] else lambda *a, **k: None

    verboselog("Reading configuration file...")
    configs = PPConfigFileParser(cmd_args["configfile"], cmd_args["surveyname"])

    verboselog("Configuration file successfully read.")

    configs["mainfilter"], configs["othercolours"] = PPGetMainFilterAndColourOffsets(
        cmd_args["paramsinput"], configs["observing_filters"], configs["aux_format"]
    )

    PPPrintConfigsToLog(configs, cmd_args)

    # End of config parsing

    if cmd_args["makeTemporaryEphemerisDatabase"]:
        verboselog("Creating temporary ephemeris database...")
        cmd_args["readTemporaryEphemerisDatabase"] = PPMakeTemporaryEphemerisDatabase(
            cmd_args["oifoutput"], cmd_args["makeTemporaryEphemerisDatabase"], configs["eph_format"]
        )

    verboselog("Reading pointing database...")

    filterpointing = PPReadPointingDatabase(
        configs["pointing_database"], configs["observing_filters"], configs["pointing_sql_query"]
    )

    verboselog("Instantiating random number generator ... ")

    if configs["rng_seed"]:
        rng_seed = configs["rng_seed"]
    else:
        rng_seed = int(time.time())

    verboselog("Random number seed is {}.".format(rng_seed))
    rng = np.random.default_rng(rng_seed)

    # Set up the data readers.
    reader = CombinedDataReader(verbose=True)

    if cmd_args["makeTemporaryEphemerisDatabase"] or cmd_args["readTemporaryEphemerisDatabase"]:
        reader.add_ephem_reader(DatabaseReader(cmd_args["readTemporaryEphemerisDatabase"]))
    else:
        # TODO: Once more ephemerides_types are added this should be wrapped in a EphemerisDataReader
        # That does the selection and checks. We are holding off adding this level of indirection until there
        # is a second ephemerides_type.
        ephem_type = configs["ephemerides_type"]
        if ephem_type.casefold() != "oif":  # pragma: no cover
            pplogger.error(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
            sys.exit(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
        reader.add_ephem_reader(OIFDataReader(cmd_args["oifoutput"], configs["eph_format"]))

    reader.add_aux_data_reader(OrbitAuxReader(cmd_args["orbinfile"], configs["aux_format"]))
    reader.add_aux_data_reader(CSVDataReader(cmd_args["paramsinput"], configs["aux_format"]))
    if configs["comet_activity"] == "comet":
        reader.add_aux_data_reader(CSVDataReader(cmd_args["cometinput"], configs["aux_format"]))

    # In case of a large input file, the data is read in chunks. The
    # "sizeSerialChunk" parameter in PPConfig.ini assigns the chunk.
    startChunk = 0
    endChunk = 0

    ii = -1
    with open(cmd_args["orbinfile"]) as f:
        for ii, l in enumerate(f):
            pass
    lenf = ii

    while endChunk < lenf:
        endChunk = startChunk + configs["size_serial_chunk"]
        verboselog("Working on objects {}-{}.".format(startChunk, endChunk))

        # Processing begins, all processing is done for chunks
        observations = reader.read_block(block_size=configs["size_serial_chunk"])
        observations = PPMatchPointingToObservations(observations, filterpointing)

        # If the ephemeris file doesn't have any observations for the objects in the chunk
        # PPReadAllInput will return an empty dataframe. We thus log a warning.
        if len(observations) == 0:
            pplogger.info(
                "WARNING: no ephemeris observations found for these objects. Skipping to next chunk..."
            )
            startChunk = startChunk + configs["size_serial_chunk"]
            continue

        verboselog("Calculating apparent magnitudes...")
        observations = PPCalculateApparentMagnitude(
            observations,
            configs["phase_function"],
            configs["mainfilter"],
            configs["othercolours"],
            configs["observing_filters"],
            configs["comet_activity"],
            verbose=cmd_args["verbose"],
        )

        if configs["trailing_losses_on"]:
            verboselog("Calculating trailing losses...")
            dmagDetect = PPTrailingLoss(observations, "circularPSF")
            observations["PSFMag"] = dmagDetect + observations["TrailedSourceMag"]
        else:
            observations["PSFMag"] = observations["TrailedSourceMag"]

        verboselog("Calculating effects of vignetting on limiting magnitude...")
        observations["fiveSigmaDepthAtSource"] = PPVignetting.vignettingEffects(observations)

        verboselog("Applying field-of-view filters...")
        observations = PPApplyFOVFilter(observations, configs, rng, verbose=cmd_args["verbose"])

        # Note that the below code creates observedTrailedSourceMag and observedPSFMag
        # as columns in the observations dataframe.
        # These are the columns that should be used moving forward for filters etc.
        # Do NOT use TrailedSourceMag or PSFMag, these are cut later.
        verboselog("Calculating astrometric and photometric uncertainties...")
        observations = PPAddUncertainties.addUncertainties(
            observations, configs, rng, verbose=cmd_args["verbose"]
        )

        verboselog("Randomising astrometry...")
        observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
        observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
        observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(
            observations, rng, sigName="AstrometricSigma(deg)", sigUnits="deg"
        )

        if configs["camera_model"] == "footprint":
            verboselog("Re-applying field-of-view filter...")
            observations = PPApplyFOVFilter(observations, configs, rng, verbose=cmd_args["verbose"])

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
                rng,
                verbose=cmd_args["verbose"],
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
                rng,
            )

            observations.reset_index(drop=True, inplace=True)
            verboselog("Number of rows AFTER applying SSP linking filter: " + str(len(observations.index)))

        # write output
        PPWriteOutput(cmd_args, configs, observations, endChunk, verbose=cmd_args["verbose"])

        startChunk = startChunk + configs["size_serial_chunk"]
        # end for

    if cmd_args["deleteTemporaryEphemerisDatabase"]:
        verboselog("Deleting the temporary ephemeris database...")
        os.remove(cmd_args["readTemporaryEphemerisDatabase"])

    pplogger.info("Post processing completed.")


def main():
    """
    A post processing survey simulator that applies a series of filters to bias a
    model Solar System small body population to what the specified wide-field
    survey would observe.

    usage: sorcha [-h] -c C [-dw [DW]] [-dr DR] [-dl] [-m M] -p P -o O -e E [-s S] -u U [-t T] [-v] [-f]
        arguments:
          -h, --help         show this help message and exit
          -c C, --config C   Input configuration file name
          -dw [DW]           Make temporary ephemeris database. If no filepath/name supplied, default name and ephemeris input location used.
          -dr DR             Location of existing/previous temporary ephemeris database to read from if wanted.
          -dl                Delete the temporary ephemeris database after code has completed.
          -m M, --comet M    Comet parameter file name
          -p P, --params P   Physical parameters file name
          -o O, --orbit O    Orbit file name
          -e E, --ephem E    Ephemeris simulation output file name
          -s S, --survey S   Survey to simulate
          -u U, --outfile U  Path to store output and logs.
          -t T, --stem T     Output file name stem.
          -v, --verbose      Verbosity. Default currently true; include to turn off verbosity.
          -f, --force        Force deletion/overwrite of existing output file(s). Default False.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        help="Input configuration file name",
        type=str,
        dest="c",
        default="./PPConfig.ini",
        required=True,
    )
    parser.add_argument(
        "-dw",
        help="Make temporary ephemeris database. If no filepath/name supplied, default name and ephemeris input location used.",
        dest="dw",
        nargs="?",
        const="default",
        type=str,
    )
    parser.add_argument(
        "-dr",
        help="Location of existing/previous temporary ephemeris database to read from if wanted.",
        dest="dr",
        type=str,
    )
    parser.add_argument(
        "-dl",
        help="Delete the temporary ephemeris database after code has completed.",
        action="store_true",
        default=False,
    )
    parser.add_argument("-m", "--comet", help="Comet parameter file name", type=str, dest="m")
    parser.add_argument(
        "-p",
        "--params",
        help="Physical parameters file name",
        type=str,
        dest="p",
        default="./data/params",
        required=True,
    )
    parser.add_argument(
        "-o", "--orbit", help="Orbit file name", type=str, dest="o", default="./data/orbit.des", required=True
    )
    parser.add_argument(
        "-e",
        "--ephem",
        help="Ephemeris simulation output file name",
        type=str,
        dest="e",
        default="./data/oiftestoutput",
        required=True,
    )
    parser.add_argument("-s", "--survey", help="Survey to simulate", type=str, dest="s", default="LSST")
    parser.add_argument(
        "-u",
        "--outfile",
        help="Path to store output and logs.",
        type=str,
        dest="u",
        default="./data/out/",
        required=True,
    )
    parser.add_argument(
        "-t", "--stem", help="Output file name stem.", type=str, dest="t", default="SSPPOutput"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Verbosity. Default currently true; include to turn off verbosity.",
        dest="v",
        default=True,
        action="store_false",
    )
    parser.add_argument(
        "-f",
        "--force",
        help="Force deletion/overwrite of existing output file(s). Default False.",
        dest="f",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    cmd_args = PPCommandLineParser(args)

    if cmd_args["surveyname"] in ["LSST", "lsst"]:
        runLSSTPostProcessing(cmd_args)
    else:
        sys.exit(
            "ERROR: Survey name not recognised. Current allowed surveys are: {}".format(["LSST", "lsst"])
        )


if __name__ == "__main__":
    main()
