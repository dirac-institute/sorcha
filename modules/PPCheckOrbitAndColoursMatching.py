#!/usr/bin/python

import pandas as pd
import logging
import sys

# Author: Grigori Fedorets

def PPCheckOrbitAndColoursMatching(orbin,colin,poiin):


   """
   PPCheckOrbitAndColoursMatching
   
   
   
   Description: Read orbit file, and store in a pandas dataframe. Note, that here, no
   orbit class is initialised


   Mandatory input:   pandas dataframe: orbin -- orbits
                      pandas dataframe: colin -- colours
                      pandas dataframe: poiin -- pointing database
   

   Output:            None; return if there is a match, throw error and quit if mismatch.
                      


   Usage: PPCheckOrbitAndColoursMatching(orbin,colin,poiin)

   """
   poi=pd.unique(poiin['ObjID'])
   poiobjs=pd.Series(poi, dtype=object)
   
   orbin = orbin.astype({'!!OID': object})
   colin = colin.astype({'ObjID': object})
   
   
   if orbin['!!OID'].equals(colin['ObjID']):
        if orbin['!!OID'].equals(poiobjs):
            return
        else:
            logging.error('ERROR: PPCheckOrbitAndColourMatching: input pointing and orbit files do not match.')
            sys.exit('ERROR: PPCheckOrbitAndColourMatching: input pointing and orbit files do not match.')
   else:
      logging.error('ERROR: PPCheckOrbitAndColourMatching: input colour and orbit files do not match.')
      sys.exit('ERROR: PPCheckOrbitAndColourMatching: input colour and orbit files do not match.')
