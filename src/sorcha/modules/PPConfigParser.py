import logging
import os
import sys
import numpy as np
import configparser

from sorcha.lightcurves.lightcurve_registration import LC_METHODS
from sorcha.activity.activity_registration import CA_METHODS


def log_error_and_exit(message: str) -> None:
    """Log a message to the error output file and terminal, then exit.

    Parameters
    ----------
    message : string
        The error message to be logged to the error output file.


    Returns
    --------
    None
    """

    logging.error(message)
    sys.exit(message)


def PPGetOrExit(config, section, key, message):
    """
    Checks to see if the config file parser has a key. If it does not, this
    function errors out and the code stops.

    Parameters
    -----------
    config : ConfigParser
        ConfigParser object containing configs.

    section : string
        Section of the key being checked.

    key : string)
        The key being checked.

    message : string
        The message to log and display if the key is not found.

    Returns
    ----------
    None.

    """

    if config.has_option(section, key):
        return config[section][key]
    else:
        logging.error(message)
        sys.exit(message)


def PPGetFloatOrExit(config, section, key, message):
    """
    Checks to see if a key in the config parser is present and can be read as a
    float. If it cannot, this function errors out and the code stops.

    Parameters
    -----------
    config : ConfigParser
        ConfigParser object containing configs.

    section : string
        section of the key being checked.

    key : string
        The key being checked.

    message : string
        The message to log and display if the key is not found.

    Returns
    ----------
    None.

    """

    if config.has_option(section, key):
        try:
            val = config.getfloat(section, key)
            return val
        except ValueError:
            logging.error(
                "ERROR: expected a float for config parameter {}. Check value in config file.".format(key)
            )
            sys.exit(
                "ERROR: expected a float for config parameter {}. Check value in config file.".format(key)
            )
    else:
        logging.error(message)
        sys.exit(message)


def PPGetIntOrExit(config, section, key, message):
    """
    Checks to see if a key in the config parser is present and can be read as an
    int. If it cannot, this function errors out and the code stops.

    Parameters
    -----------
    config : ConfigParser
        ConfigParser object containing configs.

    section : string
        Section of the key being checked.

    key : string
        The key being checked.

    message : string
        The message to log and display if the key is not found.

    Returns
    ----------
    None.

    """

    if config.has_option(section, key):
        try:
            val = config.getint(section, key)
            return val
        except ValueError:
            logging.error(
                "ERROR: expected an int for config parameter {}. Check value in config file.".format(key)
            )
            sys.exit(
                "ERROR: expected an int for config parameter {}. Check value in config file.".format(key)
            )
    else:
        logging.error(message)
        sys.exit(message)


def PPGetBoolOrExit(config, section, key, message):
    """
    Checks to see if a key in the config parser is present and can be read as a
    Boolean. If it cannot, this function errors out and the code stops.

    Parameters
    -----------
    config : ConfigParser object
        ConfigParser object containing configs.

    section : string
        Section of the key being checked.

    key : string
        The key being checked.

    message : string
        The message to log and display if the key is not found.

    Returns
    ----------
    None.

    """

    if config.has_option(section, key):
        try:
            val = config.getboolean(section, key)
            return val
        except ValueError:
            logging.error(f"ERROR: {key} could not be converted to a Boolean.")
            sys.exit(f"ERROR: {key} could not be converted to a Boolean.")
    else:
        logging.error(message)
        sys.exit(message)


def PPGetValueAndFlag(config, section, key, type_wanted):
    """
    Obtains a value from the config flag, forcing it to be the specified
    type and error-handling if it can't be forced. If the value is not present
    in the config fie, the flag is set to False; if it is, the flag is True.

    Parameters
    -----------
    config : ConfigParser
        ConfigParser object containing configs.

    section : string
        Section of the key being checked.

    key : string
        The key being checked.

    type_wanted : string
        The type the value should be forced to.
        Accepts int, float, none (for no type-forcing).

    Returns
    ----------
    value : any type
        The value of the key, with type dependent on type_wanted.
        Will be None if the key is not present.

    flag : boolean
        Will be False if the key is not present in the config file
        and True if it is.

    """

    if type_wanted == "int":
        try:
            value = config.getint(section, key, fallback=None)
        except ValueError:
            logging.error(
                "ERROR: expected an int for config parameter {}. Check value in config file.".format(key)
            )
            sys.exit(
                "ERROR: expected an int for config parameter {}. Check value in config file.".format(key)
            )
    elif type_wanted == "float":
        try:
            value = config.getfloat(section, key, fallback=None)
        except ValueError:
            logging.error(
                "ERROR: expected a float for config parameter {}. Check value in config file.".format(key)
            )
            sys.exit(
                "ERROR: expected a float for config parameter {}. Check value in config file.".format(key)
            )
    elif type_wanted == "none":
        value = config.get(section, key, fallback=None)
    else:
        logging.error("ERROR: internal error: type not recognised.")
        sys.exit("ERROR: internal error: type not recognised.")

    if value is None:
        flag = False
    else:
        flag = True

    return value, flag


def PPFindFileOrExit(arg_fn, argname):
    """Checks to see if a file given by a filename exists. If it doesn't,
    this fails gracefully and exits to the command line.

    Parameters
    -----------
    arg_fn : string
        The filepath/name of the file to be checked.

    argname : string
        The name of the argument being checked. Used for error message.

    Returns
    ----------
    arg_fn : string
        The filepath/name of the file to be checked.

    """

    pplogger = logging.getLogger(__name__)

    if os.path.exists(arg_fn):
        return arg_fn
    else:
        pplogger.error("ERROR: filename {} supplied for {} argument does not exist.".format(arg_fn, argname))
        sys.exit("ERROR: filename {} supplied for {} argument does not exist.".format(arg_fn, argname))


def PPFindDirectoryOrExit(arg_fn, argname):
    """Checks to see if a directory given by a filepath exists. If it doesn't,
    this fails gracefully and exits to the command line.

    Parameters
    -----------
    arg_fn : string
        The filepath of the directory to be checked.

    argname : string
        The name of the argument being checked. Used for error message.

    Returns
    ----------
    arg_fn : string
        The filepath of the directory to be checked.
    """

    pplogger = logging.getLogger(__name__)

    if os.path.isdir(arg_fn):
        return arg_fn
    else:
        pplogger.error("ERROR: filepath {} supplied for {} argument does not exist.".format(arg_fn, argname))
        sys.exit("ERROR: filepath {} supplied for {} argument does not exist.".format(arg_fn, argname))


def PPCheckFiltersForSurvey(survey_name, observing_filters):
    """
    When given a list of filters, this function checks to make sure they exist in the
    user-selected survey, and if the filters given in the config file do not match the
    survey filters, the function exits the program with an error.

    Parameters
    -----------
    survey_name : string
        Survey name. Currently only "LSST", "lsst" accepted.

    observing_filters: list of strings
        Observation filters of interest.

    Returns
    ----------
    None.

    Notes
    -------
    Currently only has options for LSST, but can be expanded upon later.

    """

    pplogger = logging.getLogger(__name__)

    if survey_name in ["rubin_sim", "RUBIN_SIM"]:
        lsst_filters = ["u", "g", "r", "i", "z", "y"]
        filters_ok = all(elem in lsst_filters for elem in observing_filters)

        if not filters_ok:
            bad_list = np.setdiff1d(observing_filters, lsst_filters)
            pplogger.error(
                "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                    bad_list, survey_name
                )
            )
            pplogger.error("Accepted {} filters: {}".format("LSST", lsst_filters))
            pplogger.error("Change observing_filters in config file or select another survey.")
            sys.exit(
                "ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.".format(
                    bad_list, survey_name
                )
            )


def PPConfigFileParser(configfile, survey_name):
    """
    Parses the config file, error-handles, then assigns the values into a single
    dictionary, which is passed out.

    Parameters
    -----------
    configfile : string
        Filepath/name of config file.

    survey_name : string
        Survey name. Currently only "LSST", "lsst" accepted.

    Returns
    ----------
    config_dict : dictionary
        Dictionary of config file variables.

    Notes
    -------
        We chose not to use the original ConfigParser object for readability: it's a dict of
        dicts, so calling the various values can become quite unwieldy.

    """
    pplogger = logging.getLogger(__name__)

    # Save a raw copy of the configuration to the logs as a backup.
    with open(configfile, "r") as file:
        pplogger.info(f"Copy of configuration file {configfile}:\n{file.read()}")

    config = configparser.ConfigParser()
    config.read(configfile)

    config_dict = {}

    # INPUT

    config_dict["eph_format"] = PPGetOrExit(
        config, "INPUT", "eph_format", "ERROR: no ephemerides file format is specified."
    ).lower()
    if config_dict["eph_format"] not in ["csv", "whitespace", "hdf5"]:
        pplogger.error("ERROR: eph_format should be either csv, whitespace, or hdf5.")
        sys.exit("ERROR: eph_format should be either either csv, whitespace, or hdf5.")

    config_dict["aux_format"] = PPGetOrExit(
        config, "INPUT", "aux_format", "ERROR: no auxiliary data format specified."
    ).lower()
    if config_dict["aux_format"] not in ["comma", "whitespace", "csv"]:
        pplogger.error("ERROR: aux_format should be either comma, csv, or whitespace.")
        sys.exit("ERROR: aux_format should be either comma, csv, or whitespace.")

    config_dict["ephemerides_type"] = PPGetOrExit(
        config, "INPUT", "ephemerides_type", "ERROR: no ephemerides type provided."
    ).lower()
    if config_dict["ephemerides_type"] not in ["ar", "external"]:
        pplogger.error('ERROR: ephemerides_type not recognised - expecting either "ar" or "external".')
        sys.exit('ERROR: ephemerides_type not recognised - expecting either "ar" or "external".')

    config_dict["size_serial_chunk"] = PPGetIntOrExit(
        config, "INPUT", "size_serial_chunk", "ERROR: size_serial_chunk not specified."
    )
    if config_dict["size_serial_chunk"] < 1:
        pplogger.error("ERROR: size_serial_chunk is zero or negative.")
        sys.exit("ERROR: size_serial_chunk is zero or negative.")

    config_dict["pointing_sql_query"] = PPGetOrExit(
        config, "INPUT", "pointing_sql_query", "ERROR: no pointing database SQLite3 query provided."
    )

    # ACTIVITY

    config_dict["comet_activity"] = config.get("ACTIVITY", "comet_activity", fallback=None)
    config_dict["comet_activity"] = (
        None if config_dict["comet_activity"] == "none" else config_dict["comet_activity"]
    )

    # If the user defined a specific comet_activity value, but the model has not been registered, exit the program.
    if config_dict["comet_activity"] and config_dict["comet_activity"] not in CA_METHODS:
        log_error_and_exit(
            f"The requested comet activity model, '{config_dict['comet_activity']}', is not registered. Available comet activity models are: {list(CA_METHODS.keys())}"
        )

    # FILTERS

    obsfilters = PPGetOrExit(
        config, "FILTERS", "observing_filters", "ERROR: observing_filters config file variable not provided."
    )
    config_dict["observing_filters"] = [e.strip() for e in obsfilters.split(",")]

    PPCheckFiltersForSurvey(survey_name, config_dict["observing_filters"])

    # SATURATION

    bright_limits, config_dict["bright_limit_on"] = PPGetValueAndFlag(
        config, "SATURATION", "bright_limit", "none"
    )

    try:
        bright_list = [float(e.strip()) for e in bright_limits.split(",")]
    except ValueError:
        pplogger.error("ERROR: could not parse brightness limits. Check formatting and try again.")
        sys.exit("ERROR: could not parse brightness limits. Check formatting and try again.")

    if len(bright_list) == 1:
        config_dict["bright_limit"] = bright_list[0]
    else:
        if len(bright_list) != len(config_dict["observing_filters"]):
            pplogger.error(
                "ERROR: list of saturation limits is not the same length as list of observing filters."
            )
            sys.exit("ERROR: list of saturation limits is not the same length as list of observing filters.")
        config_dict["bright_limit"] = bright_list

    # PHASECURVES

    config_dict["phase_function"] = PPGetOrExit(
        config, "PHASECURVES", "phase_function", "ERROR: phase function not defined."
    )

    # FOV

    config_dict["camera_model"] = PPGetOrExit(
        config, "FOV", "camera_model", "ERROR: camera model not defined."
    )

    if config_dict["camera_model"] not in ["circle", "footprint", "none"]:
        pplogger.error('ERROR: camera_model should be either "circle" or "footprint".')
        sys.exit('ERROR: camera_model should be either "circle" or "footprint".')

    elif config_dict["camera_model"] == "footprint":
        config_dict["footprint_path"], external_file = PPGetValueAndFlag(
            config, "FOV", "footprint_path", "none"
        )
        if external_file:
            PPFindFileOrExit(config_dict["footprint_path"], "footprint_path")
        elif survey_name.lower() not in ["lsst", "rubin_sim"]:
            log_error_and_exit(
                "a default detector footprint is currently only provided for LSST; please provide your own footprint file."
            )

        config_dict["footprint_edge_threshold"], _ = PPGetValueAndFlag(
            config, "FOV", "footprint_edge_threshold", "float"
        )

        if config.has_option("FOV", "fill_factor"):
            pplogger.error('ERROR: fill factor supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: fill factor supplied in config file but camera model is not "circle".')
        elif config.has_option("FOV", "circle_radius"):
            pplogger.error('ERROR: circle radius supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: circle radius supplied in config file but camera model is not "circle".')

    elif (config_dict["camera_model"]) == "circle":
        config_dict["fill_factor"], _ = PPGetValueAndFlag(config, "FOV", "fill_factor", "float")
        config_dict["circle_radius"], _ = PPGetValueAndFlag(config, "FOV", "circle_radius", "float")

        if not config_dict["fill_factor"] and not config_dict["circle_radius"]:
            pplogger.error(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
            sys.exit(
                'ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.'
            )
        elif config_dict["fill_factor"]:
            if config_dict["fill_factor"] < 0.0 or config_dict["fill_factor"] > 1.0:
                pplogger.error("ERROR: fill_factor out of bounds. Must be between 0 and 1.")
                sys.exit("ERROR: fill_factor out of bounds. Must be between 0 and 1.")
        elif config_dict["circle_radius"]:
            if config_dict["circle_radius"] < 0.0:
                pplogger.error("ERROR: circle_radius is negative.")
                sys.exit("ERROR: circle_radius is negative.")

        if config.has_option("FOV", "footprint_edge_threshold"):
            pplogger.error(
                'ERROR: footprint edge threshold supplied in config file but camera model is not "footprint".'
            )
            sys.exit(
                'ERROR: footprint edge threshold supplied in config file but camera model is not "footprint".'
            )

    # FADINGFUNCTION

    config_dict["fading_function_on"] = PPGetBoolOrExit(
        config, "FADINGFUNCTION", "fading_function_on", "ERROR: fading_function_on flag not present."
    )

    if config_dict["fading_function_on"]:
        config_dict["fading_function_width"] = PPGetFloatOrExit(
            config,
            "FADINGFUNCTION",
            "fading_function_width",
            "ERROR: fading function is on but no fading_function_width supplied.",
        )
        config_dict["fading_function_peak_efficiency"] = PPGetFloatOrExit(
            config,
            "FADINGFUNCTION",
            "fading_function_peak_efficiency",
            "ERROR: fading function is on but no fading_function_peak_efficiency supplied.",
        )

        if config_dict["fading_function_width"] <= 0.0 or config_dict["fading_function_width"] > 0.5:
            pplogger.error(
                "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
            )
            sys.exit(
                "ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5."
            )

        if (
            config_dict["fading_function_peak_efficiency"] < 0.0
            or config_dict["fading_function_peak_efficiency"] > 1.0
        ):
            pplogger.error("ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.")
            sys.exit("ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.")

    elif config.has_option("FADINGFUNCTION", "fading_function_width"):
        pplogger.error(
            "ERROR: fading_function_width supplied in config file but fading_function_on is False."
        )
        sys.exit("ERROR: fading_function_width supplied in config file but fading_function_on is False.")
    elif config.has_option("FADINGFUNCTION", "fading_function_peak_efficiency"):
        pplogger.error(
            "ERROR: fading_function_peak_efficiency supplied in config file but fading_function_on is False."
        )
        sys.exit(
            "ERROR: fading_function_peak_efficiency supplied in config file but fading_function_on is False."
        )

    # LINKINGFILTER

    config_dict["SSP_separation_threshold"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_separation_threshold", "float"
    )
    config_dict["SSP_number_observations"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_number_observations", "int"
    )
    config_dict["SSP_number_tracklets"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_number_tracklets", "int"
    )
    config_dict["SSP_track_window"], _ = PPGetValueAndFlag(config, "LINKINGFILTER", "SSP_track_window", "int")
    config_dict["SSP_detection_efficiency"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_detection_efficiency", "float"
    )
    config_dict["SSP_maximum_time"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_maximum_time", "float"
    )
    config_dict["SSP_night_start_utc"], _ = PPGetValueAndFlag(
        config, "LINKINGFILTER", "SSP_night_start_utc", "float"
    )

    SSPvariables = [
        config_dict["SSP_separation_threshold"],
        config_dict["SSP_number_observations"],
        config_dict["SSP_number_tracklets"],
        config_dict["SSP_track_window"],
        config_dict["SSP_detection_efficiency"],
        config_dict["SSP_maximum_time"],
        config_dict["SSP_night_start_utc"],
    ]

    # the below if-statement explicitly checks for None so a zero triggers the correct error
    if all(v is not None for v in SSPvariables):
        if config_dict["SSP_number_observations"] < 1:
            pplogger.error("ERROR: SSP_number_observations is zero or negative.")
            sys.exit("ERROR: SSP_number_observations is zero or negative.")

        if config_dict["SSP_number_tracklets"] < 1:
            pplogger.error("ERROR: SSP_number_tracklets is zero or less.")
            sys.exit("ERROR: SSP_number_tracklets is zero or less.")

        if config_dict["SSP_track_window"] <= 0.0:
            pplogger.error("ERROR: SSP_track_window is negative.")
            sys.exit("ERROR: SSP_track_window is negative.")

        if config_dict["SSP_detection_efficiency"] > 1.0 or config_dict["SSP_detection_efficiency"] > 1.0:
            pplogger.error("ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).")
            sys.exit("ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).")

        if config_dict["SSP_separation_threshold"] <= 0.0:
            pplogger.error("ERROR: SSP_separation_threshold is zero or negative.")
            sys.exit("ERROR: SSP_separation_threshold is zero or negative.")

        if config_dict["SSP_maximum_time"] < 0:
            pplogger.error("ERROR: SSP_maximum_time is negative.")
            sys.exit("ERROR: SSP_maximum_time is negative.")

        if config_dict["SSP_night_start_utc"] > 24.0 or config_dict["SSP_night_start_utc"] < 0.0:
            pplogger.error("ERROR: SSP_night_start_utc must be a valid time between 0 and 24 hours.")
            sys.exit("ERROR: SSP_night_start_utc must be a valid time between 0 and 24 hours.")

        config_dict["SSP_linking_on"] = True

    elif not any(SSPvariables):
        config_dict["SSP_linking_on"] = False

    else:
        pplogger.error(
            "ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off."
        )
        sys.exit(
            "ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off."
        )

    try:
        config_dict["drop_unlinked"] = config.getboolean("LINKINGFILTER", "drop_unlinked", fallback=True)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for drop_unlinked as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for drop_unlinked as a boolean. Check formatting and try again."
        )

    # SIMULATION

    if config_dict["ephemerides_type"] == "ar":
        config_dict["ar_ang_fov"] = PPGetFloatOrExit(
            config, "SIMULATION", "ar_ang_fov", "ERROR: ar_ang_fov not specified."
        )

        config_dict["ar_fov_buffer"] = PPGetFloatOrExit(
            config, "SIMULATION", "ar_fov_buffer", "ERROR: ar_fov_buffer not specified."
        )

        config_dict["ar_picket"] = PPGetIntOrExit(
            config, "SIMULATION", "ar_picket", "ERROR: ar_picket not specified."
        )

        config_dict["ar_obs_code"] = PPGetOrExit(
            config, "SIMULATION", "ar_obs_code", "ERROR: ar_picket not specified."
        )

        config_dict["ar_healpix_order"] = PPGetIntOrExit(
            config, "SIMULATION", "ar_healpix_order", "ERROR: ar_healpix_order not specified."
        )

    # OUTPUT

    config_dict["output_format"] = PPGetOrExit(
        config, "OUTPUT", "output_format", "ERROR: output format not specified."
    ).lower()
    if config_dict["output_format"] not in ["csv", "sqlite3", "hdf5", "h5"]:
        pplogger.error("ERROR: output_format should be either csv, sqlite3 or hdf5.")
        sys.exit("ERROR: output_format should be either csv, sqlite3 or hdf5.")

    config_dict["output_columns"] = PPGetOrExit(
        config, "OUTPUT", "output_columns", "ERROR: output size not specified."
    )

    if (config_dict["output_columns"] not in ["basic", "all"]) and ("," not in config_dict["output_columns"]):
        pplogger.error(
            "ERROR: output_columns not recognised. Must be 'basic', 'all', or a comma-separated list of columns."
        )
        sys.exit(
            "ERROR: output_columns not recognised. Must be 'basic', 'all', or a comma-separated list of columns."
        )

    # note: if providing a comma-separated list of column names, this is NOT ERROR-HANDLED
    # as we have no way of knowing ahead of time of columns that user-generated code or add-ons may add.

    if (
        "," in config_dict["output_columns"]
    ):  # assume list of column names: turn into a list and strip whitespace
        config_dict["output_columns"] = [
            colname.strip(" ") for colname in config_dict["output_columns"].split(",")
        ]

    config_dict["position_decimals"], _ = PPGetValueAndFlag(config, "OUTPUT", "position_decimals", "int")
    config_dict["magnitude_decimals"], _ = PPGetValueAndFlag(config, "OUTPUT", "magnitude_decimals", "int")

    if config_dict["position_decimals"] and config_dict["position_decimals"] < 0:
        pplogger.error("ERROR: decimal places config variables cannot be negative.")
        sys.exit("ERROR: decimal places config variables cannot be negative.")

    if config_dict["magnitude_decimals"] and config_dict["magnitude_decimals"] < 0:
        pplogger.error("ERROR: decimal places config variables cannot be negative.")
        sys.exit("ERROR: decimal places config variables cannot be negative.")

    # EXPERT

    config_dict["SNR_limit"], config_dict["SNR_limit_on"] = PPGetValueAndFlag(
        config, "EXPERT", "SNR_limit", "float"
    )
    config_dict["mag_limit"], config_dict["mag_limit_on"] = PPGetValueAndFlag(
        config, "EXPERT", "mag_limit", "float"
    )

    if config_dict["SNR_limit_on"] and config_dict["SNR_limit"] < 0:
        pplogger.error("ERROR: SNR limit is negative.")
        sys.exit("ERROR: SNR limit is negative.")

    if config_dict["mag_limit_on"] and config_dict["mag_limit"] < 0:
        pplogger.error("ERROR: magnitude limit is negative.")
        sys.exit("ERROR: magnitude limit is negative.")

    if config_dict["mag_limit_on"] and config_dict["SNR_limit_on"]:
        pplogger.error(
            "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
        )
        sys.exit(
            "ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file."
        )

    try:
        config_dict["ar_use_integrate"] = config.getboolean("EXPERT", "ar_use_integrate", fallback=False)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for ar_use_integrate as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for ar_use_integrate as a boolean. Check formatting and try again."
        )

    try:
        config_dict["trailing_losses_on"] = config.getboolean("EXPERT", "trailing_losses_on", fallback=True)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for trailing_losses_on as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for trailing_losses_on as a boolean. Check formatting and try again."
        )

    try:
        config_dict["default_SNR_cut"] = config.getboolean("EXPERT", "default_SNR_cut", fallback=True)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for default_SNR_cut as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for default_SNR_cut as a boolean. Check formatting and try again."
        )

    try:
        config_dict["randomization_on"] = config.getboolean("EXPERT", "randomization_on", fallback=True)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for randomization_on as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for randomization_on as a boolean. Check formatting and try again."
        )

    try:
        config_dict["vignetting_on"] = config.getboolean("EXPERT", "vignetting_on", fallback=True)
    except ValueError:
        pplogger.error(
            "ERROR: could not parse value for vignetting_on as a boolean. Check formatting and try again."
        )
        sys.exit(
            "ERROR: could not parse value for vignetting_on as a boolean. Check formatting and try again."
        )

    # LIGHTCURVEß

    config_dict["lc_model"] = config.get("LIGHTCURVE", "lc_model", fallback=None)
    config_dict["lc_model"] = None if config_dict["lc_model"] == "none" else config_dict["lc_model"]

    # If the user defined a lightcurve model, but the model has not been registered, exit the program.
    if config_dict["lc_model"] and config_dict["lc_model"] not in LC_METHODS:
        log_error_and_exit(
            f"The requested light curve model, '{config_dict['lc_model']}', is not registered. Available lightcurve options are: {list(LC_METHODS.keys())}"
        )

    return config_dict


def PPPrintConfigsToLog(configs, cmd_args):
    """
    Prints all the values from the config file and command line to the log.

    Parameters
    -----------
    configs : dictionary
        Dictionary of config file variables.

    cmd_args : dictionary
        Dictionary of command line arguments.

    Returns
    ----------
    None.

    """

    pplogger = logging.getLogger(__name__)

    pplogger.info("The config file used is located at " + cmd_args.configfile)
    pplogger.info("The physical parameters file used is located at " + cmd_args.paramsinput)
    pplogger.info("The orbits file used is located at " + cmd_args.orbinfile)
    if cmd_args.oifoutput:
        pplogger.info("The ephemerides file used is located at " + cmd_args.oifoutput)
    if cmd_args.output_ephemeris_file:
        pplogger.info("The output ephemerides file is located " + cmd_args.output_ephemeris_file)
    pplogger.info("The survey selected is: " + cmd_args.surveyname)

    if configs["comet_activity"] == "comet":
        pplogger.info("Cometary activity set to: " + str(configs["comet_activity"]))
    elif configs["comet_activity"] == "none":
        pplogger.info("No cometary activity selected.")

    pplogger.info("Format of ephemerides file is: " + configs["eph_format"])
    pplogger.info("Format of auxiliary files is: " + configs["aux_format"])

    pplogger.info("Pointing database path is: " + cmd_args.pointing_database)
    pplogger.info("Pointing database required query is: " + configs["pointing_sql_query"])

    pplogger.info(
        "The number of objects processed in a single chunk is: " + str(configs["size_serial_chunk"])
    )
    pplogger.info("The main filter in which H is defined is " + configs["mainfilter"])
    rescs = " ".join(str(f) for f in configs["observing_filters"])
    pplogger.info("The filters included in the post-processing results are " + rescs)

    if configs["othercolours"]:
        othcs = " ".join(str(e) for e in configs["othercolours"])
        pplogger.info("Thus, the colour indices included in the simulation are " + othcs)

    pplogger.info(
        "The apparent brightness is calculated using the following phase function model: "
        + configs["phase_function"]
    )

    if configs["ar_use_integrate"]:
        pplogger.info("ASSIST+REBOUND integration is ON. Integrate or interpolate will NOT be used.")
    else:
        pplogger.info("ASSIST+REBOUND integration is OFF. Integrate or interpolate will be used.")

    if configs["trailing_losses_on"]:
        pplogger.info("Computation of trailing losses is switched ON.")
    else:
        pplogger.info("Computation of trailing losses is switched OFF.")

    if configs["randomization_on"]:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched ON.")
    else:
        pplogger.info("Randomization of position and magnitude around uncertainties is switched OFF.")

    if configs["vignetting_on"]:
        pplogger.info("Vignetting is switched ON.")
    else:
        pplogger.info("Vignetting is switched OFF.")

    if configs["camera_model"] == "footprint":
        pplogger.info("Footprint is modelled after the actual camera footprint.")
        if configs["footprint_path"]:
            pplogger.info("Loading camera footprint from " + configs["footprint_path"])
        else:
            pplogger.info("Loading default LSST footprint LSST_detector_corners_100123.csv")
    elif configs["camera_model"] == "circle":
        pplogger.info("Footprint is circular.")
        if configs["fill_factor"]:
            pplogger.info(
                "The code will approximate chip gaps using filling factor: " + str(configs["fill_factor"])
            )
        elif configs["circle_radius"]:
            pplogger.info(
                "A circular footprint will be applied with radius: " + str(configs["circle_radius"])
            )
    else:
        pplogger.info("Camera footprint is turned OFF.")

    if configs["bright_limit_on"]:
        pplogger.info("The upper saturation limit(s) is/are: " + str(configs["bright_limit"]))
    else:
        pplogger.info("Saturation limit is turned OFF.")

    if configs["SNR_limit_on"]:
        pplogger.info("The lower SNR limit is: " + str(configs["SNR_limit"]))
    else:
        pplogger.info("SNR limit is turned OFF.")

    if configs["default_SNR_cut"]:
        pplogger.info("Default SNR cut is ON. All observations with SNR < 2.0 will be removed.")

    if configs["mag_limit_on"]:
        pplogger.info("The magnitude limit is: " + str(configs["mag_limit"]))
    else:
        pplogger.info("Magnitude limit is turned OFF.")

    if configs["fading_function_on"]:
        pplogger.info("The detection efficiency fading function is ON.")
        pplogger.info(
            "The width parameter of the fading function has been set to: "
            + str(configs["fading_function_width"])
        )
        pplogger.info(
            "The peak efficiency of the fading function has been set to: "
            + str(configs["fading_function_peak_efficiency"])
        )
    else:
        pplogger.info("The detection efficiency fading function is OFF.")

    if configs["SSP_linking_on"]:
        pplogger.info("Solar System Processing linking filter is turned ON.")
        pplogger.info("For SSP linking...")
        pplogger.info(
            "...the fractional detection efficiency is: " + str(configs["SSP_detection_efficiency"])
        )
        pplogger.info(
            "...the minimum required number of observations in a tracklet is: "
            + str(configs["SSP_number_observations"])
        )
        pplogger.info(
            "...the minimum required number of tracklets to form a track is: "
            + str(configs["SSP_number_tracklets"])
        )
        pplogger.info(
            "...the maximum window of time in days of tracklets to be contained in to form a track is: "
            + str(configs["SSP_track_window"])
        )
        pplogger.info(
            "...the minimum angular separation between observations in arcseconds is: "
            + str(configs["SSP_separation_threshold"])
        )
        pplogger.info(
            "...the maximum temporal separation between subsequent observations in a tracklet in days is: "
            + str(configs["SSP_maximum_time"])
        )
        if not configs["drop_unlinked"]:
            pplogger.info("Unlinked objects will not be dropped.")
    else:
        pplogger.info("Solar System Processing linking filter is turned OFF.")

    if configs["ephemerides_type"] == "ar":
        pplogger.info("ASSIST+REBOUND Simulation is turned ON.")
        pplogger.info("For ASSIST+REBOUND...")
        pplogger.info("...the field's angular FOV is: " + str(configs["ar_ang_fov"]))
        pplogger.info("...the buffer around the FOV is: " + str(configs["ar_fov_buffer"]))
        pplogger.info("...the picket interval is: " + str(configs["ar_picket"]))
        pplogger.info("...the observatory code is: " + str(configs["ar_obs_code"]))
        pplogger.info("...the healpix order is: " + str(configs["ar_healpix_order"]))
    else:
        pplogger.info("ASSIST+REBOUND Simulation is turned OFF.")

    if configs["lc_model"]:
        pplogger.info("A lightcurve model is being applied.")
        pplogger.info("The lightcurve model is: " + configs["lc_model"])
    else:
        pplogger.info("No lightcurve model is being applied.")

    pplogger.info(
        "Output files will be saved in path: " + cmd_args.outpath + " with filestem " + cmd_args.outfilestem
    )
    pplogger.info("Output files will be saved as format: " + configs["output_format"])
    pplogger.info(
        "In the output, positions will be rounded to "
        + str(configs["position_decimals"])
        + " decimal places."
    )
    pplogger.info(
        "In the output, magnitudes will be rounded to "
        + str(configs["magnitude_decimals"])
        + " decimal places."
    )
    if isinstance(configs["output_columns"], list):
        pplogger.info("The output columns are set to: " + " ".join(configs["output_columns"]))
    else:
        pplogger.info("The output columns are set to: " + configs["output_columns"])
