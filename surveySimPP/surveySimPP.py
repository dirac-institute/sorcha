#!/usr/bin/python

import os,sys,time
import pandas as pd
import numpy as np
import logging
import argparse
import configparser
from lsstcomet import *
from .modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPReadColours
from .modules import PPJoinColourPointing, PPMatchPointing
from .modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency
from .modules import PPReadOrbitFile, PPCheckOrbitAndColoursMatching
from .modules import PPReadOif, PPReadEphemerides
from .modules import PPDetectionProbability, PPSimpleSensorArea, PPTrailingLoss, PPMatchFieldConditions
from .modules import PPDropObservations, PPBrightLimit
from .modules import PPMakeIntermediatePointingDatabase, PPReadIntermDatabase
from .modules import PPReadCometaryInput, PPJoinOrbitalData, PPCalculateSimpleCometaryMagnitude
from .modules import PPCalculateApparentMagnitude
from .modules.PPApplyFOVFilter import PPApplyFOVFilter
from .modules.PPSNRLimit import PPSNRLimit
from .modules import PPFootprintFilter, PPAddUncertainties, PPRandomizeMeasurements, PPVignetting
from .modules.PPDetectionProbability import calcDetectionProbability, PPDetectionProbability
from .modules.PPRunUtilities import PPGetLogger, PPConfigFileParser, PPPrintConfigsToLog, PPCMDLineParser, PPWriteOutput
from .modules.PPMatchPointingToObservations import PPMatchFilterToObservations, PPMatchPointingToObservations


def runPostProcessing(parser):

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
    filterpointing=PPMatchPointing.PPMatchPointing(configs['pointingdatabase'],configs['resfilters'],configs['ppdbquery'])
    
    pplogger.info('Instantiating random number generator ... ')
    rng_seed = int(time.time())
    pplogger.info('Random number seed is {}.'.format(rng_seed))
    rng = np.random.default_rng(rng_seed)
    
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
        # The H given in the orbital DES file is omitted and erased; it is given in a separate brightness file instead
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
        observations=PPCalculateApparentMagnitude.PPCalculateApparentMagnitude(observations, configs['phasefunction'], configs['mainfilter'], configs['othercolours'], configs['resfilters'])

        if (configs['objecttype']=='comet'):
             pplogger.info('Calculating cometary magnitude using a simple model...')
             observations=PPCalculateSimpleCometaryMagnitude.PPCalculateSimpleCometaryMagnitude(observations, configs['mainfilter'])        
       
        pplogger.info('Dropping observations that are too bright...')
        observations=PPBrightLimit.PPBrightLimit(observations,configs['brightLimit'])
        
        ### The treatment is further divided by cameraModel: surfaceArea is a much simpler model, mimicking the fraction of the surface
        ### area not covered by chip gaps, whereas footprint takes into account the actual footprints
        
        pplogger.info('Applying field-of-view filters...')
        observations = PPApplyFOVFilter(observations, configs['cameraModel'], configs['footprintPath'])

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

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Input configuration file name", type=str, dest='c', default='./PPConfig.ini')
    parser.add_argument("-d", help="Make intermediate pointing database", dest='d', action='store_true')
    parser.add_argument("-m", "--comet", help="Comet parameter file name", type=str, dest='m')
    parser.add_argument("-l", "--colour", "--color", help="Colour file name", type=str, dest='l', default='./data/colour')
    parser.add_argument("-o", "--orbit", help="Orbit file name", type=str, dest='o', default='./data/orbit.des')
    parser.add_argument("-p", "--pointing", help="Pointing simulation output file name", type=str, dest='p', default='./data/oiftestoutput')

    runPostProcessing(parser)

if __name__=='__main__':
    main()
    
