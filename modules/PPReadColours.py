#!/bin/python

import pandas as pd
import os, sys

# Author: Grigori Fedorets


def PPReadColours(clr_datafile, beginLoc, chunkSize):

    """
    PPReadColours.py
    
    
    Description: This task reads in the colours file and puts it into a 
    single pandas dataframe for further use downstream by other tasks.
    
    The format of the colours is:
    
    id   colour1 colour2 etc
    
    
    Mandatory input:      string, clr_datafile, name of colour data file
                          integer, beginLoc, location in file where reading begins
                          integer, chunkSize, length of chunk to be read in 
    
    Output:               pandas dataframe
    
    
    
    usage: padafr=PPReadColours(clr_datafile, beginLoc, chunkSize)
    """

    padafr=pd.read_csv(clr_datafile, sep='\s+', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    padafr=padafr.rename(columns=lambda x: x.strip())
    
    # check for nans or nulls

    if padafr.isnull().values.any():
         #inds = pd.isnull(padafr).any('ObjID').to_numpy().nonzero()[0]
         pdt=padafr[padafr.isna().any(axis=1)]
         print(pdt)
         inds=str(pdt['ObjID'].values)
         outstr="ERROR: uninitialised values when reading colour file. ObjID: " + str(inds)
         sys.exit(outstr)
    
    return padafr
