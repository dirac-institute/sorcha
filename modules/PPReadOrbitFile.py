#!/usr/bin/python

import pandas as pd

# Author: Grigori Fedorets

def PPReadOrbitFile(orbin):


   """
   PPReadOrbitFile
   
   
   
   Description: Read orbit file, and store in a pandas dataframe. Note, that here, no
   orbit class is initialised


   Mandatory input:   string, orbin (name of input orbit file)
   

   Output:            pandas dataframe


   Usage: padafr=PPreadOrbitFile(orbin) 

   """
   
   padafr=pd.read_csv(orbin, sep='\s+')
    
   return padafr

   
   