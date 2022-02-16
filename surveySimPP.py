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
from modules import PPOutWriteCSV, PPOutWriteSqlite3, PPOutWriteHDF5
from modules import PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from modules import PPReadOif
from modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from modules import PPDropObservations, PPBrightLimit
from modules import PPMakeIntermediatePointingDatabase, PPReadIntermDatabase
from modules import PPReadCometaryInput, PPJoinOrbitalData, PPCalculateSimpleCometaryMagnitude
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
    3. reads the colour, orbit, brightness, and, optionally, cometary information files
    4. combines all data files into a single pandas dataframe
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
    
    
    usage: [from command line]                         python surveySimPP.py -c $CONFIGURATION_FILE -l $COLOURFILE -o $ORBITFILE -p $POINTINGSIMOUTPUT -b $~BRIGHTNESSFILE [--comet $COMETPARAMFILE]
    usage: [from command line, default config files]   python surveySimPP.py
    
    """

    ### Initialise argument parser
    args = parser.parse_args()
    
    
    ### Read arguments defined in the __main__ function
    configfile=args.c
    makeIntermediatePointingDatabase=bool(args.d)
    
    colourinput=args.l  
    orbinfile=args.o  
    oifoutput=args.p

    pplogger = get_logger()
    
    ### Read, assign and error-handle the configuration file
    pplogger.info('Reading configuration file...')
    
    config = configparser.ConfigParser()
    config.read(configfile)
    
    testvalue=int(config["GENERAL"]['testvalue'])
    pointingFormat=get_or_exit(config, 'INPUTFILES', 'pointingFormat', 'ERROR: no pointing simulation format is specified.')
    filesep=get_or_exit(config, 'INPUTFILES', 'auxFormat', 'ERROR: no auxilliary data (e.g. colour) format specified.')    
    objecttype=get_or_exit(config, 'OBJECTS', 'objecttype', 'ERROR: no object type provided.')
    if (objecttype != 'asteroid' and objecttype != 'comet'):
         pplogger.error('ERROR: objecttype is neither an asteroid or a comet.') 
         sys.exit('ERROR: objecttype is neither an asteroid or a comet.')
    # Names of input files are given as flags
    if (objecttype == 'comet'):
        cometinput=args.m 
    pointingdatabase=get_or_exit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    ppdbquery=get_or_exit(config, 'INPUTFILES', 'ppsqldbquery', 'ERROR: no pointing database SQLite3 query provided.')
    
    pplogger.info('Object type is ' + str(objecttype))
    
    pplogger.info('Pointing simulation result format is: ' + pointingFormat) 
    pplogger.info('Pointing simulation result path is: ' + pointingdatabase)
    pplogger.info('Pointing simulation result required query is: ' +  ppdbquery) 

    
    mainfilter=get_or_exit(config,'FILTERS', 'mainfilter', 'ERROR: main filter not defined.')
    othercolours= [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    resfilters=[e.strip() for e in config.get('FILTERS', 'resfilters').split(',')]
    

    
    if (len(othercolours) != len(resfilters)-1):
         pplogger.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
         sys.exit('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
    if mainfilter != resfilters[0]:
         pplogger.error('ERROR: main filter should be the first among resfilters.')
         sys.exit('ERROR: main filter should be the first among resfilters.') 
         
    pplogger.info('The main filter in which brightness is defined is ' + mainfilter)
    othcs=' '.join(str(e) for e in othercolours)
    pplogger.info('The colour indices included in the simulation are ' + othcs)
    rescs=' '.join(str(f) for f in resfilters)
    pplogger.info('Hence, the filters included in the post-processing results are ' + rescs)    
    
    phasefunction=get_or_exit(config,'PHASE', 'phasefunction', 'ERROR: phase function not defined.')
    
    pplogger.info('The apparent brightness is calculated using the following phase function model: ' + phasefunction)
    
    trailingLossesOn = to_bool(config["PERFORMANCE"]["trailingLossesOn"])
    
    if (trailingLossesOn == True):
             pplogger.info('Computation of trailing losses is switched ON.')
    else:
             pplogger.info('Computation of trailing losses is switched OFF.')

    
    cameraModel=get_or_exit(config, 'PERFORMANCE', 'cameraModel', 'ERROR: camera model not defined.')
    if (cameraModel != 'circle') and (cameraModel != 'footprint'):
        pplogger.error('ERROR: cameraModel should be either surfacearea or footprint.')
        sys.exit('ERROR: cameraModel should be either surfacearea or footprint.')        
    elif (cameraModel == 'footprint'):
        footprintPath=get_or_exit(config, 'INPUTFILES', 'footprintPath', 'ERROR: no camera footprint provided.')
        pplogger.info('Footprint is modelled after the actual camera footprint.')
        footprintf = PPFootprintFilter.Footprint(footprintPath)
        pplogger.info("loading camera footprint from " + footprintPath)
    else:
        pplogger.info('Footprint is circular')
    
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
    
    pplogger.info('Simulated SSP detection efficienxy is ' + str(SSPDetectionEfficiency))
    pplogger.info('The filling factor for the circular footprint is ' + str(fillfactor))
    pplogger.info('The upper (saturation) limit is ' + str(brightLimit))
    pplogger.info('For Solar System Processing, the minimum required number of observatrions in a tracklet is ' + str(minTracklet))
    pplogger.info('For Solar System Processing, the minimum required number of tracklets is' + str(noTracklets))
    pplogger.info('Fos Solar System Processing, the maximum interval of time in days of tracklets to be contained in is ' + str(trackletInterval))
    pplogger.info('For Solar System Processing, the minimum angular separation between observations in arcseconds is ' + str(inSepThreshold))



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
    filterpointing=PPMatchPointing.PPMatchPointing(pointingdatabase,resfilters,ppdbquery)
    
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
        
        pplogger.info('Reading input orbit file: ' + orbinfile)
        # The H given in the orbital DES file is omitted and erased; it is given in a separate brightness file instead
        padaor=PPReadOrbitFile.PPReadOrbitFile(orbinfile, startChunk, incrStep, filesep)
        
        pplogger.info('Reading input colours: ' + colourinput)
        padacl=PPReadColours.PPReadColours(colourinput, startChunk, incrStep, filesep)
        if (objecttype == 'comet'):
            pplogger.info('Reading cometary parameters: ' + cometinput)
            padaco=PPReadCometaryInput.PPReadCometaryInput(cometinput, startChunk, incrStep, filesep)
        
        objid_list = padacl['ObjID'].unique().tolist() 

        
        # write pointing history to database
        # select obj_id rows from tables 
        
        if (makeIntermediatePointingDatabase == True):
            # read from intermediate database
            padafr=PPReadIntermDatabase.PPReadIntermDatabase('./data/interm.db', objid_list)
        else:   
            try: 
                pplogger.info('Reading input pointing history: ' + oifoutput)
                oifoutputsuffix = oifoutput.split('.')[-1]
                padafr=PPReadOif.PPReadOif(oifoutput, pointingFormat)
                
                
                padafr=padafr[padafr['ObjID'].isin(objid_list)]

            except MemoryError:
                pplogger.error('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
                sys.exit('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
        
    
        
        pplogger.info('Checking if orbit, brightness, colour/cometary and pointing simulation input files match...')

        PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padacl,padafr)
        ###PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padabr,padafr)
        
        if (objecttype == 'comet'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padaco,padafr)
            
        
        pplogger.info('Joining physical parameters and orbital data with pointing data...')
        
        observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
        observations=PPJoinOrbitalData.PPJoinOrbitalData(observations,padaor)
        if (objecttype == 'comet'):
            pplogger.info('Joining cometary data...')
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padaco)

 
        
        # comets may have dashes in their names that mix things up
        observations['ObjID'] = observations['ObjID'].astype(str)
        #observations['ObjID'] = observations['ObjID'].str.replace('/','')
        
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
        seeing, limiting_magnitude=PPMatchFieldConditions.PPMatchFieldConditions(pointingdatabase,ppdbquery)
        
               
        pplogger.info('Dropping observations that are too bright...')
        observations=PPBrightLimit.PPBrightLimit(observations,brightLimit)
        
        ### The treatment is further divided by cameraModel: surfaceArea is a much simpler model, mimicking the fraction of the surface
        ### area not covered by chip gaps, whereas footprint takes into account the actual footprints
        
        if (cameraModel == "circle"):
            pplogger.info('Applying detection efficiency threshold...')
            observations=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(observations,SSPDetectionEfficiency)
        
            if (trailingLossesOn == True):
                pplogger.info('Calculating trailing losses...')
                observations['dmagDetect']=PPTrailingLoss.PPTrailingLoss(observations, seeing)

            else:
                observations['dmagDetect']=0.0
                
            logging.info("Dropping faint detections... ")
            observations.drop( np.where(observations["MagnitudeInFilter"] + observations["dmagDetect"] >= observations["fiveSigmaDepth"])[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
          
                
        elif (cameraModel == "footprint"):
                    
            pplogger.info('Calculating probabilities of detections...')
            observations["detection_probability"] = PPDetectionProbability(observations, filterpointing)
                   
            pplogger.info('Calculating astrometric and photometric uncertainties...')
            observations['AstrometricSigma(mas)'], observations['PhotometricSigma(mag)'], observations["SNR"] = PPAddUncertainties.addUncertainties(observations, filterpointing, obsIdNameEph='FieldID')
            observations["AstrometricSigma(deg)"] = observations['AstrometricSigma(mas)'] / 3600. / 1000.
        
            pplogger.info('Dropping observations with signal to noise ratio less than 2...')
            observations.drop( np.where(observations["SNR"] <= 2.)[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
        
            pplogger.info('Applying uncertainty to photometry...')
            observations["MagnitudeInFilter"] = PPRandomizeMeasurements.randomizePhotometry(observations, magName="MagnitudeInFilter", sigName="PhotometricSigma(mag)", rng=rng)
            
            if (trailingLossesOn == True):
                 logging.info('Calculating trailing losses...')
                 observations['dmagDetect']=PPTrailingLoss.PPTrailingLoss(observations, filterpointing)
            else:
                observations['dmagDetect']=0.0                 
                 
            pplogger.info('Calculating vignetting losses...')
            observations['dmagVignet']=PPVignetting.vignettingLosses(observations, filterpointing)
        
            pplogger.info("Dropping faint detections... ")
            observations.drop( np.where(observations["MagnitudeInFilter"] + observations["dmagDetect"] + observations['dmagVignet'] >= observations["fiveSigmaDepth"])[0], inplace=True)
            observations.reset_index(drop=True, inplace=True)
        
            pplogger.info('Calculating astrometric uncertainties...')
            observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
            observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
            observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(observations, sigName='AstrometricSigma(deg)', rng=rng)
                    
            pplogger.info('Applying sensor footprint filter...')
            #on_sensor=PPFootprintFilter.footPrintFilter(observations, filterpointing, detectors)#, ra_name="AstRATrue(deg)", dec_name="AstDecTrue(deg)")
            onSensor, detectorIDs = footprintf.applyFootprint(observations, filterpointing)
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
            pplogger.info('Dropping column with astrometric sigma in milliarcseconds ...')            
                    
            observations.drop(columns=["AstrometricSigma(mas)"])
            
        
        
            pplogger.info('Number of rows BEFORE applying detection probability threshold: ' + str(len(observations.index)))
        
            pplogger.info('Dropping observations below detection threshold...')
            observations=PPDropObservations.PPDropObservations(observations, "detection_probability")
            
            pplogger.info('Number of rows AFTER applying detection probability threshold: ' + str(len(observations.index)))
        
            # end camera footprint
        
        pplogger.info('Applying SSP criterion efficiency...')

        observations=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(observations,minTracklet,noTracklets,trackletInterval,inSepThreshold)
        observations=observations.drop(['index'], axis='columns')
        
        pplogger.info('Number of rows AFTER applying SSP criterion threshold: ' + str(len(observations.index)))

                
        
        
        
    
        pplogger.info('Constructing output path...')
        if (outputformat == 'csv'):
            outputsuffix='.csv'
            if (separatelyCSV == True):
                objid_list = observations['ObjID'].unique().tolist() 
                pplogger.info('Output to ' + str(len(objid_list)) + ' separate output CSV files...')
                i=0
                while(i<len(objid_list)):
                         single_object_df=pd.DataFrame(observations[observations['ObjID'] == objid_list[i]])
                         out=outpath + str(objid_list[i]) + '_' + outfilestem + outputsuffix
                         obsi=PPOutWriteCSV.PPOutWriteCSV(single_object_df,out)
                         i=i+1
            else:
                out=outpath + outfilestem + outputsuffix
                pplogger.info('Output to CSV file...')
                observations=PPOutWriteCSV.PPOutWriteCSV(observations,out)
            
        elif (outputformat == 'sqlite3'):
            outputsuffix='.db'
            out=outpath + outfilestem + outputsuffix
            pplogger.info('Output to sqlite3 database...')
            observations=PPOutWriteSqlite3.PPOutWriteSqlite3(observations,out)   
        elif (outputformat == 'hdf5' or outputformat=='HDF5'):
            outputsuffix=".h5"   
            out=outpath + outfilestem + outputsuffix
            pplogger.info('Output to HDF5 binary file...')
            observations=PPOutWriteHDF5.PPOutWriteHDF5(observations,out,str(endChunk))    
            
                        
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



     runPostProcessing()
