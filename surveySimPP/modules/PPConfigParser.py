#!/usr/bin/python
# Parsing and error handling of the config file.
# Should probably be overhauled. OOP would help here.

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


def PPGetValueAndFlag(config, section, key, type_wanted, none_message):
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

    # formatting and input

    config_dict['ephFormat'] = PPGetOrExit(config, 'INPUTFILES', 'ephFormat', 'ERROR: no ephemerides file format is specified.').lower()
    if config_dict['ephFormat'] not in ['csv', 'whitespace', 'hdf5']:
        pplogger.error('ERROR: ephFormat should be either csv, whitespace, or hdf5.')
        sys.exit('ERROR: ephFormat should be either either csv, whitespace, or hdf5.')

    config_dict['filesep'] = PPGetOrExit(config, 'INPUTFILES', 'auxFormat', 'ERROR: no auxiliary data format specified.').lower()
    if config_dict['filesep'] not in ['comma', 'whitespace']:
        pplogger.error('ERROR: auxFormat should be either comma, csv, or whitespace.')
        sys.exit('ERROR: auxFormat should be either comma, csv, or whitespace.')

    config_dict['ephemerides_type'] = PPGetOrExit(config, 'INPUTFILES', 'ephemerides_type', 'ERROR: no ephemerides type provided.')
    config_dict['pointingdatabase'] = PPGetOrExit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    PPFindFileOrExit(config_dict['pointingdatabase'], 'pointingdatabase')

    config_dict['ppdbquery'] = PPGetOrExit(config, 'INPUTFILES', 'ppsqldbquery', 'ERROR: no pointing database SQLite3 query provided.')

    # cometary activity checking

    config_dict['cometactivity'] = PPGetOrExit(config, 'OBJECTS', 'cometactivity', 'ERROR: no comet activity specified.').lower()
    if config_dict['cometactivity'] not in ['comet', 'none']:
        pplogger.error('ERROR: cometactivity must be "comet" or "none".')
        sys.exit('ERROR: cometactivity must be "comet" or "none".')

    # filters

    obsfilters = PPGetOrExit(config, 'FILTERS', 'observing_filters', 'ERROR: observing_filters config file variable not provided.')
    config_dict['observing_filters'] = [e.strip() for e in obsfilters.split(',')]

    config_dict['mainfilter'] = config_dict['observing_filters'][0]
    config_dict['othercolours'] = [x + "-" + config_dict['mainfilter'] for x in config_dict['observing_filters'][1:]]

    PPCheckFiltersForSurvey(survey_name, config_dict['observing_filters'])

    # phase function, trailing losses

    config_dict['phasefunction'] = PPGetOrExit(config, 'PHASE', 'phasefunction', 'ERROR: phase function not defined.')
    config_dict['trailingLossesOn'] = PPGetBoolOrExit(config, 'PERFORMANCE', 'trailingLossesOn', 'ERROR: trailingLossesOn flag not present.')

    # camera model

    config_dict['cameraModel'] = PPGetOrExit(config, 'PERFORMANCE', 'cameraModel', 'ERROR: camera model not defined.')

    if config_dict['cameraModel'] not in ['circle', 'footprint']:
        pplogger.error('ERROR: cameraModel should be either "circle" or "footprint".')
        sys.exit('ERROR: cameraModel should be either "circle" or "footprint".')

    elif (config_dict['cameraModel'] == 'footprint'):
        config_dict['footprintPath'] = PPGetOrExit(config, 'INPUTFILES', 'footprintPath', 'ERROR: no camera footprint provided.')
        PPFindFileOrExit(config_dict['footprintPath'], 'footprintPath')

        if config.has_option('FILTERINGPARAMETERS', 'fillfactor'):
            pplogger.error('ERROR: fill factor supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: fill factor supplied in config file but camera model is not "circle".')
        else:
            config_dict['fillfactor'] = 1.0

    elif (config_dict['cameraModel']) == 'circle':

        config_dict['fillfactor'] = PPGetFloatOrExit(config, 'FILTERINGPARAMETERS', 'fillfactor', 'ERROR: fillfactor must be specified for circle camera footprint.')

        if config_dict['fillfactor'] < 0.0 or config_dict['fillfactor'] > 1.0:
            pplogger.error('ERROR: fillfactor out of bounds. Must be between 0 and 1.')
            sys.exit('ERROR: fillfactor out of bounds. Must be between 0 and 1.')

    # SNR, magnitude, bright limit filters

    config_dict['brightLimit'], config_dict['brightLimitOn'] = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'brightLimit', 'float', 'Brightness limit not supplied. No brightness filter will be applied.')
    config_dict['SNRLimit'], config_dict['SNRLimitOn'] = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'SNRLimit', 'float', 'SNR limit not supplied. SNR limit defaulting to 2 sigma.')
    config_dict['magLimit'], config_dict['magLimitOn'] = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'magLimit', 'float', 'Magnitude limit not supplied. No magnitude cut will be applied.')

    if config_dict['SNRLimitOn'] and config_dict['SNRLimit'] < 0:
        pplogger.error('ERROR: SNR limit is negative.')
        sys.exit('ERROR: SNR limit is negative.')

    if config_dict['magLimitOn'] and config_dict['magLimit'] < 0:
        pplogger.error('ERROR: magnitude limit is negative.')
        sys.exit('ERROR: magnitude limit is negative.')

    if config_dict['magLimitOn'] and config_dict['SNRLimitOn']:
        pplogger.error('ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file.')
        sys.exit('ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one or both from config file.')

    # fading function

    config_dict['fadingFunctionOn'] = PPGetBoolOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionOn', 'ERROR: fadingFunctionOn flag not present.')
    
    if config_dict['fadingFunctionOn']:
        config_dict['fadingFunctionWidth'] = PPGetFloatOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionWidth', 'ERROR: fading function is on but no fadingFunctionWidth supplied.')
 
        if config_dict['fadingFunctionWidth'] <= 0.0 or config_dict['fadingFunctionWidth'] > 0.5:
            pplogger.error('ERROR: fadingFunctionWidth out of bounds. Must be greater than zero and less than 0.5.')
            sys.exit('ERROR: fadingFunctionWidth out of bounds. Must be greater than zero and less than 0.5.')

    elif config.has_option('FILTERINGPARAMETERS', 'fadingFunctionWidth'):
        pplogger.error('ERROR: fadingFunctionWidth supplied in config file but FadingFunctionOn is False.')
        sys.exit('ERROR: fadingFunctionWidth supplied in config file but FadingFunctionOn is False.')

    # SSP linking filter

    config_dict['inSepThreshold'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'inSepThreshold', 'float', 'Separation threshold not supplied for SSP filtering.')
    config_dict['minTracklet'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'minTracklet', 'int', 'Minimum tracklet length not supplied for SSP filtering.')
    config_dict['noTracklets'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'noTracklets', 'int', 'Number of tracklets not supplied for SSP filtering.')
    config_dict['trackletInterval'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'trackletInterval', 'float', 'Tracklet interval not supplied for SSP filtering.')
    config_dict['SSPDetectionEfficiency'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'SSPDetectionEfficiency', 'float', 'Detection efficiency not supplied for SSP filtering.')

    SSPvariables = [config_dict['inSepThreshold'], config_dict['minTracklet'], config_dict['noTracklets'], config_dict['trackletInterval'], config_dict['SSPDetectionEfficiency']]

    # the below if-statement explicitly checks for None so a zero triggers the correct error
    if all(v is not None for v in SSPvariables):
        # only error handles these values if they are supplied
        if config_dict['minTracklet'] < 1:
            pplogger.error('ERROR: minTracklet is zero or negative.')
            sys.exit('ERROR: minTracklet is zero or negative.')

        if config_dict['noTracklets'] < 1:
            pplogger.error('ERROR: noTracklets is zero or less.')
            sys.exit('ERROR: noTracklets is zero or less.')

        if config_dict['trackletInterval'] <= 0.0:
            pplogger.error('ERROR: trackletInterval is negative.')
            sys.exit('ERROR: trackletInterval is negative.')

        if (config_dict['SSPDetectionEfficiency'] > 1.0 or config_dict['SSPDetectionEfficiency'] > 1.0):
            pplogger.error('ERROR: SSPDetectionEfficiency out of bounds (should be between 0 and 1).')
            sys.exit('ERROR: SSPDetectionEfficiency out of bounds (should be between 0 and 1).')

        if config_dict['inSepThreshold'] <= 0.0:
            pplogger.error('ERROR: inSepThreshold is zero or negative.')
            sys.exit('ERROR: inSepThreshold is zero or negative.')

        config_dict['SSPLinkingOn'] = True

    elif not any(SSPvariables):

        config_dict['SSPLinkingOn'] = False

    else:
        pplogger.error('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')
        sys.exit('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')

    # output format and size

    config_dict['outputformat'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.').lower()
    if config_dict['outputformat'] not in ['csv', 'separatelycsv', 'sqlite3', 'hdf5', 'h5']:
        pplogger.error('ERROR: outputformat should be either csv, separatelyCSV, sqlite3 or hdf5.')
        sys.exit('ERROR: outputformat should be either csv, separatelyCSV, sqlite3 or hdf5.')

    config_dict['outputsize'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outputsize', 'ERROR: output size not specified.').lower()
    if config_dict['outputsize'] not in ['default']:
        pplogger.error('ERROR: outputsize should be "default".')
        sys.exit('ERROR: outputsize should be "default".')

    # size of chunk

    config_dict['sizeSerialChunk'] = PPGetIntOrExit(config, 'GENERAL', 'sizeSerialChunk', 'ERROR: sizeSerialChunk not specified.')
    if config_dict['sizeSerialChunk'] < 1:
        pplogger.error('ERROR: sizeSerialChunk is zero or negative.')
        sys.exit('ERROR: sizeSerialChunk is zero or negative.')

    if config.has_option('GENERAL', 'rng_seed'):
        config_dict['rng_seed'] = PPGetIntOrExit(config, 'GENERAL', 'rng_seed', 'ERROR: this error should not trigger.')
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
    pplogger.info('Creation of interim database is: ' + str(cmd_args['makeIntermediatePointingDatabase']))

    if configs['cometactivity'] == 'comet':
        pplogger.info('Cometary activity set to: ' + str(configs['cometary activity']))
    elif configs['cometactivity'] == 'none':
        pplogger.info('No cometary activity selected.')

    pplogger.info('Format of ephemerides file is: ' + configs['ephFormat'])
    pplogger.info('Format of auxiliary files is: ' + configs['filesep'])

    pplogger.info('Pointing simulation result path is: ' + configs['pointingdatabase'])
    pplogger.info('Pointing simulation result required query is: ' + configs['ppdbquery'])

    pplogger.info('The main filter in which brightness is defined is ' + configs['mainfilter'])
    othcs = ' '.join(str(e) for e in configs['othercolours'])
    pplogger.info('The colour indices included in the simulation are ' + othcs)
    rescs = ' '.join(str(f) for f in configs['observing_filters'])
    pplogger.info('Hence, the filters included in the post-processing results are ' + rescs)

    pplogger.info('The apparent brightness is calculated using the following phase function model: ' + configs['phasefunction'])

    if configs['trailingLossesOn']:
        pplogger.info('Computation of trailing losses is switched ON.')
    else:
        pplogger.info('Computation of trailing losses is switched OFF.')

    if (configs['cameraModel'] == 'footprint'):
        pplogger.info('Footprint is modelled after the actual camera footprint.')
        pplogger.info('Loading camera footprint from ' + configs['footprintPath'])
        pplogger.info('The filling factor has been set to ' + str(configs["fillfactor"]))
    else:
        pplogger.info('Footprint is circular')
        pplogger.info('The filling factor for the circular footprint is ' + str(configs["fillfactor"]))

    if configs['brightLimitOn']:
        pplogger.info('The upper brightness limit is ' + str(configs['brightLimit']))
    else:
        pplogger.info('Brightness limit is turned OFF.')

    if configs['SNRLimitOn']:
        pplogger.info('The lower SNR limit is ' + str(configs['SNRLimit']))
    else:
        pplogger.info('SNR limit is turned OFF.')

    if configs['magLimitOn']:
        pplogger.info('The magnitude limit is ' + str(configs['magLimit']))
    else:
        pplogger.info('Magnitude limit is turned OFF.')

    if configs['fadingFunctionOn']:
        pplogger.info('The detection efficiency fading function is ON.')
        pplogger.info('The width parameter of the fading function has been set to: ' + str(configs['fadingFunctionWidth']))
    else:
        pplogger.info('The detection efficiency fading function is OFF.')

    if configs['SSPLinkingOn']:
        pplogger.info('Solar System Processing linking filter is turned ON.')
        pplogger.info('For SSP linking...')
        pplogger.info('...the fractional detection efficiency is ' + str(configs["SSPDetectionEfficiency"]))
        pplogger.info('...the minimum required number of observations in a tracklet is ' + str(configs['minTracklet']))
        pplogger.info('...the minimum required number of tracklets is ' + str(configs['noTracklets']))
        pplogger.info('...the maximum interval of time in days of tracklets to be contained in is ' + str(configs['trackletInterval']))
        pplogger.info('...the minimum angular separation between observations in arcseconds is ' + str(configs['inSepThreshold']))
    else:
        pplogger.info('Solar System Processing linking filter is turned OFF.')

    pplogger.info('Output files will be saved in path: ' + cmd_args['outpath'] + ' with filestem ' + cmd_args['outfilestem'])
