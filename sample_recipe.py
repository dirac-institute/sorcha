#!/usr/bin/python

import os,sys
import pandas as pd
import logging
import argparse
import configparser
from lsstcomet import *
#from filtering import PPFilterDetectionEfficiencyThreshold
from modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPReadColours
from modules import PPhookBrightnessWithColour, PPJoinColourPointing, PPMatchPointing 
from modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency
from modules import PPOutWriteCSV, PPOutWriteSqlite3, PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from modules import PPReadOif
from modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from modules import PPDropObservations, PPBrightLimit
from modules import PPMakeIntermediatePointingDatabase, PPReadIntermDatabase
from modules import PPReadCometaryInput, PPJoinCometaryWithOrbits, PPCalculateSimpleCometaryMagnitude

#oifoutput=sys.argv[1]

# Configurate logging settings
#PPConfig.verbosity=PPConfig.verbosity*10
#logging.basicConfig(filename=PPConfig.logloc, encoding='utf-8', level=PPConfig.verbosity)

# Read config file


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

def runPostProcessing():

    """
    runPostProcessing()
    
    Author: Grigori Fedorets
    
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

    
    args = parser.parse_args()
    
    configfile=args.c
    makeIntermediatePointingDatabase=bool(args.d)
    
    colourinput=args.l  
    orbinfile=args.o  
    oifoutput=args.p


    pplogger = get_logger()
    
    
    pplogger.info('Reading configuration file...')
    
    config = configparser.ConfigParser()
    config.read(configfile)
    
    testvalue=int(config["GENERAL"]['testvalue'])
    objecttype=get_or_exit(config, 'OBJECTS', 'objecttype', 'ERROR: no object type provided.')
    #objecttype.strip()
    if (objecttype != 'asteroid' and objecttype != 'comet'):
         logging.error('ERROR: objecttype is neither an asteroid or a comet.') 
         sys.exit('ERROR: objecttype is neither an asteroid or a comet.')
    #orbinfile=get_or_exit(config, 'INPUTFILES', 'orbinfile', 'ERROR: no orbit file (DES) provided.')    
    #oifoutput=get_or_exit(config, 'INPUTFILES', 'oifoutput', 'ERROR: no ObjectInField output file provided.')
    if (objecttype == 'asteroid'):
        colourinput=get_or_exit(config, 'INPUTFILES', 'colourinput', 'ERROR: no colour input file provided.')
    elif (objecttype == 'comet'):
        #cometinput=args.comet
        cometinput=args.m 
        #if (cometinput == 'cometplaceholder'):
            # is not defined as flag but rather in input file
            #cometinput=get_or_exit(config, 'INPUTFILES', 'cometinput', 'ERROR: no comet input file provided.')
    pointingdatabase=get_or_exit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    
    mainfilter=get_or_exit(config,'FILTERS', 'mainfilter', 'ERROR: main filter not defined.')
    othercolours= [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    resfilters=[e.strip() for e in config.get('FILTERS', 'resfilters').split(',')]
    
    if (len(othercolours) != len(resfilters)-1):
         logging.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
         sys.exit('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
    if mainfilter != resfilters[0]:
         logging.error('ERROR: main filter should be the first among resfilters.')
         sys.exit('ERROR: main filter should be the first among resfilters.') 
    
    SSPDetectionEfficiency=float(config["FILTERINGPARAMETERS"]['SSPDetectionEfficiency'])
    fillfactor=float(config["FILTERINGPARAMETERS"]['fillfactor'])
    brightLimit=float(config["FILTERINGPARAMETERS"]['brightLimit'])
    inSepThreshold=float(config["FILTERINGPARAMETERS"]['inSepThreshold'])
    
    
    minTracklet=int(config["FILTERINGPARAMETERS"]['minTracklet'])
    if minTracklet < 1:
        logging.error('ERROR: minimum length of tracklet is zero or negative.')
        sys.exit('ERROR: minimum length of tracklet is zero or negative.')
    noTracklets=int(config["FILTERINGPARAMETERS"]['noTracklets'])
    if noTracklets < 1:
        logging.error('ERROR: number of tracklets is zero or negative.')
        sys.exit('ERROR: number of tracklets is zero or negative')
    trackletInterval=float(config["FILTERINGPARAMETERS"]['trackletInterval'])
    if trackletInterval <= 0.0:
        logging.error('ERROR: tracklet interval is negative.')
        sys.exit('ERROR: tracklet interval is negative.')        

    outpath=get_or_exit(config, 'OUTPUTFORMAT', 'outpath', 'ERROR: out path not specified.')   
    outfilestem=get_or_exit(config, 'OUTPUTFORMAT', 'outfilestem', 'ERROR: name of output file stem not specified.')    
    outputformat=get_or_exit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.')   
    if (outputformat != 'csv') and (outputformat != 'sqlite3'):
         sys.exit('ERROR: output format should be either csv or sqlite3.')
    separatelyCSV=bool(config["OUTPUTFORMAT"]['separatelyCSV'])
    sizeSerialChunk = int(config["GENERAL"]['sizeSerialChunk'])

    
    if (makeIntermediatePointingDatabase == True):
         PPMakeIntermediatePointingDatabase.PPMakeIntermediatePointingDatabase(oifoutput,'./data/interm.db', 100)


    #testvalue,oifoutput,colourinput,pointingdatabase,SSPDetectionEfficiency, \
    #minTracklet,noTracklets,trackletInterval \
    #=PPReadConfigFile.PPReadConfigFile()
    
    # Due to the restriction of the logger object, the parsing is done in a weird way
    # when taking arguments
    
    
    pplogger.info('Matching observationID with appropriate optical filter...')
    filterpointing=PPMatchPointing.PPMatchPointing(pointingdatabase,resfilters)
    #print(pada5)
    
    
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
        #print(lenf,startChunk,endChunk,incrStep)
        
        str1='Reading input orbit file: ' + orbinfile
        pplogger.info(str1)
        padaor=PPReadOrbitFile.PPReadOrbitFile(orbinfile, startChunk, incrStep)
        
        if (objecttype == 'asteroid'):
            str3='Reading input colours: ' + colourinput
            pplogger.info(str3)
            padacl=PPReadColours.PPReadColours(colourinput, startChunk, incrStep)
        elif (objecttype == 'comet'):
            str4='Reading cometary parameters: ' + cometinput
            padaco=PPReadCometaryInput.PPReadCometaryInput(cometinput, startChunk, incrStep)
            padacl=PPReadColours.PPReadColours(colourinput, startChunk, incrStep)
        
        
        objid_list = padacl['ObjID'].unique().tolist() 

        
        # write pointing history to d
        # select obj_id rows from tables 
        
        if (makeIntermediatePointingDatabase == True):
            # read from intermediate database
            padafr=PPReadIntermDatabase.PPReadIntermDatabase('./data/interm.db', objid_list)
        else:   
            try: 
                str2='Reading input pointing history: ' + oifoutput
                pplogger.info(str2)
                padafr=PPReadOif.PPReadOif(oifoutput)
                
                padafr=padafr[padafr['ObjID'].isin(objid_list)]

            except MemoryError:
                pplogger.error('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
                sys.exit('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
        
    
        
        pplogger.info('Checking if orbit, colour/cometary and pointing simulation input files match...')
        if (objecttype == 'asteroid'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padacl,padafr)
        elif (objecttype == 'comet'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padaco,padafr)
            
        
        pplogger.info('Joining colour/cometary data with pointing data...')
        if (objecttype == 'asteroid'):
            observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
        elif (objecttype == 'comet'):
            
            observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padaco)
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padacl)

            pplogger.info('Joining orbital data with cometary data...')
            observations=PPJoinCometaryWithOrbits.PPJoinCometaryWithOrbits(observations,padaor)
 
        print('THIS NEEDS TO BE REDONE: for now, mainfilter is converted from V magnitude')
        observations[mainfilter] = observations['V']
        
        
        pplogger.info('Applying detection efficiency threshold...')
        observations=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(observations,SSPDetectionEfficiency)
        
        
        #print(pada1)
        
        pplogger.info('Applying simple sensor area losses...')  
        observations=PPSimpleSensorArea.PPSimpleSensorArea(observations, fillfactor)
        
        
        #print(pada1)

        print(len(observations.columns))
        if (objecttype=='comet'):
             pplogger.info('Calculating cometary magnitude using a simple model...')
             observations=PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude(observations, mainfilter)
                    
             print(len(observations.columns))
        
        
        pplogger.info('Hooking colour and brightness information...')
        i=0
        while (i<len(othercolours)):
             observations=PPhookBrightnessWithColour.PPhookBrightnessWithColour(observations, mainfilter, othercolours[i], resfilters[i+1])         
             i=i+1
        #resdf1=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
        #resdf3=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf1, 'V', 'g-X', 'g')
        
        #resdf3=resdf1
        #print(resdf3)
        
        
        pplogger.info('Resolving the apparent brightness in a given optical filter corresponding to the pointing...')
        observations=PPMatchPointingsAndColours.PPMatchPointingsAndColours(observations,filterpointing)
        

        #print(pada6)

        #print(pada6)
        
        #-----------------------------------------------
        
        logging.info('Matching observationId with limiting magnitude and seeing...')
        seeing, limiting_magnitude=PPMatchFieldConditions.PPMatchFieldConditions(pointingdatabase)
        
        #print(pada6)
        logging.info('Calculating trailing losses...')
        observations=PPTrailingLoss.PPTrailingLoss(observations, seeing)
        
        pplogger.info('Dropping observations that are too bright...')
        observations=PPBrightLimit.PPBrightLimit(observations,brightLimit)
        
        
        
        
        logging.info('Calculating probabilities of detections...')
        observations=PPDetectionProbability.PPDetectionProbability(observations,limiting_magnitude)
    
        logging.info('Dropping observations below detection threshold...')
        observations=PPDropObservations.PPDropObservations(observations)
    
        
        #----------------------------------------------
        #print(pada6)
        
        
        pplogger.info('Applying SSP criterion efficiency...')

        observations=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(observations,minTracklet,noTracklets,trackletInterval,inSepThreshold)
        observations=observations.drop(['index'], axis='columns')
        
        #print(observations['FieldID'].to_string())
        
        
        # comets may have dashes in their names that mix things up
        observations['ObjID'] = observations['ObjID'].str.replace('/','')
        
        #print(observations['FieldMJD'].to_string())
        #print(observations.columns.to_string())
        
    
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
            #pada8=PPOutWriteSqlite3.PPOutWriteSqlite3(pada6,out)   
            observations=PPOutWriteSqlite3.PPOutWriteSqlite3(observations,out)               
        else:
            pplogger.error('ERROR: unknown output format.')
            sys.exit('ERROR: unknown output format.')
        
        startChunk = startChunk + sizeSerialChunk
        # end for
    
    pplogger.info('Post processing completed.')

if __name__=='__main__':

     parser = argparse.ArgumentParser()
     parser.add_argument("-c", "--config", help="Input configuration filename", type=str, dest='c', default='./PPConfig.ini')
     parser.add_argument("-d", help="Make intermediate pointing database", type=str, dest='d', default=False)
     parser.add_argument("-m", "--comet", help="Comet parameter filename", type=str, dest='m', default='./data/comet')
     parser.add_argument("-l", "--colour", "--color", help="Colour file name", type=str, dest='l', default='./data/colour')
     parser.add_argument("-o", "--orbit", help="Orbit file name", type=str, dest='o', default='./data/orbit.des')
     parser.add_argument("-p", "--pointing", help="Pointing simulation file name", type=str, dest='p', default='./data/oiftestoutput')




     runPostProcessing()
