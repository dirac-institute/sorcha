#!/usr/bin/python

import os,sys
import pandas as pd
import numpy as np
import logging
import argparse
import configparser
from lsstcomet import *
from modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPReadColours
from modules import PPhookBrightnessWithColour, PPJoinColourPointing, PPMatchPointing 
from modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency
#from modules import PPOutWriteCSV, PPOutWriteSqlite3, PPOutWriteHDF5
from modules import PPOut
from modules import PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from modules import PPReadOif, PPReadBrightness
from modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from modules import PPDropObservations, PPBrightLimit
from modules import PPMakeIntermediatePointingDatabase, PPReadIntermDatabase
from modules import PPReadCometaryInput, PPJoinCometaryWithOrbits, PPCalculateSimpleCometaryMagnitude
from modules import PPCalculateApparentMagnitude
from modules import PPFootprintFilter, PPAddUncertainties, PPRandomizeMeasurements, PPVignetting
from modules.PPDetectionProbability import calcDetectionProbability, PPDetectionProbability


def get_logger(    
        LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s ',
        LOG_NAME       = '',
        LOG_FILE_INFO  = 'postprocessing.log',
        LOG_FILE_ERROR = 'postprocessing.err'):


    #LOG_FORMAT     = '',
    log           = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # comment this to suppress console output
    #stream_handler = logging.StreamHandler()
    #stream_handler.setFormatter(log_formatter)
    #log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='w')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='w')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.INFO)

    return log


def get_or_exit(config, section, key, message):
    # from Shantanu Naidu, objectInField
    try:
        return config[section][key]
    except KeyError:
        logging.error(message)
        sys.exit(message)
        
        
#def initialisePostProcessing():
    

        
        
def to_bool(value):
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



def runPostProcessing():

    """
    runPostProcessing()
    
    Author: Grigori Fedorets, Samuel Cornwall
    
    Description: This is the main file. Its purpose is to illustrate the workflow of the 
    post-processing tools, and to perform a suite of tasks such as filtering and colour manipulation.
    The output is written to a file.
    
    This file may need to be modified for the user's purposes.
    In its modified form, the recipe does the following:
    1. reads parameters from the config file
    2. reads the pointing history file
    3. reads the colour information file
    4. combines pointing and colour data into a single pandas dataframe
    5. applies basic filters, simulating, e.g. detection efficiency 
       of solar system processing, chip gaps, etc.
    6. connecting the apparent brightness of an asteroid with its colour
    7. matching observationID with a given optical filter
    8. Resolving the apparent brightness in a given optical filter corresponding to the pointing
    [here should be detection efficency function
    9. outputs to a csv file
    
    
    Mandatory input:      orbit file and colour file (designated in the config file)
                          The parameters are defined in the config file (./PPConfig.ini) 
    
    Output:               csv datafile
    
    
    usage: [from command line]                        python sample_recipe.py -c $CONFIGURATION_FILE --colour $COLOURFILE [--comet $COMETPARAMFILE]
    usage: [from command line, default config file]   python sample_recipe.py
    
    """

    ### Initialise argument parser
    args = parser.parse_args()
    
    
    ### Read arguments defined in the __main__ function
    configfile=args.c
    makeIntermediatePointingDatabase=bool(args.d)
    
    colourinput=args.l  
    orbinfile=args.o  
    oifoutput=args.p
    brightnessfile=args.b

    pplogger = get_logger()
    
    ### Read, assign and error-handle the configuration file
    pplogger.info('Reading configuration file...')
    
    config = configparser.ConfigParser()
    config.read(configfile)
    
    testvalue=int(config["GENERAL"]['testvalue'])
    fileseparator=get_or_exit(config, 'INPUTFILES', 'fileseparator', 'ERROR: no file separator specified.')
    if (fileseparator=='comma'):
        filesep=','
    elif (fileseparator=='blank'):
        filesep=' '
    else:
        pplogger.error('ERROR: file separator should be comma or blank.')
        sys.exit('ERROR: file separator should be comma or blank.')
    objecttype=get_or_exit(config, 'OBJECTS', 'objecttype', 'ERROR: no object type provided.')
    if (objecttype != 'asteroid' and objecttype != 'comet'):
         pplogger.error('ERROR: objecttype is neither an asteroid or a comet.') 
         sys.exit('ERROR: objecttype is neither an asteroid or a comet.')
    # Names of input files are given as flags
    if (objecttype == 'comet'):
        cometinput=args.m 
    pointingdatabase=get_or_exit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    
    mainfilter=get_or_exit(config,'FILTERS', 'mainfilter', 'ERROR: main filter not defined.')
    othercolours= [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    resfilters=[e.strip() for e in config.get('FILTERS', 'resfilters').split(',')]
    
    if (len(othercolours) != len(resfilters)-1):
         pplogger.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
         sys.exit('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
    if mainfilter != resfilters[0]:
         pplogger.error('ERROR: main filter should be the first among resfilters.')
         sys.exit('ERROR: main filter should be the first among resfilters.') 
    
    phasefunction=get_or_exit(config,'PHASE', 'phasefunction', 'ERROR: phase function not defined.')
    
    trailingLossesOn = to_bool(config["PERFORMANCE"]["trailingLossesOn"])
    cameraModel=get_or_exit(config, 'PERFORMANCE', 'cameraModel', 'ERROR: camera model not defined.')
    if (cameraModel != 'surfacearea') and (cameraModel != 'footprint'):
        pplogger.error('ERROR: cameraModel should be either surfacearea or footprint.')
        sys.exit('ERROR: cameraModel should be either surfacearea or footprint.')        
    if (cameraModel == 'footprint'):
        pplogger.info("loading camera footprint ...")
        #detectors=PPFootprintFilter.readFootPrintFile('./data/detectors_corners.csv')         
        footprint = PPFootprintFilter.Footprint("./data/detectors_corners.csv")
    
    SSPDetectionEfficiency=float(config["FILTERINGPARAMETERS"]['SSPDetectionEfficiency'])
    if (SSPDetectionEfficiency > 1.0 or SSPDetectionEfficiency > 1.0 or isinstance(SSPDetectionEfficiency,(float,int))==False):
        pplogger.error('ERROR: SSP detection efficiency out of bounds (should be between 0 and 1.), or not a number.')
        sys.exit('ERROR: SSP detection efficiency out of bounds (should be between 0 and 1.), or not a number.')
    fillfactor=float(config["FILTERINGPARAMETERS"]['fillfactor'])
    brightLimit=float(config["FILTERINGPARAMETERS"]['brightLimit'])
    inSepThreshold=float(config["FILTERINGPARAMETERS"]['inSepThreshold'])
    
    
    minTracklet=int(config["FILTERINGPARAMETERS"]['minTracklet'])    
    if (minTracklet < 1 or isinstance(minTracklet,int)==False):
        pplogger.error('ERROR: minimum length of tracklet is zero or negative, or not an integer.')
        sys.exit('ERROR: minimum length of tracklet is zero or negative, or not an integer.')
    noTracklets=int(config["FILTERINGPARAMETERS"]['noTracklets'])
    if (noTracklets  < 1 or isinstance(noTracklets, int)== False):
        pplogger.error('ERROR: number of tracklets is zero or less, or not an integer.')
        sys.exit('ERROR: number of tracklets is zero or less, or not an integer.')
    trackletInterval=float(config["FILTERINGPARAMETERS"]['trackletInterval'])
    if (trackletInterval <= 0.0 or isinstance(trackletInterval,(float,int))==False):
        logging.error('ERROR: tracklet appearance interval is negative, or not a number.')
        sys.exit('ERROR: tracklet appearance interval is negative, or not a number.')
      

    outpath=get_or_exit(config, 'OUTPUTFORMAT', 'outpath', 'ERROR: out path not specified.')   
    outfilestem=get_or_exit(config, 'OUTPUTFORMAT', 'outfilestem', 'ERROR: name of output file stem not specified.')    
    outputformat=get_or_exit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.')   
    if (outputformat != 'csv') and (outputformat != 'sqlite3') and (outputformat != 'hdf5') and (outputformat != 'HDF5') and (outputformat != 'h5') :
         sys.exit('ERROR: output format should be either csv, sqlite3 or hdf5.')
    separatelyCSV=to_bool(config["OUTPUTFORMAT"]['separatelyCSV'])
    sizeSerialChunk = int(config["GENERAL"]['sizeSerialChunk'])
    
    if (makeIntermediatePointingDatabase == True):
         PPMakeIntermediatePointingDatabase.PPMakeIntermediatePointingDatabase(oifoutput,'./data/interm.db', 100)
     
    
    pplogger.info('Reading pointing database and Matching observationID with appropriate optical filter...')
    filterpointing=PPMatchPointing.PPMatchPointing(pointingdatabase,resfilters)
    
    logging.info('Instantiating random number generator ... ')
    rng = np.random.default_rng(2021)
    
    
    ### In case of a large input file, the data is read in chunks. The "sizeSerialChunk" parameter in PPConfig.ini assigns the  chunk
    
    # Here, add loop which reads only a portion of input file to avoid memory overflow
    startChunk=0
    endChunk=0
    # number of rows in an entire orbit file
    
    ii=-1
    with open(orbinfile) as f:
        for ii, l in enumerate(f):
            pass
    lenf=ii
    
    while(endChunk <= lenf):
        endChunk=startChunk + sizeSerialChunk 
        if (lenf-startChunk > sizeSerialChunk):
             incrStep=sizeSerialChunk
        else:
             incrStep=lenf-startChunk
        
        ### Processing begins, all processing is done for chunks
        
        
        str1='Reading input orbit file: ' + orbinfile
        pplogger.info(str1)
        # The H given in the orbital DES file is omitted and erased; it is given in a separate brightness file instead
        padaor=PPReadOrbitFile.PPReadOrbitFile(orbinfile, startChunk, incrStep, filesep)
        padabr=PPReadBrightness.PPReadBrightness(brightnessfile,  startChunk, incrStep, filesep)
        
        if (objecttype == 'asteroid'):
            str3='Reading input colours: ' + colourinput
            pplogger.info(str3)
            padacl=PPReadColours.PPReadColours(colourinput, startChunk, incrStep, filesep)
        elif (objecttype == 'comet'):
            str4='Reading cometary parameters: ' + cometinput
            padaco=PPReadCometaryInput.PPReadCometaryInput(cometinput, startChunk, incrStep, filesep)
            padacl=PPReadColours.PPReadColours(colourinput, startChunk, incrStep, filesep)
        
        objid_list = padacl['ObjID'].unique().tolist() 

        
        # write pointing history to database
        # select obj_id rows from tables 
        
        if (makeIntermediatePointingDatabase == True):
            # read from intermediate database
            padafr=PPReadIntermDatabase.PPReadIntermDatabase('./data/interm.db', objid_list)
        else:   
            try: 
                str2='Reading input pointing history: ' + oifoutput
                pplogger.info(str2)
                oifoutputsuffix = oifoutput.split('.')[-1]
                padafr=PPReadOif.PPReadOif(oifoutput, filesep, oifoutputsuffix)
                
                # Here, we drop the magnitudes calculated by oif as they are calculated elsewhere
                # as they can be calculated with a variety of phase functions, and in different filters
                
                padafr=padafr.drop(['V', 'V(H=0)'], axis = 1, errors='ignore')
                
                padafr=padafr[padafr['ObjID'].isin(objid_list)]

            except MemoryError:
                pplogger.error('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
                sys.exit('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
        
    
        
        pplogger.info('Checking if orbit, brightness, colour/cometary and pointing simulation input files match...')
        if (objecttype == 'asteroid'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padacl,padafr)
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padabr,padafr)
        elif (objecttype == 'comet'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padacl,padafr)
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padabr,padafr)
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padaco,padafr)
            
        
        pplogger.info('Joining colour/cometary data with pointing data...')
        if (objecttype == 'asteroid'):
            observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padabr)
        elif (objecttype == 'comet'):
            
            observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padaco)
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padabr)
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padacl)

            pplogger.info('Joining orbital data with cometary data...')
            observations=PPJoinCometaryWithOrbits.PPJoinCometaryWithOrbits(observations,padaor)
 
        
        # comets may have dashes in their names that mix things up
        observations['ObjID'] = observations['ObjID'].astype(str)
        #observations['ObjID'] = observations['ObjID'].str.replace('/','')
        #observations=observations.update(observations[['ObjID']].applymap('"{}"'.format))

        print(list(observations.columns.values))
        
        pplogger.info('Calculating apparent magnitudes...')
        observations=PPCalculateApparentMagnitude.PPCalculateApparentMagnitude(observations, phasefunction, mainfilter)        
        

        if (objecttype=='comet'):
             pplogger.info('Calculating cometary magnitude using a simple model...')
             observations=PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude(observations, mainfilter)        
        
        pplogger.info('Hooking colour and brightness information...')
        i=0
        while (i<len(othercolours)):
             observations=PPhookBrightnessWithColour.PPhookBrightnessWithColour(observations, mainfilter, othercolours[i], resfilters[i+1])         
             i=i+1

        observations=observations.reset_index(drop=True)
        
        pplogger.info('Resolving the apparent brightness in a given optical filter corresponding to the pointing...')
        observations=PPMatchPointingsAndColours.PPMatchPointingsAndColours(observations,filterpointing)
        
                
        pplogger.info('Matching observationId with limiting magnitude and seeing...')
        seeing, limiting_magnitude=PPMatchFieldConditions.PPMatchFieldConditions(pointingdatabase)
        
               
        pplogger.info('Dropping observations that are too bright...')
        observations=PPBrightLimit.PPBrightLimit(observations,brightLimit)
        
        ### The treatment is further divided by cameraModel: surfaceArea is a much simpler model, mimicking the fraction of the surface
        ### area not covered by chip gaps, whereas footprint takes into account the actual footprints
        
        if (cameraModel == "surfacearea"):
            pplogger.info('Applying detection efficiency threshold...')
            observations=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(observations,SSPDetectionEfficiency)
        
            if (trailingLossesOn == True):
                pplogger.info('Calculating trailing losses...')
                observations['dmagDetect']=PPTrailingLoss.PPTrailingLoss(observations, seeing)

            else:
                observations['dmagDetect']=0.0
                
            logging.info("Dropping faint detections... ")
            observations.drop( np.where(observations["MaginFilter"] + observations["dmagDetect"] >= observations["fiveSigmaDepth"])[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
          
                
        elif (cameraModel == "footprint"):
                    
            pplogger.info('Calculating probabilities of detections...')
            observations["detection_probability"] = PPDetectionProbability(observations, filterpointing)
                   
            logging.info('Calculating astrometric and photometric uncertainties...')
            observations['AstrometricSigma(mas)'], observations['PhotometricSigma(mag)'], observations["SNR"] = PPAddUncertainties.addUncertainties(observations, filterpointing, obsIdNameEph='FieldID')
            observations["AstrometricSigma(deg)"] = observations['AstrometricSigma(mas)'] / 3600 / 1000
        
            logging.info('Dropping observations with signal to noise ratio less than 2...')
            observations.drop( np.where(observations["SNR"] <= 2.)[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
        
            logging.info('Applying uncertainty to photometry...')
            observations["MaginFilter"] = PPRandomizeMeasurements.randomizePhotometry(observations, magName="MaginFil", sigName="PhotometricSigma(mag)", rng=rng)
            
            if (trailingLossesOn == True):
                 logging.info('Calculating trailing losses...')
                 observations['dmagDetect']=PPTrailingLoss.PPTrailingLoss(observations, filterpointing)
            else:
                observations['dmagDetect']=0.0                 
                 
            logging.info('Calculating vignetting losses...')
            observations['dmagVignet']=PPVignetting.vignettingLosses(observations, filterpointing)
        
            logging.info("Dropping faint detections... ")
            observations.drop( np.where(observations["MaginFilter"] + observations["dmagDetect"] + observations['dmagVignet'] >= observations["fiveSigmaDepth"])[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
        
            logging.info('Calculating astrometric uncertainties...')
            observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
            observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
            observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(observations, sigName='AstrometricSigma(deg)', rng=rng)
                    
            logging.info('Applying sensor footprint filter...')
            #on_sensor=PPFootprintFilter.footPrintFilter(observations, filterpointing, detectors)#, ra_name="AstRATrue(deg)", dec_name="AstDecTrue(deg)")
            onSensor, detectorIDs = footprint.applyFootprint(observations, filterpointing)
            #observations=observations.iloc[on_sensor]       
            #observations=observations.astype({"FieldID": int})
            

            #on_sensor_concat = pd.concat(on_sensor).reset_index(drop=True)
            #for i in range(len(on_sensor)):
                #print(oif.iloc[on_sensor[i]])
                #observations.loc[np.isin(observations.index, on_sensor[i]), "detector"] = int(i)
            #observations=observations.iloc[on_sensor_concat]
            
            observations=observations.iloc[onSensor]
            observations["detectorID"] = detectorIDs
        
            #oif=oif.astype({"FieldID": int})
            #surveydb=surveydb.astype({"observationId": int})
            #oif["Filter"] = pd.merge(oif["FieldID"], surveydb, left_on="FieldID", right_on="observationId", how="left")['filter']
            logging.info('Dropping column with astrometric sigma in milliarcseconds ...')            
                    
            observations.drop(columns=["AstrometricSigma(mas)"])
            
        
        
        pplogger.info('Number of rows BEFORE applying detection probability threshold: ' + str(len(observations.index)))
    
        pplogger.info('Dropping observations below detection threshold...')
        observations=PPDropObservations.PPDropObservations(observations, "detection_probability")
        
        pplogger.info('Number of rows AFTER applying detection probability threshold: ' + str(len(observations.index)))
        
        
        
        pplogger.info('Applying SSP criterion efficiency...')

        observations=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(observations,minTracklet,noTracklets,trackletInterval,inSepThreshold)
        observations=observations.drop(['index'], axis='columns')
        
        pplogger.info('Number of rows AFTER applying SSP criterion threshold: ' + str(len(observations.index)))   

        pplogger.info('Saving data...')
        if endChunk == 0:
            mode ='w'
        elif endChunk > 0:
            mode='a'
        PPOut.PPWriteOut(observations, outpath + outfilestem, mode=mode, keyin=str(endChunk))
            
                        
        else:
            pplogger.error('ERROR: unknown output format.')
            sys.exit('ERROR: unknown output format.')
        
        startChunk = startChunk + sizeSerialChunk
        # end for
    
    pplogger.info('Post processing completed.')

if __name__=='__main__':

     parser = argparse.ArgumentParser()
     parser.add_argument("-c", "--config", help="Input configuration file name", type=str, dest='c', default='./PPConfig.ini')
     parser.add_argument("-d", help="Make intermediate pointing database", type=str, dest='d', default=False)
     parser.add_argument("-m", "--comet", help="Comet parameter file name", type=str, dest='m', default='./data/comet')
     parser.add_argument("-l", "--colour", "--color", help="Colour file name", type=str, dest='l', default='./data/colour')
     parser.add_argument("-o", "--orbit", help="Orbit file name", type=str, dest='o', default='./data/orbit.des')
     parser.add_argument("-p", "--pointing", help="Pointing simulation output file name", type=str, dest='p', default='./data/oiftestoutput')
     parser.add_argument("-b", "--brightness", "--phase", help="Brightness and phase parameter file name", type=str, dest='b', default='./data/HG')

     runPostProcessing()