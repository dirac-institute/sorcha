def PPGetOrExit(config, section, key, message):
    # from Shantanu Naidu, objectInField
    try:
        return config[section][key]
    except KeyError:
        logging.error(message)
        sys.exit(message)
        

def PPGetOrPass(config, section, key, message):
    # as PPGetOrExit, except if the config variable doesn't exist, returns 0
    # essentially turns off filters if the variable isn't given
    try:
        return config[section][key]
    except KeyError:
        logging.info(message)
        return 0
                            
def PPToBool(value):
    valid = {'true': True, 't': True, '1': True, 'True': True,
             'false': False, 'f': False, '0': False, 'False': False
             }   

    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise ValueError('invalid literal for boolean. Not a string.')

    lower_value = value.lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)
        
def PPGetObjectType(config):

    pplogger = logging.getLogger(__name__)

    object_type = PPGetOrExit(config, 'OBJECTS', 'objecttype', 'ERROR: no object type provided.')    
    
    if object_type not in ['asteroid', 'comet']:
        pplogger.error('ERROR: objecttype is neither an asteroid or a comet.') 
        sys.exit('ERROR: objecttype is neither an asteroid or a comet.')

    return object_type
    
def PPGetColourFilters(config):

    pplogger = logging.getLogger(__name__)

    other_colours = [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    observing_filters = [e.strip() for e in config.get('FILTERS', 'observing_filters').split(',')]    
    
    if (len(other_colours) != len(observing_filters)-1):
        pplogger.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(observing_filters) - 1')
        sys.exit('ERROR: mismatch in input config colours and filters: len(othercolours) != len(observing_filters) - 1')
        
    return other_colours, observing_filters

def PPGetCameraFOV(configs):

    pplogger = logging.getLogger(__name__)

    camera_model = PPGetOrExit(config, 'PERFORMANCE', 'cameraModel', 'ERROR: camera model not defined.')	

    if camera_model not in ['circle', 'footprint']:
        pplogger.error('ERROR: cameraModel should be either circle or footprint.')
        sys.exit('ERROR: cameraModel should be either circle or footprint.')        

    elif camera_model == 'footprint':
        footprint_path = PPGetOrExit(config, 'INPUTFILES', 'footprintPath', 'ERROR: no camera footprint provided.')
        PPFindFileOrExit(footprint_path, 'footprintPath')

        try:
            check_for_fillfactor = config['FILTERINGPARAMETERS']['fillfactor']
            pplogger.error('ERROR: fill factor supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: fill factor supplied in config file but camera model is not "circle".')
        except KeyError:
            fill_factor = 1.0

    elif camera_model == 'circle':
        fill_factor = float(PPGetOrExit(config, 'FILTERINGPARAMETERS', 'fillfactor', 'ERROR: no fill factor specified for circular footprint.'))

    return camera_model, footprint_path, fill_factor


def PPConfigFileParser(configfile, survey_name):
    """
    Author: Steph Merritt

    Description: Parses the config file, error-handles, then assigns the values into a single 
    dictionary, which is passed out. Mostly copied out of old version of run script.

    Chose not to use the original ConfigParser object for readability: it's a dict of 
    dicts, so calling the various values can become quite unwieldy.

    This could easily be broken up even more, and probably should be.	

    Mandatory input:	string, configfile, string filepath of the config file
                        string, survey_name, command-line argument containing survey name

    Output: 			dictionary of variables taken from the config file

    """
	
    config = configparser.ConfigParser()
    config.read(configfile)

    pplogger = logging.getLogger(__name__)

    config_dict = {}
    config_dict['pointingFormat'] = PPGetOrExit(config, 'INPUTFILES', 'pointingFormat', 'ERROR: no pointing simulation format is specified.')
    config_dict['filesep'] = PPGetOrExit(config, 'INPUTFILES', 'auxFormat', 'ERROR: no auxilliary data format specified.')  

    config_dict['objecttype'] = PPGetObjectType(config)

    config_dict['ephemerides_type'] = PPGetOrExit(config, 'INPUTFILES', 'ephemerides_type', 'ERROR: no ephemerides type provided.')
    config_dict['pointingdatabase'] = PPGetOrExit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    PPFindFileOrExit(config_dict['pointingdatabase'], 'pointingdatabase')
    config_dict['ppdbquery'] = PPGetOrExit(config, 'INPUTFILES', 'ppsqldbquery', 'ERROR: no pointing database SQLite3 query provided.')

    config_dict['othercolours'], config_dict['observing_filters'] = PPGetColourFilters(config)
	
    PPCheckFiltersForSurvey(survey_name, config_dict['observing_filters'])
	 
    config_dict['phasefunction'] = PPGetOrExit(config,'PHASE', 'phasefunction', 'ERROR: phase function not defined.')
    config_dict['trailingLossesOn'] = PPToBool(config['PERFORMANCE']['trailingLossesOn'])

    config_dict['cameraModel'] = PPGetOrExit(config, 'PERFORMANCE', 'cameraModel', 'ERROR: camera model not defined.')	
	
    if config_dict['cameraModel'] not in ['circle', 'footprint']:
        pplogger.error('ERROR: cameraModel should be either circle or footprint.')
        sys.exit('ERROR: cameraModel should be either circle or footprint.')        
	
    elif (config_dict['cameraModel'] == 'footprint'):
        config_dict['footprintPath'] = PPGetOrExit(config, 'INPUTFILES', 'footprintPath', 'ERROR: no camera footprint provided.')
        PPFindFileOrExit(config_dict['footprintPath'], 'footprintPath')
		
        try:
            check_for_fillfactor = config['FILTERINGPARAMETERS']['fillfactor']
            pplogger.error('ERROR: fill factor supplied in config file but camera model is not "circle".')
            sys.exit('ERROR: fill factor supplied in config file but camera model is not "circle".')
        except KeyError:
            config_dict['fillfactor'] = 1.0
		
    elif (config_dict['cameraModel']) == 'circle':
        config_dict['fillfactor'] = float(PPGetOrExit(config, 'FILTERINGPARAMETERS', 'fillfactor', 'ERROR: no fill factor specified for circular footprint.'))

    config_dict['brightLimit'] = float(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'brightLimit', 'Brightness limit not supplied. No brightness filter will be applied.'))
    config_dict['SNRLimit'] = float(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'SNRLimit', 'SNR limit not supplied. SNR limit defaulting to 2 sigma.'))	
    config_dict['magLimit'] = float(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'magLimit', 'Magnitude limit not supplied. No magnitude cut will be applied.'))
    
    if not config_dict['SNRLimit']: config_dict['SNRLimit'] = 2.0	
    
    if config_dict['brightLimit'] and (isinstance(config_dict['brightLimit'],(float,int))==False):
        pplogger.error('ERROR: brightness limit is not an int or float.')
        sys.exit('ERROR: brightness limit is not an int or float.')
    
    if (isinstance(config_dict['SNRLimit'],(float,int))==False or config_dict['SNRLimit'] < 0):
        pplogger.error('ERROR: SNR limit is negative, or not an int or float.')
        sys.exit('ERROR: SNR limit is negative, or not an int or float.')
    
    if config_dict['magLimit'] and (isinstance(config_dict['magLimit'],(float,int))==False or config_dict['magLimit'] < 0):
        pplogger.error('ERROR: magnitude limit is negative, or not an int or float.')
        sys.exit('ERROR: magnitude limit is negative, or not an int or float.')
    
    config_dict['inSepThreshold'] = float(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'inSepThreshold', 'Separation threshold not supplied for SSP filtering.'))
    config_dict['minTracklet'] = int(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'minTracklet', 'Minimum tracklet length not supplied for SSP filtering.'))
    config_dict['noTracklets'] = int(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'noTracklets', 'Number of tracklets not supplied for SSP filtering.'))
    config_dict['trackletInterval'] = float(PPGetOrPass(config,'FILTERINGPARAMETERS','trackletInterval', 'Tracklet interval not supplied for SSP filtering.'))
    config_dict['SSPDetectionEfficiency'] = float(PPGetOrPass(config, 'FILTERINGPARAMETERS', 'SSPDetectionEfficiency', 'Detection efficiency not supplied for SSP filtering.'))
	
    if config_dict['inSepThreshold'] and config_dict['minTracklet'] and config_dict['noTracklets'] and config_dict['trackletInterval'] and config_dict['SSPDetectionEfficiency']:
        
        # only error handles these values if they are supplied
        if (config_dict['minTracklet'] < 1 or isinstance(config_dict['minTracklet'],int)==False):
            pplogger.error('ERROR: minimum length of tracklet is zero or negative, or not an integer.')
            sys.exit('ERROR: minimum length of tracklet is zero or negative, or not an integer.')
        
        if (config_dict['noTracklets']  < 1 or isinstance(config_dict['noTracklets'], int)== False):
            pplogger.error('ERROR: number of tracklets is zero or less, or not an integer.')
            sys.exit('ERROR: number of tracklets is zero or less, or not an integer.')    
        
        if (config_dict['trackletInterval'] <= 0.0 or isinstance(config_dict['trackletInterval'],(float,int))==False):
            pplogger.error('ERROR: tracklet appearance interval is negative, or not a number.')
            sys.exit('ERROR: tracklet appearance interval is negative, or not a number.')
        
        if (config_dict['SSPDetectionEfficiency'] > 1.0 or config_dict['SSPDetectionEfficiency'] > 1.0 or isinstance(config_dict['SSPDetectionEfficiency'],(float,int))==False):
            pplogger.error('ERROR: SSP detection efficiency out of bounds (should be between 0 and 1.), or not a number.')
            sys.exit('ERROR: SSP detection efficiency out of bounds (should be between 0 and 1.), or not a number.')
              
        config_dict['SSPFiltering'] = True  
    
    elif not config_dict['inSepThreshold'] and not config_dict['minTracklet'] and not config_dict['noTracklets'] and not config_dict['trackletInterval'] and not config_dict['SSPDetectionEfficiency']:
        config_dict['SSPFiltering'] = False
    else:
        pplogger.error('ERROR: only some SSP filtering variables supplied. Supply all five required variables for SSP filter, or none to turn filter off.')
        sys.exit('ERROR: only some SSP filtering variables supplied. Supply all five required variables for SSP filter, or none to turn filter off.')
			
    config_dict['outpath'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outpath', 'ERROR: out path not specified.')   
    config_dict['outfilestem'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outfilestem', 'ERROR: name of output file stem not specified.')
	
    PPFindFileOrExit(config_dict['outpath'], 'outpath')

    config_dict['outputformat'] = PPGetOrExit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.')   
    if config_dict['outputformat'] not in ['csv', 'separatelyCSV', 'separatelyCsv', 'separatelycsv', 'sqlite3', 'hdf5', 'HDF5', 'h5']:
        pplogger.error('ERROR: output format should be either csv, separatelyCSV, sqlite3 or hdf5.')
        sys.exit('ERROR: output format should be either csv, separatelyCSV, sqlite3 or hdf5.')

    config_dict['sizeSerialChunk'] = int(config['GENERAL']['sizeSerialChunk'])

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
            bad_list = np.setdiff1d(observing_filters,lsst_filters)
            pplogger.error('ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.'.format(bad_list, survey_name))
            pplogger.error('Accepted {} filters: {}'.format("LSST", lsst_filters))
            pplogger.error('Change observing_filters in config file or select another survey.')
            sys.exit('ERROR: Filter(s) {} given in config file are not recognised filters for {} survey.'.format(bad_list, survey_name))