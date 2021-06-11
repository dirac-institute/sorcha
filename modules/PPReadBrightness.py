#!/bin/python

import pandas as pd
import os, sys

# Author: Grigori Fedorets


def PPReadBrightness(br_datafile, beginLoc, chunkSize,filesep):

    """
    PPReadBrightness.py
    
    
    Description: This task reads in the brightness file and puts it into a 
    single pandas dataframe for further use downstream by other tasks.
    
    The format of the colours is one of the following:
    
    ObjID H G
    ObjID H G1 G2
    ObjID H G12
    ObjID H S
    
    
    
    
    
    Mandatory input:      string, br_datafile, name of brightn data file
                          integer, beginLoc, location in file where reading begins
                          integer, chunkSize, length of chunk to be read in 
                          string, filesep, separator used in input file, blank or comma
    
    Output:               pandas dataframe
    
    
    
    usage: padafr=PPReadBrightness(br_datafile, beginLoc, chunkSize,filesep)
    """
    
    if (filesep==" "):
        padafr=pd.read_csv(br_datafile, sep='\s+', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    elif (filesep==","):
        padafr=pd.read_csv(br_datafile, delimiter=',', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    padafr=padafr.rename(columns=lambda x: x.strip())
    
    # check for nans or nulls

    if padafr.isnull().values.any():
         #inds = pd.isnull(padafr).any('ObjID').to_numpy().nonzero()[0]
         pdt=padafr[padafr.isna().any(axis=1)]
         print(pdt)
         inds=str(pdt['ObjID'].values)
         outstr="ERROR: uninitialised values when reading brightness file. ObjID: " + str(inds)
         sys.exit(outstr)
    
    return padafr
