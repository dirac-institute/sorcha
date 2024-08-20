#!/usr/bin/python

import sys
import time
import numpy as np
import argparse
import os
import logging

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
from sorcha.modules.PPOutput import PPWriteOutput, PPIndexSQLDatabase
from sorcha.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets
from sorcha.modules.PPFootprintFilter import Footprint
from sorcha.modules.PPStats import stats

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.DatabaseReader import DatabaseReader
from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.OIFReader import OIFDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader

from sorcha.activity.activity_registration import update_activity_subclasses
from sorcha.lightcurves.lightcurve_registration import update_lc_subclasses

from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.citation_text import cite_sorcha


def cite():  # pragma: no cover
    """Providing the bibtex, AAS Journals software latex command, and acknowledgement
    statements for Sorcha and the associated packages that power it.

    Parameters
    ----------
    None

    Returns
    --------
    None
    """
    cite_sorcha()


def mem(df):
    """
    Memory utility function that returns back how much memory the inputted pandas dataframe is using
    Parameters
    ------------
    df : pandas dataframe

    Returns
    -----------
    usage : int

    """

    usage = df.memory_usage(deep=True).sum()
    for k, v in df.attrs.items():
        usage += v.nbytes
    return usage


def runLSSTSimulation(args, configs):
    """
    Runs the post processing survey simulator functions that apply a series of
    filters to bias a model Solar System small body population to what the
    Vera C. Rubin Observatory Legacy Survey of Space and Time would observe.

    Parameters
    -----------
    args : dictionary or `sorchaArguments` object
        dictionary of command-line arguments.

    pplogger : logging.Logger, optional
        The logger to use in this function. If None creates a new one.
        Default = None

    Returns
    -----------
    None.

    """
    pplogger = logging.getLogger(__name__)
    pplogger.info("Post-processing begun.")

    update_lc_subclasses()
    update_activity_subclasses()

    try:
        args.validate_arguments()
    except Exception as err:
        pplogger.error(err)
        sys.exit(err)

    # if verbosity flagged, the verboselog function will log the message specified
    # if not, verboselog does absolutely nothing
    verboselog = pplogger.info if args.verbose else lambda *a, **k: None

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
    # "sizeSerialChunk" parameter in the config file assigns the chunk.
    startChunk = 0
    endChunk = 0
    loopCounter = 0

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
        verboselog("Starting main Sorcha processing loop round {}".format(loopCounter))
        endChunk = startChunk + configs["size_serial_chunk"]
        verboselog("Working on objects {}-{}".format(startChunk, endChunk))

        # Processing begins, all processing is done for chunks
        if configs["ephemerides_type"].casefold() == "external":
            verboselog("Reading in chunk of orbits and associated ephemeris from an external file")
            observations = reader.read_block(block_size=configs["size_serial_chunk"])
            observations.to_csv("post_readin_ephem_nonprimary.csv")
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
        if len(observations.index) == 0:
            pplogger.info(
                "WARNING: no ephemeris observations found for these objects. Skipping to next chunk..."
            )
            startChunk = startChunk + configs["size_serial_chunk"]
            loopCounter = loopCounter + 1
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
            observations["PSFMagTrue"] = dmagDetect + observations["trailedSourceMagTrue"]
        else:
            observations["PSFMagTrue"] = observations["trailedSourceMagTrue"]

        if configs["vignetting_on"]:
            verboselog("Calculating effects of vignetting on limiting magnitude...")
            observations["fiveSigmaDepth_mag"] = PPVignetting.vignettingEffects(observations)
        else:
            verboselog(
                "Vignetting turned OFF in config file. 5-sigma depth of field will be used for subsequent calculations."
            )
            observations["fiveSigmaDepth_mag"] = observations["fieldFiveSigmaDepth_mag"]

        # Note that the below code creates trailedSourceMag and PSFMag
        # as columns in the observations dataframe.
        # These are the columns that should be used moving forward for filters etc.
        # Do NOT use trailedSourceMagTrue or PSFMagTrue, these are the unrandomised magnitudes.
        verboselog("Calculating astrometric and photometric uncertainties...")
        observations = PPAddUncertainties.addUncertainties(
            observations, configs, args._rngs, verbose=args.verbose
        )

        if configs["randomization_on"]:
            verboselog(
                "Number of rows BEFORE randomizing astrometry and photometry: " + str(len(observations.index))
            )
            observations = PPRandomizeMeasurements.randomizeAstrometryAndPhotometry(
                observations, configs, args._rngs, verbose=args.verbose
            )
            verboselog(
                "Number of rows AFTER randomizing astrometry and photometry: " + str(len(observations.index))
            )
        else:
            verboselog(
                "Randomization turned off in config file. No astrometric or photometric randomization performed."
            )
            verboselog(
                "NOTE: new columns RATrue_deg and DecTrue_deg are EQUAL to columns RA_deg and Dec_deg."
            )
            verboselog(
                "NOTE: columns trailedSourceMagTrue and PSFMagTrue are EQUAL to columns trailedSourceMag and PSFMag."
            )
            observations["RATrue_deg"] = observations["RA_deg"].copy()
            observations["DecTrue_deg"] = observations["Dec_deg"].copy()
            observations["trailedSourceMag"] = observations["trailedSourceMagTrue"].copy()
            observations["PSFMag"] = observations["PSFMagTrue"].copy()

        if configs["camera_model"] != "none" and len(observations.index) > 0:
            verboselog("Applying field-of-view filters...")
            verboselog("Number of rows BEFORE applying FOV filters: " + str(len(observations.index)))
            observations = PPApplyFOVFilter(
                observations, configs, args._rngs, footprint=footprint, verbose=args.verbose
            )
            verboselog("Number of rows AFTER applying FOV filters: " + str(len(observations.index)))

        if configs["SNR_limit_on"] and len(observations.index) > 0:
            verboselog(
                "Dropping observations with signal to noise ratio less than {}...".format(
                    configs["SNR_limit"]
                )
            )
            verboselog("Number of rows BEFORE applying SNR limit filter: " + str(len(observations.index)))
            observations = PPSNRLimit(observations, configs["SNR_limit"])
            verboselog("Number of rows AFTER applying SNR limit filter: " + str(len(observations.index)))

        if configs["mag_limit_on"] and len(observations.index) > 0:
            verboselog("Dropping detections fainter than user-defined magnitude limit... ")
            verboselog("Number of rows BEFORE applying mag limit filter: " + str(len(observations.index)))
            observations = PPMagnitudeLimit(observations, configs["mag_limit"])
            verboselog("Number of rows AFTER applying mag limit filter: " + str(len(observations.index)))

        if configs["fading_function_on"] and len(observations.index) > 0:
            verboselog("Applying detection efficiency fading function...")
            verboselog("Number of rows BEFORE applying fading function: " + str(len(observations.index)))
            observations = PPFadingFunctionFilter(
                observations,
                configs["fading_function_peak_efficiency"],
                configs["fading_function_width"],
                args._rngs,
                verbose=args.verbose,
            )
            verboselog("Number of rows AFTER applying fading function: " + str(len(observations.index)))

        if configs["bright_limit_on"] and len(observations.index) > 0:
            verboselog("Dropping observations that are too bright...")
            verboselog("Number of rows BEFORE applying bright limit filter " + str(len(observations.index)))
            observations = PPBrightLimit(observations, configs["observing_filters"], configs["bright_limit"])
            verboselog("Number of rows AFTER applying bright limit filter " + str(len(observations.index)))

        if configs["SSP_linking_on"] and len(observations.index) > 0:
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
                configs["SSP_night_start_utc"],
                drop_unlinked=configs["drop_unlinked"],
            )
            observations.reset_index(drop=True, inplace=True)
            verboselog("Number of rows AFTER applying SSP linking filter: " + str(len(observations.index)))

        # write output if chunk not empty
        if len(observations.index) > 0:
            pplogger.info("Post processing completed for this chunk")
            pplogger.info("Outputting results for this chunk")
            PPWriteOutput(args, configs, observations, verbose=args.verbose)
            if args.stats is not None:
                stats(observations, args.stats, args.outpath, configs)
        else:
            verboselog("No observations left in chunk. No output will be written for this chunk.")

        startChunk = startChunk + configs["size_serial_chunk"]
        loopCounter = loopCounter + 1
        # end for

    if configs["output_format"] == "sqlite3" and os.path.isfile(
        os.path.join(args.outpath, args.outfilestem + ".db")
    ):
        pplogger.info("Indexing output SQLite database...")
        PPIndexSQLDatabase(os.path.join(args.outpath, args.outfilestem + ".db"))

    pplogger.info("Sorcha process is completed.")
