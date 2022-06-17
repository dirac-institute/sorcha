#!/bin/python

import pandas as pd
import sys
import logging

# Author: Grigori Fedorets


def PPReadCometaryInput(comet_datafile, beginLoc, chunkSize, filesep):

    """
    PPReadCometaryInput.py

    Description: This task reads in the cometary data file and puts it into a
    single pandas dataframe for further use downstream by other tasks.

    The format of the colours is:

    ObjID   afrho k

    NB, the R parameter is not given explicitly, but rather calculated through
    the absolute magnitude, assuming geometric albedo pv=0.04


    Mandatory input:      string, comet_datafile, name of comet data file
                          integer, beginLoc, location in file where reading begins
                          integer, chunkSize, length of chunk to be read in
                          string, filesep, separator used in input file, blank or comma


    Output:               pandas dataframe

    usage: padafr=PPReadCometaryInput(comet_datafile, beginLoc, chunkSize)
    """
    
    pplogger = logging.getLogger(__name__)

    if (filesep == "whitespace"):
        padafr = pd.read_csv(comet_datafile, delim_whitespace=True, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)
    elif (filesep == "csv" or filesep == "comma"):
        padafr = pd.read_csv(comet_datafile, delimiter=',', skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)

    padafr = padafr.rename(columns=lambda x: x.strip())

    # check for nans or nulls

    if padafr.isnull().values.any():
        pdt = padafr[padafr.isna().any(axis=1)]
        inds = str(pdt['ObjID'].values)
        outstr = "ERROR: uninitialised values when reading comet data file. ObjID: " + str(inds)
        pplogger.error(outstr)
        sys.exit(outstr)

    padafr['ObjID'] = padafr['ObjID'].astype(str)

    return padafr
