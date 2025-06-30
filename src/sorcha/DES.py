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
from sorcha.modules.DESCuts import des_distance_cut, des_motion_cut
from sorcha.modules.PPLinkingFilter import PPLinkingFilter
from sorcha.modules.DESDiscoveryFilter import DESDiscoveryFilter
from sorcha.modules.PPTrailingLoss import PPTrailingLoss
from sorcha.modules.PPBrightLimit import PPBrightLimit
from sorcha.modules.PPCalculateApparentMagnitude import PPCalculateApparentMagnitude
from sorcha.modules.PPApplyFOVFilter import PPApplyFOVFilter
from sorcha.modules.PPFootprintFilter import Footprint
from sorcha.modules.PPSNRLimit import PPSNRLimit
from sorcha.modules import PPAddUncertainties, PPRandomizeMeasurements
from sorcha.modules import PPVignetting
from sorcha.modules.DESFadingFunctionFilter import DESFadingFunctionFilter
from sorcha.modules.PPFaintObjectCullingFilter import PPFaintObjectCullingFilter


from sorcha.modules.PPMatchPointingToObservations import PPMatchPointingToObservations
from sorcha.modules.PPMagnitudeLimit import PPMagnitudeLimit
from sorcha.modules.PPOutput import PPWriteOutput, PPIndexSQLDatabase
from sorcha.modules.PPGetMainFilterAndColourOffsets import PPGetMainFilterAndColourOffsets
from sorcha.modules.PPStats import stats

from sorcha.readers.CombinedDataReader import CombinedDataReader
from sorcha.readers.CSVReader import CSVDataReader
from sorcha.readers.EphemerisReader import EphemerisDataReader
from sorcha.readers.OrbitAuxReader import OrbitAuxReader

from sorcha.activity.activity_registration import update_activity_subclasses
from sorcha.lightcurves.lightcurve_registration import update_lc_subclasses

from sorcha.utilities.sorchaArguments import sorchaArguments
from sorcha.utilities.sorchaConfigs import sorchaConfigs, PrintConfigsToLog
from sorcha.utilities.sorchaCommandLineParser import sorchaCommandLineParser
from sorcha.utilities.fileAccessUtils import FindFileOrExit
from sorcha.utilities.citation_text import cite_sorcha
from sorcha.utilities.sorchaGetLogger import sorchaGetLogger


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


def runDESSimulation(args, sconfigs):
    """
    Runs the post processing survey simulator functions that apply a series of
    filters to bias a model Solar System small body population to what the Cerro Tololo observatory Dark Energy Survey would observe.

    Parameters
    -----------
    args : dictionary or `sorchaArguments` object
        dictionary of command-line arguments.

    pplogger : logging.Logger, optional
        The logger to use in this function. If None creates a new one.
        Default = None
    sconfigs: dataclass
        Dataclass of configuration file arguments.

    Returns
    -----------
    None.

    """
    pplogger = logging.getLogger(__name__)
    pplogger.info("Post-processing begun.")

    try:
        args.validate_arguments()
    except Exception as err:
        pplogger.error(err)
        sys.exit(err)

    # if verbosity flagged, the verboselog function will log the message specified
    # if not, verboselog does absolutely nothing
    verboselog = pplogger.info if args.loglevel else lambda *a, **k: None

    sconfigs.filters.mainfilter, sconfigs.filters.othercolours = PPGetMainFilterAndColourOffsets(
        args.paramsinput, sconfigs.filters.observing_filters, sconfigs.input.aux_format
    )

    PrintConfigsToLog(sconfigs, args)

    # End of config parsing

    verboselog("Reading pointing database...")

    filterpointing = PPReadPointingDatabase(
        args.pointing_database,
        sconfigs.filters.observing_filters,
        sconfigs.input.pointing_sql_query,
        args.surveyname,
        fading_function_on=sconfigs.fadingfunction.fading_function_on,
    )

    # if we are going to compute the ephemerides, then we should pre-compute all
    # of the needed values derived from the pointing information.

    if sconfigs.input.ephemerides_type.casefold() != "external":
        verboselog("Pre-computing pointing information for ephemeris generation")
        filterpointing = precompute_pointing_information(filterpointing, args, sconfigs)

    # Set up the data readers.
    ephem_type = sconfigs.input.ephemerides_type
    ephem_primary = False
    reader = CombinedDataReader(ephem_primary=ephem_primary, verbose=True)

    # TODO: Once more ephemerides_types are added this should be wrapped in a EphemerisDataReader
    # That does the selection and checks. We are holding off adding this level of indirection until there
    # is a second ephemerides_type.

    if ephem_type.casefold() not in ["ar", "external"]:  # pragma: no cover
        pplogger.error(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
        sys.exit(f"PPReadAllInput: Unsupported value for ephemerides_type {ephem_type}")
    if ephem_type.casefold() == "external":
        reader.add_ephem_reader(EphemerisDataReader(args.input_ephemeris_file, sconfigs.input.eph_format))

    reader.add_aux_data_reader(OrbitAuxReader(args.orbinfile, sconfigs.input.aux_format))
    reader.add_aux_data_reader(CSVDataReader(args.paramsinput, sconfigs.input.aux_format))
    if sconfigs.activity.comet_activity is not None or sconfigs.lightcurve.lc_model is not None:
        reader.add_aux_data_reader(CSVDataReader(args.complex_parameters, sconfigs.input.aux_format))

    # Check to make sure the ObjIDs in all of the aux_data_readers are a match.
    reader.check_aux_object_ids()

    # In case of a large input file, the data is read in chunks. The
    # "size_serial_chunk" parameter in the config file assigns the chunk size.
    startChunk = 0
    endChunk = 0
    loopCounter = 0

    # Get number of objects in total.
    lenf = len(reader.aux_data_readers[0].obj_id_table)

    footprint = None
    if sconfigs.fov.camera_model == "footprint":
        verboselog("Creating sensor footprint object for filtering")
        footprint = Footprint(sconfigs.fov.footprint_path, args.surveyname)

    while endChunk < lenf:
        verboselog("Starting main Sorcha processing loop round {}".format(loopCounter))
        endChunk = startChunk + sconfigs.input.size_serial_chunk
        verboselog("Working on objects {}-{}".format(startChunk, endChunk))

        # Processing begins, all processing is done for chunks
        if sconfigs.input.ephemerides_type.casefold() == "external":
            verboselog("Reading in chunk of orbits and associated ephemeris from an external file")
            observations = reader.read_block(block_size=sconfigs.input.size_serial_chunk)
        else:
            verboselog("Ingest chunk of orbits")
            orbits_df = reader.read_aux_block(block_size=sconfigs.input.size_serial_chunk)

            if not sconfigs.expert.brute_force:
                verboselog("Cutting all objects too faint to be observed")
                verboselog(
                    "Number of rows BEFORE removing faint objects in faint object culling filter: "
                    + str(len(orbits_df.index))
                )
                orbits_df = PPFaintObjectCullingFilter(
                    orbits_df,
                    filterpointing,
                    sconfigs.filters.mainfilter,
                    sconfigs.filters.observing_filters,
                    sconfigs.lightcurve.lc_model,
                    sconfigs.activity.comet_activity,
                )
                verboselog(
                    "Number of rows After removing faint objects in faint object culling filter: "
                    + str(len(orbits_df.index))
                )
                if len(orbits_df) == 0:  # the above could feasibly nuke the entire dataframe, so...
                    pplogger.info(
                        "WARNING: no objects in this chunk pass faint object culling filter. Skipping to next chunk..."
                    )
                    startChunk = startChunk + sconfigs.input.size_serial_chunk
                    loopCounter = loopCounter + 1
                    continue

            verboselog("Starting ephemeris generation")
            observations = create_ephemeris(orbits_df, filterpointing, args, sconfigs)
            verboselog("Ephemeris generation completed")

        verboselog("Start post processing for this chunk")
        verboselog("Matching pointing database information to observations on rough camera footprint")

        # If the ephemeris file doesn't have any observations for the objects in the chunk
        # PPReadAllInput will return an empty dataframe. We thus log a warning.
        if len(observations.index) == 0:
            pplogger.info(
                "WARNING: no ephemeris observations found for these objects. Skipping to next chunk..."
            )
            startChunk = startChunk + sconfigs.input.size_serial_chunk
            loopCounter = loopCounter + 1
            continue

        observations = PPMatchPointingToObservations(observations, filterpointing)

        verboselog("Calculating apparent magnitudes...")
        observations = PPCalculateApparentMagnitude(
            observations,
            sconfigs.phasecurves.phase_function,
            sconfigs.filters.mainfilter,
            sconfigs.filters.othercolours,
            sconfigs.filters.observing_filters,
            sconfigs.activity.comet_activity,
            lightcurve_choice=sconfigs.lightcurve.lc_model,
            verbose=args.loglevel,
        )

        if sconfigs.expert.trailing_losses_on:
            verboselog("Calculating trailing losses...")
            dmagDetect = PPTrailingLoss(observations, "circularPSF")
            observations["PSFMagTrue"] = dmagDetect + observations["trailedSourceMagTrue"]
        else:
            observations["PSFMagTrue"] = observations["trailedSourceMagTrue"]

        if sconfigs.expert.vignetting_on:
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

        # Calulculating uncertainties section. (currently removed for DES)
        # ---------------------------------------------------------------------------------

        # verboselog("Calculating astrometric and photometric uncertainties...")
        # observations = PPAddUncertainties.addUncertainties(
        #     observations, sconfigs, args._rngs, verbose=args.loglevel
        # )

        if sconfigs.expert.randomization_on:
            verboselog(
                "Number of rows BEFORE randomizing astrometry and photometry: " + str(len(observations.index))
            )
            observations = PPRandomizeMeasurements.randomizeAstrometryAndPhotometry(
                observations, sconfigs, args._rngs, verbose=args.loglevel
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

        if sconfigs.fov.camera_model != "none" and len(observations.index) > 0:
            verboselog("Applying field-of-view filters...")
            verboselog("Number of rows BEFORE applying FOV filters: " + str(len(observations.index)))
            observations = PPApplyFOVFilter(
                observations,
                sconfigs,
                args._rngs,
                visits=args.visits,
                footprint=footprint,
                verbose=args.loglevel,
            )
            verboselog("Number of rows AFTER applying FOV filters: " + str(len(observations.index)))

        if sconfigs.expert.snr_limit_on and len(observations.index) > 0:
            verboselog(
                "Dropping observations with signal to noise ratio less than {}...".format(
                    sconfigs.expert.snr_limit
                )
            )
            verboselog("Number of rows BEFORE applying SNR limit filter: " + str(len(observations.index)))
            observations = PPSNRLimit(observations, sconfigs.expert.snr_limit)
            verboselog("Number of rows AFTER applying SNR limit filter: " + str(len(observations.index)))

        if sconfigs.expert.mag_limit_on and len(observations.index) > 0:
            verboselog("Dropping detections fainter than user-defined magnitude limit... ")
            verboselog("Number of rows BEFORE applying mag limit filter: " + str(len(observations.index)))
            observations = PPMagnitudeLimit(observations, sconfigs.expert.mag_limit)
            verboselog("Number of rows AFTER applying mag limit filter: " + str(len(observations.index)))

        if sconfigs.fadingfunction.fading_function_on and len(observations.index) > 0:
            verboselog("Applying detection efficiency fading function for DES...")
            verboselog("Number of rows BEFORE applying fading function: " + str(len(observations.index)))
            observations = DESFadingFunctionFilter(
                observations,
                args._rngs,
                verbose=args.loglevel,
            )
            verboselog("Number of rows AFTER applying fading function: " + str(len(observations.index)))

        if sconfigs.saturation.bright_limit_on and len(observations.index) > 0:
            verboselog("Dropping observations that are too bright...")
            verboselog("Number of rows BEFORE applying bright limit filter " + str(len(observations.index)))
            observations = PPBrightLimit(
                observations, sconfigs.filters.observing_filters, sconfigs.saturation.bright_limit
            )
            verboselog("Number of rows AFTER applying bright limit filter " + str(len(observations.index)))

        if sconfigs.linkingfilter.des_distance_cut_on and len(observations.index) > 0:
            verboselog("Number of rows BEFORE applying distance cuts: " + str(len(observations.index)))
            observations = des_distance_cut(
                observations,
                sconfigs.linkingfilter.des_distance_cut_upper,
                sconfigs.linkingfilter.des_distance_cut_lower,
            )
            verboselog("Number of rows AFTER applying distance cuts: " + str(len(observations.index)))

        if sconfigs.linkingfilter.des_motion_cut_on and len(observations.index) > 0:
            verboselog("Number of rows BEFORE applying motion cuts: " + str(len(observations.index)))
            observations = des_motion_cut(
                observations,
                sconfigs.linkingfilter.des_motion_cut_upper,
                sconfigs.linkingfilter.des_motion_cut_lower,
            )
            verboselog("Number of rows AFTER applying motion cuts: " + str(len(observations.index)))

        if sconfigs.linkingfilter.ssp_linking_on and len(observations.index) > 0:
            verboselog("Applying SSP linking filter...")
            verboselog("Number of rows BEFORE applying SSP linking filter: " + str(len(observations.index)))
            observations = PPLinkingFilter(
                observations,
                sconfigs.linkingfilter.ssp_detection_efficiency,
                sconfigs.linkingfilter.ssp_number_observations,
                sconfigs.linkingfilter.ssp_number_tracklets,
                sconfigs.linkingfilter.ssp_track_window,
                sconfigs.linkingfilter.ssp_separation_threshold,
                sconfigs.linkingfilter.ssp_maximum_time,
                sconfigs.linkingfilter.ssp_night_start_utc,
                drop_unlinked=sconfigs.linkingfilter.drop_unlinked,
            )
            observations.reset_index(drop=True, inplace=True)
            if len(observations.index) > 0:
                observations.drop("date_linked_MJD", axis=1, inplace=True)
                # use linking filter again for triplet detection.
                observations = PPLinkingFilter(
                    observations,
                    sconfigs.linkingfilter.ssp_detection_efficiency,
                    sconfigs.linkingfilter.ssp_number_observations,
                    3,
                    180,
                    sconfigs.linkingfilter.ssp_separation_threshold,
                    sconfigs.linkingfilter.ssp_maximum_time,
                    sconfigs.linkingfilter.ssp_night_start_utc,
                    drop_unlinked=sconfigs.linkingfilter.drop_unlinked,
                )
            observations.reset_index(drop=True, inplace=True)
            verboselog("Number of rows AFTER applying SSP linking filter: " + str(len(observations.index)))
            if len(observations.index) > 0 and sconfigs.linkingfilter.ssp_number_tracklets >= 3:
                verboselog("Applying DES discovery filter...")
                verboselog(
                    "Number of rows BEFORE applying DES Discovery filter: " + str(len(observations.index))
                )
                observations = DESDiscoveryFilter(observations)

                verboselog(
                    "Number of rows AFTER applying DES Discovery filter: " + str(len(observations.index))
                )
            else:
                verboselog("Minimum number of tracklets is < 3, DES Discovery filter is not applied")

        # write output if chunk not empty
        if len(observations.index) > 0:
            pplogger.info("Post processing completed for this chunk")
            pplogger.info("Outputting results for this chunk")
            PPWriteOutput(args, sconfigs, observations, verbose=args.loglevel)
            if args.stats is not None:
                stats(observations, args.stats, args.outpath, sconfigs)
        else:
            verboselog("No observations left in chunk. No output will be written for this chunk.")

        startChunk = startChunk + sconfigs.input.size_serial_chunk
        loopCounter = loopCounter + 1
        # end for

    if sconfigs.output.output_format == "sqlite3" and os.path.isfile(
        os.path.join(args.outpath, args.outfilestem + ".db")
    ):
        pplogger.info("Indexing output SQLite database...")
        PPIndexSQLDatabase(os.path.join(args.outpath, args.outfilestem + ".db"))

    pplogger.info("Sorcha process is completed.")
