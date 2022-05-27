#!/usr/bin/python
# Utility functions used in the running of surveySimPP.py.

import logging
import os
import sys
import numpy as np
import configparser
from datetime import datetime
from .PPReadOrbitFile import PPReadOrbitFile
from .PPCheckOrbitAndPhysicalParametersMatching import PPCheckOrbitAndPhysicalParametersMatching
from .PPReadCometaryInput import PPReadCometaryInput
from .PPReadIntermDatabase import PPReadIntermDatabase
from .PPReadEphemerides import PPReadEphemerides
from .PPJoinPhysicalParametersPointing import PPJoinPhysicalParametersPointing
from .PPJoinOrbitalData import PPJoinOrbitalData
from .PPMatchPointingToObservations import PPMatchPointingToObservations
from .PPReadPhysicalParameters import PPReadPhysicalParameters


def PPGetLogger(
        log_location,
        log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s ',
        log_name='',
        log_file_info='postprocessing.log',
        log_file_error='postprocessing.err'):

    # log_format     = '',
    log = logging.getLogger(log_name)
    log_formatter = logging.Formatter(log_format)

    # comment this to suppress console output
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(log_formatter)
    # log.addHandler(stream_handler)

    dstr = datetime.now().strftime('%Y%m%d%H%M')
    cpid = os.getpid()

    log_file_info = str(log_location + dstr + '-' + str(cpid) + '-' + log_file_info)
    log_file_error = str(log_location + dstr + '-' + str(cpid) + '-' + log_file_error)

    file_handler_info = logging.FileHandler(log_file_info, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(log_file_error, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log


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
        logging.info(none_message)
    else:
        flag = True

    return value, flag


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

    config_dict['pointingFormat'] = PPGetOrExit(config, 'INPUTFILES', 'pointingFormat', 'ERROR: no pointing simulation format is specified.')
    config_dict['filesep'] = PPGetOrExit(config, 'INPUTFILES', 'auxFormat', 'ERROR: no auxiliary data format specified.')
    config_dict['ephemerides_type'] = PPGetOrExit(config, 'INPUTFILES', 'ephemerides_type', 'ERROR: no ephemerides type provided.')
    config_dict['pointingdatabase'] = PPGetOrExit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    PPFindFileOrExit(config_dict['pointingdatabase'], 'pointingdatabase')
    config_dict['ppdbquery'] = PPGetOrExit(config, 'INPUTFILES', 'ppsqldbquery', 'ERROR: no pointing database SQLite3 query provided.')

    # object type checking

    config_dict['objecttype'] = PPGetOrExit(config, 'OBJECTS', 'objecttype', 'ERROR: no object type provided.')
    if config_dict['objecttype'] not in ['asteroid', 'comet']:
        pplogger.error('ERROR: objecttype is neither an asteroid or a comet.')
        sys.exit('ERROR: objecttype is neither an asteroid or a comet.')

    # filters

    config_dict['othercolours'] = [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    config_dict['observing_filters'] = [e.strip() for e in config.get('FILTERS', 'observing_filters').split(',')]
    if (len(config_dict['othercolours']) != len(config_dict['observing_filters']) - 1):
        pplogger.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(observing_filters) - 1')
        sys.exit('ERROR: mismatch in input config colours and filters: len(othercolours) != len(observing_filters) - 1')

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
        sys.exit('ERROR: SNR limit and magnitude limit are mutually exclusive. Please delete one for both from config file.')

    # fading function

    config_dict['fadingFunctionOn'] = PPGetBoolOrExit(config, 'FILTERINGPARAMETERS', 'fadingFunctionOn', 'ERROR: fadingFunctionOn flag not present.')

    # SSP linking filter

    config_dict['inSepThreshold'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'inSepThreshold', 'float', 'Separation threshold not supplied for SSP filtering.')
    config_dict['minTracklet'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'minTracklet', 'int', 'Minimum tracklet length not supplied for SSP filtering.')
    config_dict['noTracklets'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'noTracklets', 'int', 'Number of tracklets not supplied for SSP filtering.')
    config_dict['trackletInterval'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'trackletInterval', 'float', 'Tracklet interval not supplied for SSP filtering.')
    config_dict['SSPDetectionEfficiency'], _ = PPGetValueAndFlag(config, 'FILTERINGPARAMETERS', 'SSPDetectionEfficiency', 'float', 'Detection efficiency not supplied for SSP filtering.')

    if (config_dict['inSepThreshold'] is not None
            and config_dict['minTracklet'] is not None
            and config_dict['noTracklets'] is not None
            and config_dict['trackletInterval'] is not None
            and config_dict['SSPDetectionEfficiency'] is not None):

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

        config_dict['SSPLinkingOn'] = True

    elif (config_dict['inSepThreshold'] is None
            and config_dict['minTracklet'] is None
            and config_dict['noTracklets'] is None
            and config_dict['trackletInterval'] is None
            and config_dict['SSPDetectionEfficiency'] is None):

        config_dict['SSPLinkingOn'] = False

    else:
        pplogger.error('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')
        sys.exit('ERROR: only some SSP linking variables supplied. Supply all five required variables for SSP linking filter, or none to turn filter off.')

    # output format

    config_dict['outputformat'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.')
    if config_dict['outputformat'] not in ['csv', 'separatelyCSV', 'separatelyCsv', 'separatelycsv', 'sqlite3', 'hdf5', 'HDF5', 'h5']:
        pplogger.error('ERROR: output format should be either csv, separatelyCSV, sqlite3 or hdf5.')
        sys.exit('ERROR: output format should be either csv, separatelyCSV, sqlite3 or hdf5.')

    # size of chunk

    config_dict['sizeSerialChunk'] = PPGetIntOrExit(config, 'GENERAL', 'sizeSerialChunk', 'ERROR: sizeSerialChunk not specified.')
    if config_dict['sizeSerialChunk'] < 1:
        pplogger.error('ERROR: sizeSerialChunk is zero or negative.')
        sys.exit('ERROR: sizeSerialChunk is zero or negative.')

    return config_dict


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


def PPPrintConfigsToLog(configs):
    """
    Author: Steph Merritt

    Description: Prints all the values from the config file to the log.

    Mandatory input:    dict, configs, dictionary of config variables created by PPConfigFileParser

    Output: none

    """

    pplogger = logging.getLogger(__name__)

    pplogger.info('Object type is ' + str(configs['objecttype']))

    pplogger.info('Pointing simulation result format is: ' + configs['pointingFormat'])
    pplogger.info('Pointing simulation result path is: ' + configs['pointingdatabase'])
    pplogger.info('Pointing simulation result required query is: ' + configs['ppdbquery'])

    pplogger.info('The main filter in which brightness is defined is ' + configs['observing_filters'][0])
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


def PPCMDLineParser(parser):
    """
    Author: Steph Merritt

    Description: Parses the command line arguments, makes sure the filenames given actually exist,
    then stores them in a single dict.

    Will only look for the comet parameters file if it's actually given at the command line.

    Mandatory input:    ArgumentParser object, parser, of command line arguments

    output:             dictionary of variables taken from command line arguments

    """

    args = parser.parse_args()

    cmd_args_dict = {}

    cmd_args_dict['paramsinput'] = PPFindFileOrExit(args.l, '-l, --params')
    cmd_args_dict['orbinfile'] = PPFindFileOrExit(args.o, '-o, --orbit')
    cmd_args_dict['oifoutput'] = PPFindFileOrExit(args.p, '-p, --pointing')
    cmd_args_dict['configfile'] = PPFindFileOrExit(args.c, '-c, --config')
    cmd_args_dict['outpath'] = PPFindFileOrExit(args.u, '-u, --outfile')

    if args.m:
        cmd_args_dict['cometinput'] = PPFindFileOrExit(args.m, '-m, --comet')

    cmd_args_dict['makeIntermediatePointingDatabase'] = bool(args.d)
    cmd_args_dict['surveyname'] = args.s
    cmd_args_dict['outfilestem'] = args.t

    return cmd_args_dict


def PPReadAllInput(cmd_args, configs, filterpointing, startChunk, incrStep):
    """
    Author: Steph Merritt

    Description: Reads in the simulation data and the orbit and physical parameter files, and then
    joins them with the pointing database to create a single Pandas dataframe of simulation
    data with all necessary orbit, physical parameter and pointing information.

    Mandatory input:	dict, cmd_args, dictionary of command line variables created by PPCMDLineParser
                        dict, configs, dictionary of config variables created by PPConfigFileParser
                        pandas DataFrame, filterpointing, pointing database
                        int, startChunk, start of chunk
                        int, incrStep, size of chunk

    Output:             pandas Dataframe, observations, dataframe of simulation data with all
                        necessary orbit, physical parameter and pointing information.
    """

    pplogger = logging.getLogger(__name__)

    pplogger.info('Reading input orbit file: ' + cmd_args['orbinfile'])
    padaor = PPReadOrbitFile(cmd_args['orbinfile'], startChunk, incrStep, configs['filesep'])

    pplogger.info('Reading input physical parameters: ' + cmd_args['paramsinput'])
    padacl = PPReadPhysicalParameters(cmd_args['paramsinput'], startChunk, incrStep, configs['filesep'])
    if (configs['objecttype'] == 'comet'):
        pplogger.info('Reading cometary parameters: ' + cmd_args['cometinput'])
        padaco = PPReadCometaryInput(cmd_args['cometinput'], startChunk, incrStep, configs['filesep'])

    objid_list = padacl['ObjID'].unique().tolist()

    if cmd_args['makeIntermediatePointingDatabase']:
        # read from intermediate database
        padafr = PPReadIntermDatabase('./data/interm.db', objid_list)
    else:
        try:
            pplogger.info('Reading input pointing history: ' + cmd_args['oifoutput'])
            padafr = PPReadEphemerides(cmd_args['oifoutput'], configs['ephemerides_type'], configs["pointingFormat"])

            padafr = padafr[padafr['ObjID'].isin(objid_list)]

        except MemoryError:
            pplogger.error('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
            sys.exit('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')

    pplogger.info('Checking if orbit, brightness, physical parameters and pointing simulation input files match...')
    PPCheckOrbitAndPhysicalParametersMatching(padaor, padacl, padafr)

    if (configs['objecttype'] == 'comet'):
        PPCheckOrbitAndPhysicalParametersMatching(padaor, padaco, padafr)

    pplogger.info('Joining physical parameters and orbital data with simulation data...')
    observations = PPJoinPhysicalParametersPointing(padafr, padacl)
    observations = PPJoinOrbitalData(observations, padaor)
    if (configs['objecttype'] == 'comet'):
        pplogger.info('Joining cometary data...')
        observations = PPJoinPhysicalParametersPointing(observations, padaco)

    pplogger.info('Joining info from pointing database with simulation data and dropping observations in non-requested filters...')
    observations = PPMatchPointingToObservations(observations, filterpointing)

    return observations
