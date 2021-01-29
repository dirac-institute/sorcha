#!/usr/bin/python

import pandas as pd
import logging
import sys

# Author: Grigori Fedorets

def PPCheckOrbitAndColoursMatching(orbin,colin):


   """
   PPCheckOrbitAndColoursMatching
   
   
   
   Description: Read orbit file, and store in a pandas dataframe. Note, that here, no
   orbit class is initialised


   Mandatory input:   pandas dataframe: orbin -- orbits
                      pandas dataframe: colin -- colours
   

   Output:            None; return if there is a match, throw error and quit if mismatch.
                      


   Usage: PPCheckOrbitAndColoursMatching(orbin,colin)

   """

   if orbin['!!OID'].equals(colin['ObjID']):
        return
   else:
      logging.error('ERROR: PPCheckOrbitAndColourMatching: input colour and orbit files do not match.')
      sys.exit('ERROR: PPCheckOrbitAndColourMatching: input colour and orbit files do not match.')
