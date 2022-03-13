#!/usr/bin/python

import pandas as pd
import logging
import sys

# Author: Grigori Fedorets

def PPCheckOrbitAndColoursMatching(orbin,colin,poiin):


   """
   PPCheckOrbitAndColoursMatching
   
   
   
   Description: Checks whether orbit and colour files contain the same object id:s, and
               additionally checks if the pointing database object id:s is a subset of 
               all the object id:s found in the orbit/physical parameter files.


   Mandatory input:   pandas dataframe: orbin -- orbits
                      pandas dataframe: colin -- colours/cometary parameters
                      pandas dataframe: poiin -- pointing database
   

   Output:            None; return if there is a match, throw error and quit if mismatch.
                      


   Usage: PPCheckOrbitAndColoursMatching(orbin,colin,poiin)

   """
   poi=pd.unique(poiin['ObjID'])
   poiobjs=pd.Series(poi, dtype=object)
   
   orbin = orbin.astype({'!!OID': object})
   colin = colin.astype({'ObjID': object})
   

   if orbin['!!OID'].equals(colin['ObjID']):
        if poiobjs.isin(orbin['!!OID']).all():
            return
        else:
            logging.error('ERROR: PPCheckOrbitAndColourMatching: input pointing and orbit files do not match.')
            sys.exit('ERROR: PPCheckOrbitAndColourMatching: input pointing and orbit files do not match.')
   else:
      logging.error('ERROR: PPCheckOrbitAndColourMatching: input colour/cometary parameter and orbit files do not match.')
      sys.exit('ERROR: PPCheckOrbitAndColourMatching: input colour/cometary parameter and orbit files do not match.')
