#!/usr/bin/python

import pandas as pd
import sys
import logging

# Author: Grigori Fedorets


def PPReadOrbitFile(orbin, beginLoc, chunkSize, filesep):
    """
    PPReadOrbitFile

    Description: Read orbit file, and store in a pandas dataframe. Note, that here, no
    orbit class is initialised


    Mandatory input:   string, orbin (name of input orbit file)
                      integer, beginLoc, location in file where reading begins
                      integer, chunkSize, length of chunk to be read in
                      string, filesep, separator used in input file, whitespace or csv


    Output:            pandas dataframe


    Usage: padafr=PPreadOrbitFile(orbin, beginLoc, chunkSize, filesep)

    """

    pplogger = logging.getLogger(__name__)

    if (filesep == "whitespace"):
        padafr = pd.read_csv(orbin, delim_whitespace=True, skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)
    elif (filesep == "csv" or filesep == "comma"):
        padafr = pd.read_csv(orbin, delimiter=',', skiprows=range(1, beginLoc + 1), nrows=chunkSize, header=0)

    padafr = padafr.rename(columns=lambda x: x.strip())
    # rename i to incl to avoid confusion with the colour i
    padafr = padafr.rename(columns={"i": "incl"})

    # Check for nans or nulls

    if padafr.isnull().values.any():
        pdt = padafr[padafr.isna().any(axis=1)]
        inds = str(pdt['ObjID'].values)
        outstr = "ERROR: uninitialised values when reading orbit file. ObjID: " + str(inds)
        sys.exit(outstr)
        pplogger.info(outstr)

    padafr = padafr.drop(['INDEX', 'N_PAR', 'MOID', 'COMPCODE'], axis=1, errors='ignore')
    padafr['ObjID'] = padafr['ObjID'].astype(str)

    return padafr
