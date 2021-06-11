#!/bin/python

import pandas as pd
import os, sys
import numpy as np

# Author: Grigori Fedorets


def PPReadColours(clr_datafile, beginLoc, chunkSize, filesep):

    """
    PPReadColours.py
    
    
    Description: This task reads in the colours file and puts it into a 
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

    if (filesep==" "):
        padafr=pd.read_csv(clr_datafile, sep='\s+', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    elif (filesep==','):
        #print('Si!')
        #col_names = pd.read_csv(clr_datafile, nrows=0).columns
        #print(type(col_names))
        #col_names_ = col_names.str().split()
        #col_names_ = [item.split() for item in col_names][0]
        #print(col_names_)
        #types_dict = {'ObjID': str, mainfilter: float}
        #types_dict.update({col: float for col in col_names_ if col not in types_dict})
        #print(types_dict)
        padafr=pd.read_csv(clr_datafile, skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
        #padafr=pd.read_csv(clr_datafile, sep=',', dtype=types_dict, lineterminator='\n', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
    #print('Before')
    #print(padafr.columns)
    
    #f = open(clr_datafile, "r")
    #hdr=f.readline()
    #hdr=np.array(hdr)
    #print(hdr)
    #hdr=hdr.strip('\n')
    #hdr=hdr.split(',')
    #print(hdr)
    #padafr=padafr.rename(columns=lambda x: x.split())
    #padaf=padafr.rename(columns=hdr)
    
    #padafr=padafr.rename(columns=lambda x: x.split())
    #print(padafr.columns)
    #tmpcl=padafr.columns[0]
    #print(tmpcl)
    #padafr=padafr.rename(columns=tmpcl)  
    #padafr.columns=tmpcl
    
    #print('After')
    #print(type(padafr.columns))
    #print(padafr.columns)
    #print(padafr.columns[0])
    
    
    
    # check for nans or nulls

    if padafr.isnull().values.any():
         #inds = pd.isnull(padafr).any('ObjID').to_numpy().nonzero()[0]
         pdt=padafr[padafr.isna().any(axis=1)]
         print(pdt)
         inds=str(pdt['ObjID'].values)
         outstr="ERROR: uninitialised values when reading colour file. ObjID: " + str(inds)
         sys.exit(outstr)
    
    return padafr
