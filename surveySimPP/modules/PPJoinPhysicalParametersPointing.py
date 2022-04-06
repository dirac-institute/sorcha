#!/usr/bin/python

import pandas as pd

# Author: Grigori Fedorets

def PPJoinPhysicalParametersPointing(padafr,padacl):

   """
   PPJoinPhysicalParametersPointing.py



   Description: This task  joins the pointing pandas database with the
   physical parameters pandas database. Each database has to have same ObjID:s: NaN:s will
   be populate the fields for the missing objects.  
   

   Mandatory input:      oif pandas database and physical parameters database

   Output:               new joined pandas dataframe


   usage: padafr1=PPJoinPhysicalParametersPointing(padafr,padacl)
   """



   resdf=padafr.join(padacl.set_index('ObjID'), on='ObjID')
   return resdf
