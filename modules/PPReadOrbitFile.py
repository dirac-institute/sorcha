#!/usr/bin/python

import pandas as pd
import os, sys

# Author: Grigori Fedorets

def PPReadOrbitFile(orbin, beginLoc, chunkSize):


   """
   PPReadOrbitFile
   
   
   
   Description: Read orbit file, and store in a pandas dataframe. Note, that here, no
   orbit class is initialised


   Mandatory input:   string, orbin (name of input orbit file)
                      integer, beginLoc, location in file where reading begins
                      integer, chunkSize, length of chunk to be read in 
   

   Output:            pandas dataframe


   Usage: padafr=PPreadOrbitFile(orbin, beginLoc, chunkSize) 

   """

   padafr=pd.read_csv(orbin, sep='\s+', skiprows=range(1,beginLoc+1), nrows=chunkSize, header=0)
   padafr=padafr.rename(columns=lambda x: x.strip())

   # Check for nans or nulls
   
   if padafr.isnull().values.any():
         pdt=padafr[padafr.isna().any(axis=1)]
         inds=str(pdt['ObjID'].values)
         outstr="ERROR: uninitialised values when reading orbit file. ObjID: " + str(inds)
         sys.exit(outstr)
         logger.info(outstr)
   
   return padafr

   
   