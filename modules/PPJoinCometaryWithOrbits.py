#!/usr/bin/python

import pandas as pd
import os, sys

# Author: Grigori Fedorets

def PPJoinCometaryWithOrbits(padafr,padaor):

   """
   PPJoinCometaryWithOrbits.py



   Description: This task  joins the pointing pandas database with the
   colour/cometary pandas database. Each database has to have same ObjID:s: NaN:s will
   be populate the fields for the missing objects.  
   

   Mandatory input:      oif pandas database and colour/cometary database

   Output:               new joined pandas dataframe


   usage: padafr1=PPPJoinCometaryWithOrbits(padafr,padaor)
   """



   resdf=padafr.join(padaor.set_index('!!OID'), on='ObjID')
   
   # check if there is q in the resulting database
   if 'q' not in resdf.columns:
       if ('a' not in resdf.columns or 'e' not in resdf.columns):
            pplogger.error('ERROR: PPJoinCometaryWithOrbits: unable to join cometary and orbital parameters: no a or e in input.')
            sys.exit('ERROR: PPJoinCometaryWithOrbits: unable to join cometary and orbital parameters: no a or e in input.')
       else:
           resdf['q'] = resdf['a'] * (1. - resdf['e'])
   
   return resdf