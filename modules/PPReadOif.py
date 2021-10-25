#!/bin/python

import pandas as pd

#Author: Grigori Fedorets

def PPReadOif(oif_output, filesep, suffix):
   """
   PPReadOif.py



   Description: This task reads in the output of oif (objectsInField) and puts it into a 
   single pandas dataframe for further use downstream by other tasks.

   This task should be used as the first one in the collection of subsequent tasks
   called recipes.

   Any other relevant data (e.g. magnitudes and colours) are read and amended to the
   main pandas dataframe by separate tasks.



   Mandatory input:      string, oif_output, name of text file including Output from objectsInField (oif) 
                         string, filesep, separator used in input file, blank or comma
                         string, suffix, file extension of input file, either csv, txt or h5 (hdf5, HDF5)

   

   Output:               pandas dataframe


   usage: padafr=PPReadOif(oif_output,filesep)
   """

   if (filesep==" ") and ((suffix=='csv') or (suffix=='txt')):
       padafr=pd.read_csv(oif_output, sep='\s+')
   elif (filesep==",")  and ((suffix=='csv') or (suffix=='txt')):
       padafr=pd.read_csv(oif_output, delimiter=',')   
   elif (suffix=='h5') or (suffix=='hdf5') or (suffix=='HDF5'):
       padafr=pd.read_hdf(oif_output).reset_index(drop=True)
  

   padafr=padafr.rename(columns=lambda x: x.strip())
    
   return padafr

    
