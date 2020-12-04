#!/usr/bin/python

import pandas as pd

"""
PPJoinColourPointing.py

Author: Grigori Fedorets

Description: This task  joins the pointing pandas database with the
colour pandas database. Each database has to have same ObjID:s: NaN:s will
be populate the fields for the missing objects.  


Mandatory input:      oif pandas database and colour database

Output:               new joined pandas dataframe


usage: padafr1=PPJoinColourPointing(padafr,padacl)
"""

def PPJoinColourPointing(padafr,padacl):

   resdf=padafr.join(padacl.set_index('ObjID'), on='ObjID')
   return resdf
