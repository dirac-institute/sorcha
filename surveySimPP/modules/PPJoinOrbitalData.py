#!/usr/bin/python

import pandas as pd
import os, sys
import logging

# Author: Grigori Fedorets

def PPJoinOrbitalData(padafr,padaor):

   """
   PPJoinOrbitalData.py



   Description: This task  joins the pointing pandas database with the
   orbital pandas database (including brightness H). Each database has to have same ObjID:s: NaN:s will
   be populate the fields for the missing objects.  
   

   Mandatory input:      oif pandas database and colour/cometary database

   Output:               new joined pandas dataframe


   usage: padafr1=PPJoinOrbitalData(padafr,padaor)
   """

   pplogger = logging.getLogger(__name__)

   resdf=padafr.join(padaor.set_index('!!OID'), on='ObjID')
   
   # check if there is q in the resulting database
   if 'q' not in resdf.columns:
       if ('a' not in resdf.columns or 'e' not in resdf.columns):
            pplogger.error('ERROR: PPJoinOrbitalData: unable to join cometary and orbital parameters: no a or e in input.')
            sys.exit('ERROR: PPJoinOrbitalData: unable to join cometary and orbital parameters: no a or e in input.')
       else:
           resdf['q'] = resdf['a'] * (1. - resdf['e'])
   
   return resdf