# Sam Cornwall's post processing script for the simulated solar system catalogue
# Based on Grigori Fedorets' post processing script
#
import os, sys
import numpy as np
import pandas as pd
import logging
import argparse
import configparser
import time
import tracemalloc
import sqlite3 as sql

from modules import PPTranslateMagnitude
from modules import PPAddUncertainties
from modules import PPRandomizeMeasurements
from modules import PPTrailingLoss
from modules import PPFootprintFilter
from modules import PPOutWriteCSV
from modules import PPOutWriteSqlite3
from modules import PPVignetting

def get_logger(
        LOG_FORMAT     = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s ',
        LOG_NAME       = '',
        LOG_FILE_INFO  = 'postprocessing.log',
        LOG_FILE_ERROR = 'postprocessing.err'):

    #From Grigori Fedorets' post processing recipe

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

def run():

    t0=time.time()

    args = parser.parse_args()
    configfile=args.c

    pplogger = get_logger()

    config = configparser.ConfigParser()

    #load defaults and specified config file
    defaults = './configs/defaults.ini'
    config.read(defaults)
    config.read(configfile)

    testvalue=int(config["GENERAL"]['testvalue'])
    #orbinfile=get_or_exit(config, 'INPUTFILES', 'orbinfile', 'ERROR: no orbit file (DES) provided.')           The orbit file is not used
    oifoutput=get_or_exit(config, 'INPUTFILES', 'oifoutput', 'ERROR: no ObjectInField output file provided.')
    colourinput=get_or_exit(config, 'INPUTFILES', 'colourinput', 'ERROR: no colour input file provided.')
    pointingdatabase=get_or_exit(config, 'INPUTFILES', 'pointingdatabase', 'ERROR: no pointing database provided.')
    footprint=get_or_exit(config, "INPUTFILES", "camerafootprint", "ERROR: no footprint provided.")


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

#------------------------------------------------------------------------------

    str2='Reading input pointing history: ' + oifoutput
    pplogger.info(str2)

    file_ext = oifoutput.split('.')[-1]
    if file_ext == 'h5':
        oif=pd.read_hdf(oifoutput).reset_index(drop=True)
    elif file_ext == 'csv':
        oif = pd.read_csv(oifoutput, delim_whitespace=True)
    else:
        oif=pd.read_hdf(oifoutput).reset_index(drop=True)

    pplogger.info('Reading pointing database')
    con=sql.connect(pointingdatabase)
    surveydb=pd.read_sql_query('SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec, rotSkyPos FROM SummaryAllProps order by observationId', con)

    logging.info("Joining pointing data to objects observations...")
    surveydb_join= pd.merge(oif["FieldID"], surveydb, left_on="FieldID", right_on="observationId", how="left")
    for name in surveydb.columns:
        oif[name] = surveydb_join

    str3='Reading input colours: ' + colourinput
    pplogger.info(str3)
    colors=pd.read_csv(colourinput, delim_whitespace=True)

    logging.info("loading camera footprint ...")
    detectors=PPFootprintFilter_xyz.readFootPrintFile('detectors_corners.csv')

    logging.info('Translating magnitudes to appropriate filters...')
    oif["MaginFilterTrue"]=PPTranslateMagnitude.PPTranslateMagnitude(oif, surveydb, colors)

    logging.info('Calculating astromentric and photometric uncertainties...')
    oif['AstrometricSigma(mas)'], oif['PhotometricSigma(mag)'], oif["SNR"] = PPAddUncertainties.addUncertainties(oif, surveydb, obsIdNameEph='FieldID')
    oif["AstrometricSigma(deg)"] = oif['AstrometricSigma(mas)'] / 3600 / 1000

    logging.info('Dropping observations with signal to noise ratio less than 2...')
    oif.drop( np.where(oif["SNR"] <= 2.)[0], inplace=True)
    oif.reset_index(drop=True, inplace=True)

    logging.info('Applying uncertainty to photometry...')
    oif["MaginFilter"] = PPRandomizeMeasurements.randomizePhotometry(oif, magName="MaginFilterTrue", sigName="PhotometricSigma(mag)")

    logging.info('Calculating trailing losses...')
    oif['dmagDetect']=PPTrailingLoss.PPTrailingLoss(oif, surveydb)

    logging.info('Calculating vignetting losses...')
    oif['dmagVignet']=PPVignetting.vignettingLosses(oif, surveydb)

    logging.info("Dropping faint detections... ")
    oif.drop( np.where(oif["MaginFilter"] + oif["dmagDetect"] + oif['dmagVignet'] >= oif["fiveSigmadepth"])[0], inplace=True)
    oif.reset_index(drop=True, inplace=True)

    logging.info('Calculating astrometric uncertainties...')
    oif["AstRATrue(deg)"] = oif["AstRA(deg)"]
    oif["AstDecTrue(deg)"] = oif["AstDec(deg)"]
    oif["AstRA(deg)"], oif["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(oif, sigName='AstrometricSigma(deg)')

    logging.info('Applying sensor footprint filter...')
    on_sensor=PPFootprintFilter.footPrintFilter(oif, surveydb, detectors)#, ra_name="AstRATrue(deg)", dec_name="AstDecTrue(deg)")
    oif=oif.iloc[on_sensor]

    oif=oif.astype({"FieldID": int})
    oif["Filter"] = pd.merge(oif["FieldID"], surveydb[["observationId", 'filter']], left_on="FieldID", right_on="observationId", how="left")['filter']
    oif.drop(columns=["AstrometricSigma(mas)"])

#------------------------------------------------------------------------------

    pplogger.info('Constructing output path...')
    if (outputformat == 'csv'):
        outputsuffix='.csv'
        out=outpath + outfilestem + outputsuffix
        pplogger.info('Output to CSV file...')
        pada8=PPOutWriteCSV.PPOutWriteCSV(oif,out)
    elif (outputformat == 'sqlite3'):
        outputsuffix='.db'
        out=outpath + outfilestem + outputsuffix
        pplogger.info('Output to sqlite3 database...')
        pada8=PPOutWriteSqlite3.PPOutWriteSqlite3(oif,out)
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
     t0=time.time()
     tracemalloc.start()
     run()
     _, peak = tracemalloc.get_traced_memory()
     t1=time.time()
     print("Peak memory use was %f3.3 GB, runtime was %f.3.3 minutes" %(peak / 10**9, (t1-t0)/60 ))