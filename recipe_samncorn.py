#!/usr/bin/python

import os,sys
import pandas as pd
import numpy as np
import logging
import argparse
import configparser
import time
#from filtering import PPFilterDetectionEfficiencyThreshold

from modules import PPOutWriteCSV, PPOutWriteSqlite3, PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from modules import PPBrightLimit
from modules import PPAddUncertainties
from modules import PPDropObservations
from modules.PPDetectionProbability import calcDetectionProbability
from modules.PPAddUncertainties import calcAstrometricUncertainty, magErrorFromSNR
from modules import PPTranslateMagnitude
import sqlite3 as sql
import tracemalloc


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
    
    
    usage: [from command line]                        python sample_recipe.py -c $CONFIGURATION_FILE
    usage: [from command line, default config file]   python sample_recipe.py
    
    """

    t0=time.time()
    
    args = parser.parse_args()
    
    configfile=args.c

    pplogger = get_logger()
    
    
    pplogger.info('Reading configuration file...')
    
    config = configparser.ConfigParser()
    config.read(configfile)
    
    testvalue=int(config["GENERAL"]['testvalue'])
    orbinfile=get_or_exit(config, 'INPUTFILES', 'orbinfile', 'ERROR: no orbit file (DES) provided.')    
    oifoutput=get_or_exit(config, 'INPUTFILES', 'oifoutput', 'ERROR: no ObjectInField output file provided.')
    colourinput=get_or_exit(config, 'INPUTFILES', 'colourinput', 'ERROR: no colour input file provided.')
    pointingdatabase=get_or_exit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    
    mainfilter=get_or_exit(config,'FILTERS', 'mainfilter', 'ERROR: main filter not defined.')
    othercolours= [e.strip() for e in config.get('FILTERS', 'othercolours').split(',')]
    resfilters=[e.strip() for e in config.get('FILTERS', 'resfilters').split(',')]
    
    if (len(othercolours) != len(resfilters)-1):
         logging.error('ERROR: mismatch in input config colours and filters: len(othercolours) != len(resfilters) + 1')
         sys.exit()
    if mainfilter != resfilters[0]:
         logging.error('ERROR: main filter should be the first among resfilters.')
         sys.exit() 
    
    SSPDetectionEfficiency=float(config["FILTERINGPARAMETERS"]['SSPDetectionEfficiency'])
    fillfactor=float(config["FILTERINGPARAMETERS"]['fillfactor'])
    brightLimit=float(config["FILTERINGPARAMETERS"]['brightLimit'])
    inSepThreshold=float(config["FILTERINGPARAMETERS"]['inSepThreshold'])
    
    
    minTracklet=int(config["FILTERINGPARAMETERS"]['minTracklet'])
    if minTracklet < 1:
        logging.error('ERROR: minimum length of tracklet is zero or negative.')
        sys.exit()
    noTracklets=int(config["FILTERINGPARAMETERS"]['noTracklets'])
    if noTracklets < 1:
        logging.error('ERROR: number of tracklets is zero or negative.')
        sys.exit()
    trackletInterval=float(config["FILTERINGPARAMETERS"]['trackletInterval'])
    if trackletInterval <= 0.0:
        logging.error('ERROR: tracklet interval is negative.')
        sys.exit()        

    outpath=get_or_exit(config, 'OUTPUTFORMAT', 'outpath', 'ERROR: out path not specified.')   
    outfilestem=get_or_exit(config, 'OUTPUTFORMAT', 'outfilestem', 'ERROR: name of output file stem not specified.')    
    outputformat=get_or_exit(config, 'OUTPUTFORMAT', 'outputformat', 'ERROR: output format not specified.')   
    if (outputformat != 'csv') and (outputformat != 'sqlite3') and (outputformat != 'hdf5'):
         sys.exit('ERROR: output format should be either csv or sqlite3.')



    #testvalue,oifoutput,colourinput,pointingdatabase,SSPDetectionEfficiency, \
    #minTracklet,noTracklets,trackletInterval \
    #=PPReadConfigFile.PPReadConfigFile()
    
    # Due to the restriction of ther logger object, the parsing is done in a weird way
    # when taking arguments
    str1='Reading input orbit file: ' + orbinfile
    pplogger.info(str1)
    #orbits=pd.read_csv(orbinfile, delim_whitespace=True)
    #PPReadOrbitFile.PPReadOrbitFile(orbinfile)
    
    str2='Reading input pointing history: ' + oifoutput
    pplogger.info(str2)
    oif=pd.read_hdf(oifoutput).reset_index(drop=True)
    #readOif.readOif(oifoutput)
    
    pplogger.info('Reading pointing database')
    con=sql.connect(pointingdatabase)
    surveydb=pd.read_sql_query('SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, fiveSigmaDepth FROM SummaryAllProps order by observationId', con)
    
    str3='Reading input colours: ' + colourinput
    pplogger.info(str3)
    colors=pd.read_csv(colourinput, delim_whitespace=True)
    #PPreadColours.PPreadColours(colourinput)
    
    #should check the performance on this
    #pplogger.info('Checking if orbit, colour and pointing simulation input files match...')
    #PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(orbits,colors,oif)
    
    
    logging.info('Applying simple sensor area losses...')  
    #oif=PPSimpleSensorArea.PPSimpleSensorArea(oif, fillfactor)
    #Why do we have the above? add fillfactor to detection probability
    #nvm, looking into using the camera footprint from the LSST stack, so
    #it may be smart to keep a seperate step
    PPDropObservations.PPDropObservations(oif, fillfactor)
    
    logging.info('Translating magnitudes to appropriate filters...')  
    oif["MaginFil"]=PPTranslateMagnitude.PPTranslateMagnitude(oif, surveydb, colors)
    
    #-----------------------------------------------
    
    logging.info('Calculating trailing losses...')
    oif['dmagDetect'], _ =PPTrailingLoss.PPTrailingLoss(oif, surveydb)
    
    lim_mag = surveydb.lookup(oif["FieldID"], ['fiveSigmaDepth']*len(oif.index))
    
    logging.info('Calculating probabilities of detections...')
    oif['probability'] = PPDetectionProbability(oif, surveydb, trailing_losses=True)

    logging.info('Dropping observations below detection threshold...')
    PPDropObservations.PPDropObservations(oif, oif['probability'])
    
    logging.info('Calculating astrometric and photometric uncertainties')
    oif['AstRASigma(mas)'], oif['PhotometricSigma(mag)'] = PPAddUncertainties.addUncertainties(oif, surveydb, obsIdNameEph='FieldID')
    oif['AstDecSigma(mas)'] = oif['AstRASigma(mas)']
    
    #----------------------------------------------
    
    #pplogger.info('Applying SSP criterion efficiency...')
    #pada7=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(pada5,1,1,15.0,inSepThreshold)

    
    pplogger.info('Constructing output path...')
    if (outputformat == 'csv'):
        outputsuffix='.csv'
        out=outpath + outfilestem + outputsuffix
        pplogger.info('Output to CSV file...')
        oif=PPOutWriteCSV.PPOutWriteCSV(oif,out)
    elif (outputformat == 'sqlite3'):
        outputsuffix='.db'
        out=outpath + outfilestem + outputsuffix
        pplogger.info('Output to sqlite3 database...')
        oif=PPOutWriteSqlite3.PPOutWriteSqlite3(oif,out)     
    elif (outputformat=='hdf5'):
        outputsuffix='.h5'
        out=outpath + outfilestem + outputsuffix
        pplogger.info('Output to hdf5')
        
        if (os.path.isfile(out)):
            oif.to_hdf(out,key='data',
                       complevel=3, complib='zlib',index=False,
                       format='table', mode='a')
        else:
            oif.to_hdf(out,key='data',
                       complevel=3, complib='zlib',index=False,
                       format='table')
    else:
        pplogger.error('ERROR: unknown output format.')
        sys.exit('ERROR: unknown output format.')
    
    pplogger.info('Post processing completed.')
    
    t1=time.time()
    pplogger.info('runtime: '+str(t1-t0))

if __name__=='__main__':

     parser = argparse.ArgumentParser()
     parser.add_argument("-c", help="Input configuration filename", type=str, default='./PPConfig.ini')

     tracemalloc.start()
     runPostProcessing()
     _, peak = tracemalloc.get_traced_memory()
     print("Peak memory use was %f3.3 GB" %(peak / 10**9))
