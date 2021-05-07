#!/bin/python

import pandas as pd
import os, sys

# Author: Grigori Fedorets


def PPReadCometaryInput(comet_datafile, beginLoc, chunkSize):

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
    
    Output:               pandas dataframe
    
    
    
    usage: padafr=PPReadCometaryInput(comet_datafile, beginLoc, chunkSize)
    """

    padafr=pd.read_csv(comet_datafile, sep='\s+', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    padafr=padafr.rename(columns=lambda x: x.strip())
    
    # check for nans or nulls

    if padafr.isnull().values.any():
         #inds = pd.isnull(padafr).any('ObjID').to_numpy().nonzero()[0]
         pdt=padafr[padafr.isna().any(axis=1)]
         print(pdt)
         inds=str(pdt['ObjID'].values)
         outstr="ERROR: uninitialised values when reading comet data file. ObjID: " + str(inds)
         sys.exit(outstr)
    
    return padafr
