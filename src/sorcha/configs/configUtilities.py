import logging
import sys

## below are the utility functions used to help validate the keywords, add more as needed


def check_key_exists(value, key_name):
    """
    Checks to confirm that a mandatory config file value is present and has been read into the dataclass as truthy. Returns an error if value is falsy

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key_name : string
        The key being checked.

    Returns
    ----------
    None.

    """

    if value is None:
        logging.error(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )
        sys.exit(
            f"ERROR: No value found for required key {key_name} in config file. Please check the file and try again."
        )


def check_key_doesnt_exist(value, key_name, reason):
    """
    Checks to confirm that a config file value is not present and has been read into the dataclass as falsy. Returns an error if value is truthy

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key_name : string
        The key being checked.

    reason : string
        reason given in the error message on why this value shouldn't be in the config file

    Returns
    ----------
    None.
    """

    # checks to make sure value doesn't exist
    if value is not None:
        logging.error(f"ERROR: {key_name} supplied in config file {reason}")
        sys.exit(f"ERROR: {key_name} supplied in config file {reason}")


def cast_as_int(value, key):
    # replaces PPGetIntOrExit: checks to make sure the value can be cast as an integer.
    """
    Checks to see if value can be cast as an interger.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as an integer

    """

    try:
        int(value)
    except ValueError:
        logging.error(f"ERROR: expected an int for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected an int for config parameter {key}. Check value in config file.")

    return int(value)


def cast_as_float(value, key):
    # replaces PPGetFloatOrExit: checks to make sure the value can be cast as a float.
    """
    Checks to see if value can be cast as a float.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as a float

    """

    try:
        float(value)
    except ValueError:
        logging.error(f"ERROR: expected a float for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a float for config parameter {key}. Check value in config file.")

    return float(value)


def cast_as_bool(value, key):
    # replaces PPGetBoolOrExit: checks to make sure the value can be cast as a bool.
    """
    Checks to see if value can be cast as a boolen.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.
    Returns
    ----------
    value as a boolen
    """

    str_value = str(value).strip()

    if str_value in ["true", "1", "yes", "y", "True"]:
        return True
    elif str_value in ["false", "0", "no", "n", "False"]:
        return False
    else:
        logging.error(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
        sys.exit(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")


def check_value_in_list(value, valuelist, key):
    # PPConfigParser often checks to see if a config variable is in a list of permissible variables, so this abstracts it out.
    """
    Checks to see if a config variable is in a list of permissible variables.

    Parameters
    -----------
    value : object attribute
        value of the config file value

    valuelist: list
        list of permissible values for attribute

    key : string
        The key being checked.
    Returns
    ----------
    None.

    """

    if value not in valuelist:
        logging.error(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )
        sys.exit(
            f"ERROR: value {value} for config parameter {key} not recognised. Expecting one of: {valuelist}."
        )


def cast_as_bool_or_set_default(value, key, default):
    # replaces PPGetBoolOrExit: checks to make sure the value can be cast as a bool.
    """
    Checks to see if value can be cast as a boolen and if not set (equals None) gives default bool.

    Parameters
    -----------
    value : object attribute
        value of the config file attribute

    key : string
        The key being checked.

    default : bool
        default bool if value is None

    Returns
    ----------
    value as a boolen
    """

    if value is not None:
        str_value = str(value).strip()

        if str_value in ["true", "1", "yes", "y", "True"]:
            return True
        elif str_value in ["false", "0", "no", "n", "False"]:
            return False
        else:
            logging.error(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
            sys.exit(f"ERROR: expected a bool for config parameter {key}. Check value in config file.")
    elif value is None:
        return default


def PrintConfigsToLog(sconfigs, cmd_args):
    """
    Prints all the values from the config file and command line to the log.

    Parameters
    -----------
    sconfigs : dataclass
        Dataclass of config file variables.

    cmd_args : dictionary
        Dictionary of command line arguments.

    Returns
    ----------
    None.

    """
    pplogger = logging.getLogger(__name__)

    pplogger.info("The config file used is located at " + str(cmd_args.configfile))
    pplogger.info("The physical parameters file used is located at " + cmd_args.paramsinput)
    pplogger.info("The orbits file used is located at " + cmd_args.orbinfile)
    if cmd_args.input_ephemeris_file:
        pplogger.info("The ephemerides file used is located at " + cmd_args.input_ephemeris_file)
    if cmd_args.output_ephemeris_file:
        pplogger.info("The output ephemerides file is located " + cmd_args.output_ephemeris_file)
    pplogger.info("The survey selected is: " + cmd_args.surveyname)

    if sconfigs.activity.comet_activity == "comet":
        pplogger.info("Cometary activity set to: " + str(sconfigs.activity.comet_activity))
    elif sconfigs.activity.comet_activity == None:
        pplogger.info("No cometary activity selected.")

    pplogger.info("Format of ephemerides file is: " + sconfigs.input.eph_format)
    pplogger.info("Format of auxiliary files is: " + sconfigs.input.aux_format)

    pplogger.info("Pointing database path is: " + cmd_args.pointing_database)
    pplogger.info("Pointing database required query is: " + sconfigs.input.pointing_sql_query)

    pplogger.info(
        "The number of objects processed in a single chunk is: " + str(sconfigs.input.size_serial_chunk)
    )
    pplogger.info("The main filter in which H is defined is " + sconfigs.filters.mainfilter)
    rescs = " ".join(str(f) for f in sconfigs.filters.observing_filters)
    pplogger.info("The filters included in the post-processing results are " + rescs)

    if sconfigs.filters.othercolours:
        othcs = " ".join(str(e) for e in sconfigs.filters.othercolours)
        pplogger.info("Thus, the colour indices included in the simulation are " + othcs)

    pplogger.info(
        "The apparent brightness is calculated using the following phase function model: "
        + sconfigs.phasecurves.phase_function
    )

    if sconfigs.expert.trailing_losses_on:
        pplogger.info("Computation of trailing losses is switched ON.")
    else:
        pplogger.info("Computation of trailing losses is switched OFF.")

    if sconfigs.expert.randomization_on:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched ON.")
    else:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched OFF.")

    if sconfigs.expert.vignetting_on:
        pplogger.info("Vignetting is switched ON.")
    else:
        pplogger.info("Vignetting is switched OFF.")

    if sconfigs.fov.camera_model == "footprint":
        pplogger.info("Footprint is modelled after the actual camera footprint.")
        if sconfigs.fov.footprint_path:
            pplogger.info("Loading camera footprint from " + sconfigs.fov.footprint_path)
        else:
            if cmd_args.surveyname.lower() in ["rubin_sim", "lsst"]:
                pplogger.info("Loading default LSST footprint LSST_detector_corners_100123.csv")
            if cmd_args.surveyname.lower() == "des":
                pplogger.info("Loading default DES footprint DES_ccd_corners.csv")
        if sconfigs.fov.footprint_edge_threshold:
            pplogger.info(
                "The footprint edge threshold is "
                + str(sconfigs.fov.footprint_edge_threshold)
                + " arcseconds"
            )
        else:
            pplogger.info("Default footprint edge threshold used (10px or 2 arcseconds).")
    elif sconfigs.fov.camera_model == "circle":
        pplogger.info("Footprint is circular.")
        if sconfigs.fov.fill_factor:
            pplogger.info(
                "The code will approximate chip gaps using filling factor: " + str(sconfigs.fov.fill_factor)
            )
        elif sconfigs.fov.circle_radius:
            pplogger.info(
                "A circular footprint will be applied with radius: " + str(sconfigs.fov.circle_radius)
            )
    elif sconfigs.fov.camera_model == "visits_footprint":
        pplogger.info("Footprint is the actual camera footprint for each observation.")
        pplogger.info("Loading camera footprint from sqlite database " + cmd_args.visits)
        pplogger.info("Visits database required query is: " + sconfigs.input.visits_query)

    else:
        pplogger.info("Camera footprint is turned OFF.")

    if sconfigs.saturation.bright_limit_on:
        pplogger.info("The upper saturation limit(s) is/are: " + str(sconfigs.saturation.bright_limit))
    else:
        pplogger.info("Saturation limit is turned OFF.")

    if sconfigs.expert.snr_limit_on:
        pplogger.info("The lower SNR limit is: " + str(sconfigs.expert.snr_limit))
    else:
        pplogger.info("SNR limit is turned OFF.")

    if sconfigs.expert.default_snr_cut:
        pplogger.info("Default SNR cut is ON. All observations with SNR < 2.0 will be removed.")

    if sconfigs.expert.mag_limit_on:
        pplogger.info("The magnitude limit is: " + str(sconfigs.expert.mag_limit))
    else:
        pplogger.info("Magnitude limit is turned OFF.")

    if sconfigs.fadingfunction.fading_function_on:
        pplogger.info("The detection efficiency fading function is ON.")
        pplogger.info(f"fading function {sconfigs.fadingfunction.fading_function_type} is selected.")
        if sconfigs.fadingfunction.fading_function_type == "general":
            pplogger.info(
                "The width parameter of the fading function has been set to: "
                + str(sconfigs.fadingfunction.fading_function_width)
            )
            pplogger.info(
                "The peak efficiency of the fading function has been set to: "
                + str(sconfigs.fadingfunction.fading_function_peak_efficiency)
            )
        elif sconfigs.fadingfunction.fading_function_type == "des_per_obs":
            pplogger.info(
                f"des_transient_efficency has been set to: {sconfigs.fadingfunction.des_transient_efficency}"
            )
    else:
        pplogger.info("The detection efficiency fading function is OFF.")

    if sconfigs.linkingfilter.ssp_linking_on:
        pplogger.info("Solar System Processing linking filter is turned ON.")
        pplogger.info("For SSP linking...")
        pplogger.info(
            "...the fractional detection efficiency is: "
            + str(sconfigs.linkingfilter.ssp_detection_efficiency)
        )
        pplogger.info(
            "...the minimum required number of observations in a tracklet is: "
            + str(sconfigs.linkingfilter.ssp_number_observations)
        )
        pplogger.info(
            "...the minimum required number of tracklets to form a track is: "
            + str(sconfigs.linkingfilter.ssp_number_tracklets)
        )
        pplogger.info(
            "...the maximum window of time in days of tracklets to be contained in to form a track is: "
            + str(sconfigs.linkingfilter.ssp_track_window)
        )
        pplogger.info(
            "...the minimum angular separation between observations in arcseconds is: "
            + str(sconfigs.linkingfilter.ssp_separation_threshold)
        )
        pplogger.info(
            "...the maximum temporal separation between subsequent observations in a tracklet in days is: "
            + str(sconfigs.linkingfilter.ssp_maximum_time)
        )
        pplogger.info(
            "...the time in UTC at which it is noon at the observatory location (in standard time) is "
            + str(sconfigs.linkingfilter.ssp_night_start_utc)
        )
        if not sconfigs.linkingfilter.drop_unlinked:
            pplogger.info("Unlinked objects will not be dropped.")
    elif sconfigs.linkingfilter.des_discovery_on:
        pplogger.info("Outer Solar System DES discovery filter is turned ON.")
        if sconfigs.linkingfilter.des_distance_cut_on:
            pplogger.info("Object distance cuts on.")
            pplogger.info(
                f"Distance cut bounds are: {sconfigs.linkingfilter.des_distance_cut_lower} to {sconfigs.linkingfilter.des_distance_cut_upper} au."
            )
        if sconfigs.linkingfilter.des_motion_cut_on:
            pplogger.info("Object motion cuts on.")
            pplogger.info(
                f"Motion cut bounds are: {sconfigs.linkingfilter.des_motion_cut_lower} to {sconfigs.linkingfilter.des_motion_cut_upper} deg/day."
            )
    else:
        pplogger.info("Solar System Processing linking filter is turned OFF.")
    pplogger.info("The auxiliary files used for emphemris generation...")
    pplogger.info("...the leap second file is: " + str(sconfigs.auxiliary.leap_seconds))
    pplogger.info(
        "...the historical Earth orientation specification file is: "
        + str(sconfigs.auxiliary.earth_historical)
    )
    pplogger.info(
        "...the prediction of the Earth's future orientation file is: "
        + str(sconfigs.auxiliary.earth_predict)
    )
    pplogger.info(
        "...the orientation information and physical constants for other bodies file is: "
        + str(sconfigs.auxiliary.orientation_constants)
    )
    pplogger.info(
        "...the Earth's position for ephemerides file is: " + str(sconfigs.auxiliary.planet_ephemeris)
    )
    pplogger.info(
        "...the regularly updated specification of the Earth's orientation file is: "
        + str(sconfigs.auxiliary.earth_high_precision)
    )
    pplogger.info(
        "...the observatory position information and Minor Planet Center (MPC) observatory codes file is: "
        + str(sconfigs.auxiliary.observatory_codes)
        + " and compressed file is: "
        + str(sconfigs.auxiliary.observatory_codes_compressed)
    )
    pplogger.info(
        "...the ephemerides for solar-system planets from JPL's Horizon system file is: "
        + str(sconfigs.auxiliary.jpl_planets)
    )
    pplogger.info(
        "...the ephemerides for solar-system small bodies from JPL's Horizon system file is: "
        + str(sconfigs.auxiliary.jpl_small_bodies)
    )
    pplogger.info("...the meta kernal file is : " + str(sconfigs.auxiliary.meta_kernel))
    if sconfigs.input.ephemerides_type == "ar":
        pplogger.info("ASSIST+REBOUND Simulation is turned ON.")
        pplogger.info("For ASSIST+REBOUND...")
        pplogger.info("...the field's angular FOV is: " + str(sconfigs.simulation.ar_ang_fov))
        pplogger.info("...the buffer around the FOV is: " + str(sconfigs.simulation.ar_fov_buffer))
        pplogger.info("...the picket interval is: " + str(sconfigs.simulation.ar_picket))
        pplogger.info("...the observatory code is: " + str(sconfigs.simulation.ar_obs_code))
        pplogger.info("...the healpix order is: " + str(sconfigs.simulation.ar_healpix_order))
        pplogger.info("...the number of sub-intervals is: " + str(sconfigs.simulation.ar_n_sub_intervals))
    else:
        pplogger.info("ASSIST+REBOUND Simulation is turned OFF.")

    if sconfigs.lightcurve.lc_model:
        pplogger.info("A lightcurve model is being applied.")
        pplogger.info("The lightcurve model is: " + sconfigs.lightcurve.lc_model)
    else:
        pplogger.info("No lightcurve model is being applied.")

    pplogger.info(
        "Output files will be saved in path: " + cmd_args.outpath + " with filestem " + cmd_args.outfilestem
    )
    pplogger.info("Output files will be saved as format: " + sconfigs.output.output_format)
    if sconfigs.output.position_decimals:
        pplogger.info(
            "In the output, positions will be rounded to "
            + str(sconfigs.output.position_decimals)
            + " decimal places."
        )
    else:
        pplogger.info("In the output, positions will not be rounded")
    if sconfigs.output.magnitude_decimals:
        pplogger.info(
            "In the output, magnitudes will be rounded to "
            + str(sconfigs.output.magnitude_decimals)
            + " decimal places."
        )
    else:
        pplogger.info("In the output, magnitudes will not be rounded")
    if isinstance(sconfigs.output.output_columns, list):
        pplogger.info("The output columns are set to: " + " ".join(sconfigs.output.output_columns))
    else:
        pplogger.info("The output columns are set to: " + sconfigs.output.output_columns)
