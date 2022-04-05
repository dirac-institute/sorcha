#!/usr/bin/python

import os,sys,time
import pandas as pd
import numpy as np
import logging
import argparse
import configparser
from surveySimPP.modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPReadColours
from surveySimPP.modules import PPJoinColourPointing, PPMatchPointing
from surveySimPP.modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency
from surveySimPP.modules import PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from surveySimPP.modules import PPReadOif, PPReadEphemerides
from surveySimPP.modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from surveySimPP.modules import PPDropObservations, PPBrightLimit
from surveySimPP.modules import PPMakeIntermediatePointingDatabase, PPReadIntermDatabase
from surveySimPP.modules import PPReadCometaryInput, PPJoinOrbitalData, PPCalculateSimpleCometaryMagnitude
from surveySimPP.modules import PPCalculateApparentMagnitude
from surveySimPP.modules.PPApplyFOVFilter import PPApplyFOVFilter
from surveySimPP.modules.PPSNRLimit import PPSNRLimit
from surveySimPP.modules import PPFootprintFilter, PPAddUncertainties, PPRandomizeMeasurements, PPVignetting
from surveySimPP.modules.PPDetectionProbability import calcDetectionProbability, PPDetectionProbability
from surveySimPP.modules.PPRunUtilities import PPGetLogger, PPConfigFileParser, PPPrintConfigsToLog, PPCMDLineParser, PPWriteOutput
from surveySimPP.modules.PPMatchPointingToObservations import PPMatchFilterToObservations, PPMatchPointingToObservations

# Author: Samuel Cornwall, Siegfried Eggl, Grigori Fedorets, Steph Merritt, Meg Schwamb

def runPostProcessing(parser):

    """
    
    Runs the post processing survey simulator functions that apply a series of filters to bias a model Solar System smallbody population to what the Vera C. Rubin Observatory Legacy Survey of Space and Time would observe. 

    Output:               csv, hdf5, or sqlite file
    
    
    """

    ### Initialise argument parser and assign command line arguments
    
    cmd_args = PPCMDLineParser(parser)

    pplogger = PPGetLogger()
    
    ### Read, assign and error-handle the configuration file
    pplogger.info('Reading configuration file...')
    
    configs = PPConfigFileParser(cmd_args['configfile'], pplogger)
   
    pplogger.info('Configuration file successfully read.')
        
    PPPrintConfigsToLog(configs, pplogger)
    
    ### End of config parsing
    
    if (cmd_args['makeIntermediatePointingDatabase'] == True):
         PPMakeIntermediatePointingDatabase.PPMakeIntermediatePointingDatabase(cmd_args['oifoutput'],'./data/interm.db', 100)
     
    pplogger.info('Reading pointing database and Matching observationID with appropriate optical filter...')
    filterpointing=PPMatchPointing.PPMatchPointing(configs['pointingdatabase'],configs['observing_filters'],configs['ppdbquery'])
    
    pplogger.info('Instantiating random number generator ... ')
    rng_seed = int(time.time())
    pplogger.info('Random number seed is {}.'.format(rng_seed))
    rng = np.random.default_rng(rng_seed)
    
    # Extracting mainfilter, the first in resfilters
    mainfilter=configs['observing_filters'][0]
    
    ### In case of a large input file, the data is read in chunks. The "sizeSerialChunk" parameter in PPConfig.ini assigns the chunk.
    
    # Here, add loop which reads only a portion of input file to avoid memory overflow
    startChunk=0
    endChunk=0
    # number of rows in an entire orbit file
    
    ii=-1
    with open(cmd_args['orbinfile']) as f:
        for ii, l in enumerate(f):
            pass
    lenf=ii
    
    while(endChunk <= lenf):
        endChunk=startChunk + configs['sizeSerialChunk'] 
        if (lenf-startChunk > configs['sizeSerialChunk']):
             incrStep=configs['sizeSerialChunk']
        else:
             incrStep=lenf-startChunk
        
        ### Processing begins, all processing is done for chunks
        
        pplogger.info('Reading input orbit file: ' + cmd_args['orbinfile'])
        padaor=PPReadOrbitFile.PPReadOrbitFile(cmd_args['orbinfile'], startChunk, incrStep, configs['filesep'])
        
        pplogger.info('Reading input colours: ' + cmd_args['colourinput'])
        padacl=PPReadColours.PPReadColours(cmd_args['colourinput'], startChunk, incrStep, configs['filesep'])
        if (configs['objecttype'] == 'comet'):
            pplogger.info('Reading cometary parameters: ' + cmd_args['cometinput'])
            padaco=PPReadCometaryInput.PPReadCometaryInput(cmd_args['cometinput'], startChunk, incrStep, configs['filesep'])
        
        objid_list = padacl['ObjID'].unique().tolist() 
       
        # write pointing history to database
        # select obj_id rows from tables 
        
        if (cmd_args['makeIntermediatePointingDatabase'] == True):
            # read from intermediate database
            padafr=PPReadIntermDatabase.PPReadIntermDatabase('./data/interm.db', objid_list)
        else:   
            try: 
                pplogger.info('Reading input pointing history: ' + cmd_args['oifoutput'])
                padafr=PPReadEphemerides.PPReadEphemerides(cmd_args['oifoutput'], configs['ephemerides_type'], configs["pointingFormat"])
                
                
                padafr=padafr[padafr['ObjID'].isin(objid_list)]

            except MemoryError:
                pplogger.error('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
                sys.exit('ERROR: insufficient memory. Try to run with -d True or reduce sizeSerialChunk.')
        
        
        pplogger.info('Checking if orbit, brightness, colour/cometary and pointing simulation input files match...')
        PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padacl,padafr)
        
        if (configs['objecttype'] == 'comet'):
            PPCheckOrbitAndColoursMatching.PPCheckOrbitAndColoursMatching(padaor,padaco,padafr)
             
        pplogger.info('Joining physical parameters and orbital data with simulation data...')       
        observations=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
        observations=PPJoinOrbitalData.PPJoinOrbitalData(observations,padaor)
        if (configs['objecttype'] == 'comet'):
            pplogger.info('Joining cometary data...')
            observations=PPJoinColourPointing.PPJoinColourPointing(observations,padaco)
        
        pplogger.info('Joining info from pointing database with simulation data and dropping observations in non-requested filters...')
        observations = PPMatchPointingToObservations(observations, filterpointing)
                
        pplogger.info('Calculating apparent magnitudes...')
        observations=PPCalculateApparentMagnitude.PPCalculateApparentMagnitude(observations, configs['phasefunction'], mainfilter, configs['othercolours'], configs['observing_filters'])

        if (configs['objecttype']=='comet'):
             pplogger.info('Calculating cometary magnitude using a simple model...')
             observations=PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude(observations, mainfilter)        
       
        pplogger.info('Dropping observations that are too bright...')
        observations=PPBrightLimit.PPBrightLimit(observations,configs['brightLimit'])
        
        ### The treatment is further divided by cameraModel: surfaceArea is a much simpler model, mimicking the fraction of the surface
        ### area not covered by chip gaps, whereas footprint takes into account the actual footprints
        
        pplogger.info('Applying field-of-view filters...')
        observations = PPApplyFOVFilter(observations, configs)

        pplogger.info('Calculating probabilities of detections...')
        observations["detection_probability"] = PPDetectionProbability(observations)
               
        pplogger.info('Calculating astrometric and photometric uncertainties...')
        observations['AstrometricSigma(mas)'], observations['PhotometricSigma(mag)'], observations["SNR"] = PPAddUncertainties.uncertainties(observations)
        observations["AstrometricSigma(deg)"] = observations['AstrometricSigma(mas)'] / 3600. / 1000.
    
        pplogger.info('Dropping observations with signal to noise ratio less than 2...')
        observations = PPSNRLimit(observations)
    
        pplogger.info('Applying uncertainty to photometry...')
        observations["MagnitudeInFilter"] = PPRandomizeMeasurements.randomizePhotometry(observations, magName="MagnitudeInFilter", sigName="PhotometricSigma(mag)", rng=rng)
        
        if (configs['trailingLossesOn'] == True):
             pplogger.info('Calculating trailing losses...')
             observations['dmagDetect']=PPTrailingLoss.PPTrailingLoss(observations)
        else:
            observations['dmagDetect']=0.0                 
             
        pplogger.info('Calculating vignetting losses...')
        observations['dmagVignet']=PPVignetting.vignettingLosses(observations)
    
        pplogger.info("Dropping faint detections... ")
        observations.drop( np.where(observations["MagnitudeInFilter"] + observations["dmagDetect"] + observations['dmagVignet'] >= observations["fiveSigmaDepth"])[0], inplace=True)
        observations.reset_index(drop=True, inplace=True)
    
        pplogger.info('Calculating astrometric uncertainties...')
        observations["AstRATrue(deg)"] = observations["AstRA(deg)"]
        observations["AstDecTrue(deg)"] = observations["AstDec(deg)"]
        observations["AstRA(deg)"], observations["AstDec(deg)"] = PPRandomizeMeasurements.randomizeAstrometry(observations, sigName='AstrometricSigma(deg)', rng=rng)
    
        pplogger.info('Dropping column with astrometric sigma in milliarcseconds ...')                    
        observations.drop(columns=["AstrometricSigma(mas)"])
        
        pplogger.info('Number of rows BEFORE applying detection probability threshold: ' + str(len(observations.index)))
    
        pplogger.info('Dropping observations below detection threshold...')
        observations=PPDropObservations.PPDropObservations(observations, "detection_probability")
        
        pplogger.info('Number of rows AFTER applying detection probability threshold: ' + str(len(observations.index)))
        
        pplogger.info('Applying SSP criterion efficiency...')

        observations=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(observations,configs['minTracklet'],configs['noTracklets'],configs['trackletInterval'],configs['inSepThreshold'])
        observations=observations.drop(['index'], axis='columns')
        
        pplogger.info('Number of rows AFTER applying SSP criterion threshold: ' + str(len(observations.index)))

		# write output
        PPWriteOutput(configs, observations, pplogger, endChunk)
                
        startChunk = startChunk + configs['sizeSerialChunk']
        # end for
    
    pplogger.info('Post processing completed.')


def main():
    """

    A post processing survey simulator that applies a series of filters to bias a model Solar System small body population to what the specified wide-field survey would observe.

    Mandatory input:      configuration file, orbit file, colour file, and optional cometary activity properties file

    Output:               csv, hdf5, or sqlite file


    usage: surveySimPP [-h] [-c C] [-d] [-m M] [-l L] [-o O] [-p P]
        optional arguments:
         -h, --help      show this help message and exit
         -c C, --config C   Input configuration file name
         -d          Make intermediate pointing database
         -m M, --comet M    Comet parameter file name
         -l L, --colour L, --color L  Colour file name
         -o O, --orbit O    Orbit file name
         -p P, --pointing P  Pointing simulation output file name
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Input configuration file name", type=str, dest='c', default='./PPConfig.ini', required=True)
    parser.add_argument("-d", help="Make intermediate pointing database", dest='d', action='store_true')
    parser.add_argument("-m", "--comet", help="Comet parameter file name", type=str, dest='m')
    parser.add_argument("-l", "--colour", "--color", help="Colour file name", type=str, dest='l', default='./data/colour', required=True)
    parser.add_argument("-o", "--orbit", help="Orbit file name", type=str, dest='o', default='./data/orbit.des', required=True)
    parser.add_argument("-p", "--pointing", help="Pointing simulation output file name", type=str, dest='p', default='./data/oiftestoutput', required=True)

    runPostProcessing(parser)

if __name__=='__main__':
    main()
    
