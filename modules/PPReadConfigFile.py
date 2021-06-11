#!/usr/bin/python

from modules import PPConfig

# Author: Grigori Fedorets


def PPReadConfigFile():
    """
    PPReadConfigFile
   
   
   
    Description: Read config files and interrupt if there are inconsistencies.


    Mandatory input:   None; reads PPConfig
   

    Output:            None; initializes variables


    usage: PPreadConfigFile()    
    """
   
    # Files

    oifoutput=PPConfig.oifoutput
    colourinput=PPConfig.colourinput
    pointingdatabase=PPConfig.pointingdatabase
    
    # Parameter values
    SSPDetectionEfficiency=PPConfig.SSPDetectionEfficiency
    if (SSPDetectionEfficiency > 1.0 or SSPDetectionEfficiency > 1.0 or isinstance(SSPDetectionEfficiency,(float,int))==False):
        logging.error('PPreadConfigFile: ERROR: SSP detection efficiency out of bounds (should be between 0 and 1.), or not a number.')
        sys.exit()
        
    minTracklet=PPConfig.minTracklet
    if (minTracklet < 1 or isinstance(minTracklet,int)==False):
        logging.error('PPreadConfigFile: ERROR: minimum length of tracklet is zero or negative, or not an integer.')
        sys.exit()
        
    noTracklets=PPConfig.noTracklets
    if (noTracklets  < 1 or isinstance(noTracklets, int)== False):
        logging.error('PPreadConfigFile: ERROR: number of tracklets is zero or less, or not an integer.')
        sys.exit()
        
    trackletInterval=PPConfig.trackletInterval
    if (trackletInterval <= 0.0 or isinstance(trackletInterval,(float,int))==False):
        logging.error('PPreadConfigFile: ERROR: tracklet appearance interval is negative, or not a number.')
        sys.exit()
        
    testValue=PPConfig.testValue
    if (isinstance(testValue,int)==False):
        logging.error('PPreadConfigFile: ERROR: test value is not an integer.')
        sys.exit()       
    

    return testValue,oifoutput,colourinput,pointingdatabase,SSPDetectionEfficiency,minTracklet,noTracklets,trackletInterval