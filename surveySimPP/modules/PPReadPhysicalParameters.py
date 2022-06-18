#!/bin/python

import pandas as pd
import sys
import logging

# Author: Grigori Fedorets


def PPReadPhysicalParameters(clr_datafile, othercolours, beginLoc, chunkSize, filesep):
    """
    PPReadPhysicalParameters.py


    Description: This task reads in the physical parameters file and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    The format of the colours is:

    id   colour1 colour2 etc


    Mandatory input:      string, clr_datafile, name of colour data file
                          integer, beginLoc, location in file where reading begins
                          integer, chunkSize, length of chunk to be read in
                          string, filesep, separator used in input file, blank or comma

    Output:               pandas dataframe



    usage: padafr=PPReadColours(clr_datafile, beginLoc, chunkSize,filesep)
    """

    pplogger = logging.getLogger(__name__)

    if (filesep == "whitespace"):
        padafr = pd.read_csv(clr_datafile, delim_whitespace=True, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)
    elif (filesep == "comma" or filesep == "csv"):
        padafr=pd.read_csv(clr_datafile, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)
        
    # check that the columns match up with the othercolours calculated from observing_filters config variable
    if not all(colour in padafr.columns for colour in othercolours):
        pplogger.error('ERROR: colour offset columns in physical parameters file do not match with observing filters specified in config file.')
        sys.exit('ERROR: colour offset columns in physical parameters file do not match with observing filters specified in config file.')
        
    # check for nans or nulls

    if padafr.isnull().values.any():
         pdt = padafr[padafr.isna().any(axis=1)]
         print(pdt)
         inds = str(pdt['ObjID'].values)
         outstr = "ERROR: uninitialised values when reading colour file. ObjID: " + str(inds)
         pplogger.error(outstr)
         sys.exit(outstr)

    padafr['ObjID'] = padafr['ObjID'].astype(str)

    return padafr
