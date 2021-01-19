#!/usr/bin/python

import os,sys
import pandas as pd
import logging
#from filtering import PPFilterDetectionEfficiencyThreshold
from modules import PPFilterDetectionEfficiencyThreshold, PPreadColoursUser, PPreadColours
from modules import PPhookBrightnessWithColour, PPJoinColourPointing, PPMatchPointing 
from modules import PPMatchPointingsAndColours, PPFilterSSPCriterionEfficiency
from modules import PPOutWriteCSV
from modules import readOif, PPConfig, PPReadConfigFile



#oifoutput=sys.argv[1]

# Configurate logging settings
#PPConfig.verbosity=PPConfig.verbosity*10
#logging.basicConfig(filename=PPConfig.logloc, encoding='utf-8', level=PPConfig.verbosity)

# Read config file

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
    9. outputs to a csv fileq]
    
    
    Mandatory input:      orbit file and colour file (designated in the config file)
                          The parameters are defined in the config file (./modules/PPConfig.py) 
    
    Output:               csv datafile
    
    
    usage: [from command line] python sample_recipe.py
    
    """
    
    logging.info('Reading configuration file...')
    testvalue,oifoutput,colourinput,pointingdatabase,SSPDetectionEfficiency, \
    minTracklet,noTracklets,trackletInterval \
    =PPReadConfigFile.PPReadConfigFile()
    

    
    logging.info('Reading input pointing history: ', oifoutput)
    padafr=readOif.readOif(oifoutput)
    
    logging.info('Reading input colours: ', colourinput)
    padacl=PPreadColours.PPreadColours(colourinput)
    
    logging.info('Joining colour data with pointing data...')
    resdf=PPJoinColourPointing.PPJoinColourPointing(padafr,padacl)
    
    logging.info('Applying detection efficiency threshold...')
    pada1=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(padafr,SSPDetectionEfficiency)
    
    
    
    logging.info('Hooking colour and brightness information...')
    resdf1=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf, 'V', 'i-r', 'i')
    resdf3=PPhookBrightnessWithColour.PPhookBrightnessWithColour(resdf1, 'V', 'g-X', 'g')
    
    
    logging.info('Matching observationID with appropriate optical filter...')
    pada5=PPMatchPointing.PPMatchPointing(pointingdatabase)
    
    logging.info('Resolving the apparent brightness in a given optical filter corresponding to the pointing...')
    pada6=PPMatchPointingsAndColours.PPMatchPointingsAndColours(resdf3,pada5)
    

    logging.info('Output to CSV file...')
    pada7=PPFilterSSPCriterionEfficiency.PPFilterSSPCriterionEfficiency(pada6,1,1,15.0)
    pada8=PPOutWriteCSV.PPOutWriteCSV(pada6,'out.csv')
    
    logging.info('Post processing completed.')

if __name__=='__main__':
     runPostProcessing()
