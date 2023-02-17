#!/usr/bin/python
# Parsing and error handling of the config file.

import logging
import os
import sys
import numpy as np
import configparser


def PPGetOrExit(config, section, key, message):

    if config.has_option(section, key):
        return config[section][key]
    else:
        logging.error(message)
        sys.exit(message)


def PPGetFloatOrExit(config, section, key, message):

    if config.has_option(section, key):
        try:
            val = config.getfloat(section, key)
            return val
        except ValueError:
            logging.error("ERROR: expected a float for config parameter {}. Check value in config file.".format(key))
            sys.exit("ERROR: expected a float for config parameter {}. Check value in config file.".format(key))
    else:
        logging.error(message)
        sys.exit(message)


def PPGetIntOrExit(config, section, key, message):

    if config.has_option(section, key):
        try:
            val = config.getint(section, key)
            return val
        except ValueError:
            logging.error("ERROR: expected an int for config parameter {}. Check value in config file.".format(key))
            sys.exit("ERROR: expected an int for config parameter {}. Check value in config file.".format(key))
    else:
        logging.error(message)
        sys.exit(message)


def PPGetBoolOrExit(config, section, key, message):

    if config.has_option(section, key):
        try:
            val = config.getboolean(section, key)
            return val
        except ValueError:
            logging.error(f'ERROR: {key} could not be converted to a Boolean.')
            sys.exit(f'ERROR: {key} could not be converted to a Boolean.')
    else:
        logging.error(message)
        sys.exit(message)


def PPGetValueAndFlag(config, section, key, type_wanted):
    """Obtains a value from the config flag, forcing it to be the specified
    type and error-handling if it can't be forced. If the value is not present
    in the config fie, the flag is set to False; if it is, the flag is True.
    """

    if type_wanted == "int":
        try:
            value = config.getint(section, key, fallback=None)
        except ValueError:
            logging.error("ERROR: expected an int for config parameter {}. Check value in config file.".format(key))
            sys.exit("ERROR: expected an int for config parameter {}. Check value in config file.".format(key))
    elif type_wanted == "float":
        try:
            value = config.getfloat(section, key, fallback=None)
        except ValueError:
            logging.error("ERROR: expected a float for config parameter {}. Check value in config file.".format(key))
            sys.exit("ERROR: expected a float for config parameter {}. Check value in config file.".format(key))
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
    """
    Author: Steph Merritt

    Description: Checks to see if the filename given by arg_fn actually exists. If it doesn't,
    this fails gracefully and exits to the command line.

    Mandatory input:    string, arg_fn, string filename passed by command line argument
                        string, argname,  name/flag of the argument printed in error message

    Output:             string, arg_fn unchanged
    """

    pplogger = logging.getLogger(__name__)

    if os.path.exists(arg_fn):
        return arg_fn
    else:
        pplogger.error('ERROR: filename {} supplied for {} argument does not exist.'.format(arg_fn, argname))
        sys.exit('ERROR: filename {} supplied for {} argument does not exist.'.format(arg_fn, argname))


def PPFindDirectoryOrExit(arg_fn, argname):
    """
    Author: Steph Merritt

    Description: Checks to see if the directory given by arg_fn actually exists. If it doesn't,
    this fails gracefully and exits to the command line.

    Mandatory input:    string, arg_fn, string directory passed by command line argument
                        string, argname,  name/flag of the argument printed in error message

    Output:             string, arg_fn unchanged
    """
    pplogger = logging.getLogger(__name__)

    if os.path.isdir(arg_fn):
        return arg_fn
    else:
        pplogger.error('ERROR: filepath {} supplied for {} argument does not exist.'.format(arg_fn, argname))
        sys.exit('ERROR: filepath {} supplied for {} argument does not exist.'.format(arg_fn, argname))


def PPCheckFiltersForSurvey(survey_name, observing_filters):
    """
    Author: Steph Merritt

    When given a list of filters, this function checks to make sure they exist in the
    user-selected survey. Currently only has options for LSST, but can be expanded upon
    later. If the filters given in the config file do not match the survey filters,
    the function exits the program with an error.

    Parameters:
    -----------
    survey_name: string containing survey name
    observing_filters: list of strings with colour filters.

    """

    pplogger = logging.getLogger(__name__)

    if survey_name in ["LSST", "lsst"]:

        lsst_filters = ['u', 'g', 'r', 'i', 'z', 'y']
        filters_ok = all(elem in lsst_filters for elem in observing_filters)

        if not filters_ok:
            bad_list = np.setdiff1d(observing_filters, lsst_filters)
            pplogger.error('ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.'.format(bad_list, survey_name))
            pplogger.error('Accepted {} filters: {}'.format("LSST", lsst_filters))
            pplogger.error('Change observing_filters in config file or select another survey.')
            sys.exit('ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.'.format(bad_list, survey_name))


def PPConfigFileParser(configfile, survey_name):
    """
    Author: Steph Merritt

    Description: Parses the config file, error-handles, then assigns the values into a single
    dictionary, which is passed out. Mostly copied out of old version of run script.

    Chose not to use the original ConfigParser object for readability: it's a dict of
    dicts, so calling the various values can become quite unwieldy.

    This could easily be broken up even more, and probably should be.

    Mandatory input:    string, configfile, string filepath of the config file
                        string, survey_name, command-line argument containing survey name

    Output:             dictionary of variables taken from the config file

    """

    config = configparser.ConfigParser()
    config.read(configfile)

    pplogger = logging.getLogger(__name__)

    config_dict = {}

    # INPUT

    config_dict['eph_format'] = PPGetOrExit(config, 'INPUT', 'eph_format', 'ERROR: no ephemerides file format is specified.').lower()
    if config_dict['eph_format'] not in ['csv', 'whitespace', 'hdf5']:
        pplogger.error('ERROR: eph_format should be either csv, whitespace, or hdf5.')
        sys.exit('ERROR: eph_format should be either either csv, whitespace, or hdf5.')

    config_dict['aux_format'] = PPGetOrExit(config, 'INPUT', 'aux_format', 'ERROR: no auxiliary data format specified.').lower()
    if config_dict['aux_format'] not in ['comma', 'whitespace']:
        pplogger.error('ERROR: aux_format should be either comma, csv, or whitespace.')
        sys.exit('ERROR: aux_format should be either comma, csv, or whitespace.')

    config_dict['ephemerides_type'] = PPGetOrExit(config, 'INPUT', 'ephemerides_type', 'ERROR: no ephemerides type provided.').lower()
    if config_dict['ephemerides_type'] not in ['oif']:
        pplogger.error('ERROR: ephemerides_type not recognised.')
        sys.exit('ERROR: ephemerides_type not recognised.')

    config_dict['pointing_database'] = PPGetOrExit(config, 'INPUT', 'pointing_database', 'ERROR: no pointing database provided.')
    PPFindFileOrExit(config_dict['pointing_database'], 'pointing_database')

    config_dict['size_serial_chunk'] = PPGetIntOrExit(config, 'INPUT', 'size_serial_chunk', 'ERROR: size_serial_chunk not specified.')
    if config_dict['size_serial_chunk'] < 1:
        pplogger.error('ERROR: size_serial_chunk is zero or negative.')
        sys.exit('ERROR: size_serial_chunk is zero or negative.')

    # ACTIVITY

    config_dict['comet_activity'] = PPGetOrExit(config, 'ACTIVITY', 'comet_activity', 'ERROR: no comet activity specified.').lower()
    if config_dict['comet_activity'] not in ['comet', 'none']:
        pplogger.error('ERROR: comet_activity must be "comet" or "none".')
        sys.exit('ERROR: comet_activity must be "comet" or "none".')

    # FILTERS

    obsfilters = PPGetOrExit(config, 'FILTERS', 'observing_filters', 'ERROR: observing_filters config file variable not provided.')
    config_dict['observing_filters'] = [e.strip() for e in obsfilters.split(',')]

    PPCheckFiltersForSurvey(survey_name, config_dict['observing_filters'])

    # SATURATION

    bright_limits, config_dict['bright_limit_on'] = PPGetValueAndFlag(config, 'SATURATION', 'bright_limit', 'none')

    try:
        bright_list = [float(e.strip()) for e in bright_limits.split(',')]
    except ValueError:
        pplogger.error('ERROR: could not parse brightness limits. Check formatting and try again.')
        sys.exit('ERROR: could not parse brightness limits. Check formatting and try again.')

    if len(bright_list) == 1:
        config_dict['bright_limit'] = bright_list[0]
    else:
        if len(bright_list) != len(config_dict['observing_filters']):
            pplogger.error('ERROR: list of saturation limits is not the same length as list of observing filters.')
            sys.exit('ERROR: list of saturation limits is not the same length as list of observing filters.')
        config_dict['bright_limit'] = bright_list

    # PHASECURVES

    config_dict['phase_function'] = PPGetOrExit(config, 'PHASECURVES', 'phase_function', 'ERROR: phase function not defined.')

    # FOV

    config_dict['camera_model'] = PPGetOrExit(config, 'FOV', 'camera_model', 'ERROR: camera model not defined.')

    if config_dict['camera_model'] not in ['circle', 'footprint']:
        pplogger.error('ERROR: camera_model should be either "circle" or "footprint".')
        sys.exit('ERROR: camera_model should be either "circle" or "footprint".')

    elif (config_dict['camera_model'] == 'footprint'):
        config_dict['footprint_path'] = PPGetOrExit(config, 'FOV', 'footprint_path', 'ERROR: no camera footprint provided.')
        PPFindFileOrExit(config_dict['footprint_path'], 'footprint_path')

        if config.has_option('FOV', 'fill_factor'):
            pplogger.error('ERROR: fill factor supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: fill factor supplied in config file but camera model is not "circle".')
        elif config.has_option('FOV', 'circle_radius'):
            pplogger.error('ERROR: circle radius supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: circle radius supplied in config file but camera model is not "circle".')

    elif (config_dict['camera_model']) == 'circle':

        config_dict['fill_factor'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'fillfactor', 'float')
        config_dict['circle_radius'], _ = PPGetValueAndFlag(config, 'PERFORMANCE', 'circleRadius', 'float')

        if not config_dict['fill_factor'] and not config_dict['circle_radius']:
            pplogger.error('ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.')
            sys.exit('ERROR: either "fill_factor" or "circle_radius" must be specified for circular footprint.')
        elif config_dict['fill_factor']:
            if config_dict['fill_factor'] < 0.0 or config_dict['fill_factor'] > 1.0:
                pplogger.error('ERROR: fill_factor out of bounds. Must be between 0 and 1.')
                sys.exit('ERROR: fill_factor out of bounds. Must be between 0 and 1.')
        elif config_dict['circle_radius']:
            if config_dict['circle_radius'] < 0.0:
                pplogger.error('ERROR: circle_radius is negative.')
                sys.exit('ERROR: circle_radius is negative.')

    # FADINGFUNCTION

    config_dict['fading_function_on'] = PPGetBoolOrExit(config, 'FADINGFUNCTION', 'fading_function_on', 'ERROR: fading_function_on flag not present.')

    if config_dict['fading_function_on']:
        config_dict['fading_function_width'] = PPGetFloatOrExit(config, 'FADINGFUNCTION', 'fading_function_width', 'ERROR: fading function is on but no fading_function_width supplied.')
        config_dict['fading_function_peak_efficiency'] = PPGetFloatOrExit(config, 'FADINGFUNCTION', 'fading_function_peak_efficiency', 'ERROR: fading function is on but no fading_function_peak_efficiency supplied.')

        if config_dict['fading_function_width'] <= 0.0 or config_dict['fading_function_width'] > 0.5:
            pplogger.error('ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5.')
            sys.exit('ERROR: fading_function_width out of bounds. Must be greater than zero and less than 0.5.')

        if config_dict['fading_function_peak_efficiency'] < 0.0 or config_dict['fading_function_peak_efficiency'] > 1.0:
            pplogger.error('ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.')
            sys.exit('ERROR: fading_function_peak_efficiency out of bounds. Must be between 0 and 1.')

    elif config.has_option('FADINGFUNCTION', 'fading_function_width'):
        pplogger.error('ERROR: fading_function_width supplied in config file but fading_function_on is False.')
        sys.exit('ERROR: fading_function_width supplied in config file but fading_function_on is False.')
    elif config.has_option('FADINGFUNCTION', 'fading_function_peak_efficiency'):
        pplogger.error('ERROR: fading_function_peak_efficiency supplied in config file but fading_function_on is False.')
        sys.exit('ERROR: fading_function_peak_efficiency supplied in config file but fading_function_on is False.')

    # LINKINGFILTER

    config_dict['SSP_separation_threshold'], _ = PPGetValueAndFlag(config, 'LINKINGFILTER', 'SSP_separation_threshold', 'float')
    config_dict['SSP_number_observations'], _ = PPGetValueAndFlag(config, 'LINKINGFILTER', 'SSP_number_observations', 'int')
    config_dict['SSP_number_tracklets'], _ = PPGetValueAndFlag(config, 'LINKINGFILTER', 'SSP_number_tracklets', 'int')
    config_dict['SSP_track_window'], _ = PPGetValueAndFlag(config, 'LINKINGFILTER', 'SSP_track_window', 'float')
    config_dict['SSP_detection_efficiency'], _ = PPGetValueAndFlag(config, 'LINKINGFILTER', 'SSP_detection_efficiency', 'float')

    SSPvariables = [config_dict['SSP_separation_threshold'], config_dict['SSP_number_observations'], config_dict['SSP_number_tracklets'], config_dict['SSP_track_window'], config_dict['SSP_detection_efficiency']]

    # the below if-statement explicitly checks for None so a zero triggers the correct error
    if all(v is not None for v in SSPvariables):
        if config_dict['SSP_number_observations'] < 1:
            pplogger.error('ERROR: SSP_number_observations is zero or negative.')
            sys.exit('ERROR: SSP_number_observations is zero or negative.')

        if config_dict['SSP_number_tracklets'] < 1:
            pplogger.error('ERROR: SSP_number_tracklets is zero or less.')
            sys.exit('ERROR: SSP_number_tracklets is zero or less.')

        if config_dict['SSP_track_window'] <= 0.0:
            pplogger.error('ERROR: SSP_track_window is negative.')
            sys.exit('ERROR: SSP_track_window is negative.')

        if (config_dict['SSP_detection_efficiency'] > 1.0 or config_dict['SSP_detection_efficiency'] > 1.0):
            pplogger.error('ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).')
            sys.exit('ERROR: SSP_detection_efficiency out of bounds (should be between 0 and 1).')

        if config_dict['SSP_separation_threshold'] <= 0.0:
            pplogger.error('ERROR: SSP_separation_threshold is zero or negative.')
            sys.exit('ERROR: SSP_separation_threshold is zero or negative.')

        config_dict['SSP_linking_on'] = True

    elif not any(SSPvariables):
        config_dict['SSP_linking_on'] = False

    else:
        pplogger.error('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')
        sys.exit('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')

    # OUTPUT

    config_dict['output_format'] = PPGetOrExit(config, 'OUTPUT', 'output_format', 'ERROR: output format not specified.').lower()
    if config_dict['output_format'] not in ['csv', 'separatelycsv', 'sqlite3', 'hdf5', 'h5']:
        pplogger.error('ERROR: output_format should be either csv, separatelycsv, sqlite3 or hdf5.')
        sys.exit('ERROR: output_format should be either csv, separatelycsv, sqlite3 or hdf5.')

    config_dict['output_size'] = PPGetOrExit(config, 'OUTPUT', 'output_size', 'ERROR: output size not specified.').lower()
    if config_dict['output_size'] not in ['default', 'all']:
        pplogger.error('ERROR: output_size not recognised.')
        sys.exit('ERROR: output_size not recognised.')

    config_dict['position_decimals'] = PPGetIntOrExit(config, 'OUTPUT', 'position_decimals', 'ERROR: positional decimal places not specified.')
    config_dict['magnitude_decimals'] = PPGetIntOrExit(config, 'OUTPUT', 'magnitude_decimals', 'ERROR: magnitude decimal places not specified.')

    if config_dict['position_decimals'] < 0 or config_dict['magnitude_decimals'] < 0:
        pplogger.error('ERROR: decimal places config variables cannot be negative.')
        sys.exit('ERROR: decimal places config variables cannot be negative.')

    # EXPERT

    config_dict['SNR_limit'], config_dict['SNR_limit_on'] = PPGetValueAndFlag(config, 'EXPERT', 'SNR_limit', 'float')
    config_dict['mag_limit'], config_dict['mag_limit_on'] = PPGetValueAndFlag(config, 'EXPERT', 'mag_limit', 'float')

    if config_dict['SNR_limit_on'] and config_dict['SNR_limit'] < 0:
        pplogger.error('ERROR: SNR limit is negative.')
        sys.exit('ERROR: SNR limit is negative.')

    if config_dict['mag_limit_on'] and config_dict['mag_limit'] < 0:
        pplogger.error('ERROR: magnitude limit is negative.')
        sys.exit('ERROR: magnitude limit is negative.')

    if config_dict['mag_limit_on'] and config_dict['SNR_limit_on']:
        pplogger.error('ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file.')
        sys.exit('ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file.')
    try:
        config_dict['trailing_losses_on'] = config.getboolean('EXPERT', 'trailing_losses_on', fallback=True)
    except ValueError:
        pplogger.error('ERROR: could not parse value for trailing_losses_on as a boolean. Check formatting and try again.')
        sys.exit('ERROR: could not parse value for trailing_losses_on as a boolean. Check formatting and try again.')

    config_dict['pointing_sql_query'] = PPGetOrExit(config, 'EXPERT', 'pointing_sql_query', 'ERROR: no pointing database SQLite3 query provided.')

    if config.has_option('EXPERT', 'rng_seed'):
        config_dict['rng_seed'] = PPGetIntOrExit(config, 'EXPERT', 'rng_seed', 'ERROR: this error should not trigger.')
    else:
        config_dict['rng_seed'] = None

    return config_dict


def PPPrintConfigsToLog(configs, cmd_args):
    """
    Author: Steph Merritt

    Description: Prints all the values from the config file to the log.

    Mandatory input:    dict, configs, dictionary of config variables created by PPConfigFileParser

    Output: none

    """

    pplogger = logging.getLogger(__name__)

    pplogger.info('The config file used is located at ' + cmd_args['configfile'])
    pplogger.info('The physical parameters file used is located at ' + cmd_args['paramsinput'])
    pplogger.info('The orbits file used is located at ' + cmd_args['orbinfile'])
    pplogger.info('The ephemerides file used is located at ' + cmd_args['oifoutput'])
    pplogger.info('The survey selected is: ' + cmd_args['surveyname'])

    if cmd_args['makeTemporaryEphemerisDatabase']:
        pplogger.info('Creating of temporary ephemeris database at: ' + str(cmd_args['makeTemporaryEphemerisDatabase']))

    if cmd_args['readTemporaryEphemerisDatabase']:
        pplogger.info('Reading from existing temporary ephemeris database at ' + str(cmd_args['readTemporaryEphemerisDatabase']))

    if cmd_args['deleteTemporaryEphemerisDatabase']:
        pplogger.info('Temporary ephemeris database will be deleted upon code conclusion.')

    if configs['comet_activity'] == 'comet':
        pplogger.info('Cometary activity set to: ' + str(configs['cometary activity']))
    elif configs['comet_activity'] == 'none':
        pplogger.info('No cometary activity selected.')

    pplogger.info('Format of ephemerides file is: ' + configs['eph_format'])
    pplogger.info('Format of auxiliary files is: ' + configs['aux_format'])

    pplogger.info('Pointing database path is: ' + configs['pointing_database'])
    pplogger.info('Pointing database required query is: ' + configs['pointing_sql_query'])

    pplogger.info('The number of objects processed in a single chunk is: ' + str(configs['size_serial_chunk']))
    pplogger.info('The main filter in which H is defined is ' + configs['mainfilter'])
    rescs = ' '.join(str(f) for f in configs['observing_filters'])
    pplogger.info('The filters included in the post-processing results are ' + rescs)

    if configs['othercolours']:
        othcs = ' '.join(str(e) for e in configs['othercolours'])
        pplogger.info('Thus, the colour indices included in the simulation are ' + othcs)

    pplogger.info('The apparent brightness is calculated using the following phase function model: ' + configs['phase_function'])

    if configs['trailing_losses_on']:
        pplogger.info('Computation of trailing losses is switched ON.')
    else:
        pplogger.info('Computation of trailing losses is switched OFF.')

    if (configs['camera_model'] == 'footprint'):
        pplogger.info('Footprint is modelled after the actual camera footprint.')
        pplogger.info('Loading camera footprint from ' + configs['footprint_path'])
    else:
        pplogger.info('Footprint is circular.')
        if configs['fill_factor']:
            pplogger.info('The code will approximate chip gaps using filling factor: ' + str(configs['fill_factor']))
        elif configs['circleRadius']:
            pplogger.info('A circular footprint will be applied with radius: ' + str(configs['circle_radius']))

    if configs['bright_limit_on']:
        pplogger.info('The upper saturation limit(s) is/are: ' + str(configs['bright_limit']))
    else:
        pplogger.info('Saturation limit is turned OFF.')

    if configs['SNR_limit_on']:
        pplogger.info('The lower SNR limit is: ' + str(configs['SNR_limit']))
    else:
        pplogger.info('SNR limit is turned OFF.')

    if configs['mag_limit_on']:
        pplogger.info('The magnitude limit is: ' + str(configs['mag_limit']))
    else:
        pplogger.info('Magnitude limit is turned OFF.')

    if configs['fading_function_on']:
        pplogger.info('The detection efficiency fading function is ON.')
        pplogger.info('The width parameter of the fading function has been set to: ' + str(configs['fading_function_width']))
        pplogger.info('The peak efficiency of the fading function has been set to: ' + str(configs['fading_function_peak_efficiency']))
    else:
        pplogger.info('The detection efficiency fading function is OFF.')

    if configs['SSP_linking_on']:
        pplogger.info('Solar System Processing linking filter is turned ON.')
        pplogger.info('For SSP linking...')
        pplogger.info('...the fractional detection efficiency is: ' + str(configs["SSP_detection_efficiency"]))
        pplogger.info('...the minimum required number of observations in a tracklet is: ' + str(configs['SSP_number_observations']))
        pplogger.info('...the minimum required number of tracklets to form a track is: ' + str(configs['SSP_number_tracklets']))
        pplogger.info('...the maximum window of time in days of tracklets to be contained in to form a track is: ' + str(configs['SSP_track_window']))
        pplogger.info('...the minimum angular separation between observations in arcseconds is: ' + str(configs['SSP_separation_threshold']))
    else:
        pplogger.info('Solar System Processing linking filter is turned OFF.')

    pplogger.info('Output files will be saved in path: ' + cmd_args['outpath'] + ' with filestem ' + cmd_args['outfilestem'])
    pplogger.info('Output files will be saved as format: ' + configs['output_format'])
    pplogger.info('In the output, positions will be rounded to ' + str(configs['position_decimals']) + ' decimal places.')
    pplogger.info('In the output, magnitudes will be rounded to ' + str(configs['magnitude_decimals']) + ' decimal places.')
    pplogger.info('The output size is set to: ' + configs['output_size'])
