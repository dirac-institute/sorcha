#!/usr/bin/python

import pandas as pd

# Author: Grigori Fedorets

def PPFilterSSPCriterionEfficiency(padain,minintracklets,nooftracklets,intervaltime):
   """
   PPFilterSSPCriterionEfficiency.py
   
   
   
   Description: This task reads in the modified pandas dataframe
   (including colours), checks against the SSP detection criterion
   (three detections over 15 nights), and outputs only the objects
   that satisfy that criterion.

   Generally, to be applied after detection threshold.


   Mandatory input:   padain: modified pandas dataframe
                      minintracklet: integer, minimum number of observations
                      nooftracklets: integer, number of tracklets required for linking
                      interval time: float, interval of time (in days) which should include
                                     nooftracklets to qualify for a detection.

   Output:               pandas dataframe


   usage: padafr=PPFilterSSPCriterionEfficiency(padain,minintracklet,nooftracklets,intervaltime)
   """


   objid_list = padain['ObjID'].unique().tolist() 
    
   padaout=pd.DataFrame()
   
   # Here one might think of parallelisation
   i=0
   while(i<len(objid_list)):
        subs=padain[padain['ObjID']==objid_list[i]]
        # The absolute minimum number of observations is two
        if len(subs.index) > 2:
             counter=0
             r=subs.index.tolist()
             padaouttracklet=pd.DataFrame()

             j=r[0]
             # If criterion becomes satisfied, or data end:
             # first, tracklet
             while(counter==0 or j<=r[-1]-minintracklets):
                  # Longest night at LSST site is around 10.8 hours
                  if(subs.at[j+minintracklets,'FieldMJD']-subs.at[j,'FieldMJD'] < 11/24.):
                       padaouttracklet=padaouttracklet.append(subs, ignore_index=True)
                       counter=counter+1
                  j=j+1
             if (counter >= nooftracklets):
                       padaout=padaout.append(padaouttracklet, ignore_index=True)

             # For reference, a simple criterion: 3 points in 15 days
             #while(counter==0 or j<=r[-1]-2):
             #     if(subs.at[j+2,'FieldMJD']-subs.at[j,'FieldMJD'] < 15.0):
             #          padaout=padaout.append(subs, ignore_index=True)
             #          counter=counter+1
             #     j=j+1


        i=i+1
   
   return padaout





