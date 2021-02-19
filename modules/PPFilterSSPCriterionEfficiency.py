#!/usr/bin/python

import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

# Author: Grigori Fedorets

def PPFilterSSPCriterionEfficiency(padain,minintracklets,nooftracklets,intervaltime,inSepThresHoldAsec):
   """
   PPFilterSSPCriterionEfficiency.py
   
   
   
   Description: This task reads in the modified pandas dataframe
   (including colours), checks if coordinates within tracklets are far enough 
   to be separated by SSP, checks against the SSP detection criterion
   (_nooftracklets_ detections over _intervaltime_ nights), and outputs only the objects
   that satisfy that criterion.

   Generally, to be applied after detection threshold.


   Mandatory input:   padain: modified pandas dataframe
                      minintracklet: integer, minimum number of observations
                      nooftracklets: integer, number of tracklets required for linking
                      interval time: float, interval of time (in days) which should include
                                     nooftracklets to qualify for a detection.
                      inSepThresHoldAsec: float: minimum separation for SSP inside the tracklet
                                     to distinguish between two images to recognise the motion 
                                     between images

   Output:               pandas dataframe


   usage: padafr=PPFilterSSPCriterionEfficiency(padain,minintracklet,nooftracklets,intervaltime, inSepThresHoldAsec)
   """


   objid_list = padain['ObjID'].unique().tolist() 
    
   padaout=pd.DataFrame()
   
   sepThreshold=inSepThresHoldAsec/3600.
   
   # Here one might think of parallelisation
   i=0
   while(i<len(objid_list)):
        subs=padain[padain['ObjID']==objid_list[i]]
        # The absolute minimum number of observations is two
        if len(subs.index) >= 2:
             counter=0 # of number of tracklets per object
             r=subs.index.tolist()
             padaouttracklet=pd.DataFrame()
             padaouttrackletcoll=pd.DataFrame()

             j=r[0]
             # If criterion becomes satisfied, or data end:
             # first, tracklet
             while(j<=r[-1]-minintracklets+1):
                  # Longest night at LSST site is around 10.8 hours
                  if(subs.at[j+minintracklets-1,'FieldMJD']-subs.at[j,'FieldMJD'] < 11/24.):
                       padaouttracklet=padaouttracklet.append(subs.loc[j:j+minintracklets-1])#, ignore_index=True)
                       # Check if observations within tracklets are not too close to each other
                       firstCoordTracklet=SkyCoord(padaouttracklet.at[j,'AstRA(deg)']*u.degree, padaouttracklet.at[j,'AstDec(deg)']*u.degree)
                       lastCoordTracklet=SkyCoord(padaouttracklet['AstRA(deg)'].iloc[-1]*u.degree, padaouttracklet['AstDec(deg)'].iloc[-1]*u.degree)
                       sep=firstCoordTracklet.separation(lastCoordTracklet).degree
                       if (sep>sepThreshold):
                           padaouttrackletcoll=padaouttrackletcoll.append(padaouttracklet)
                           counter=counter+1
                  j=j+1

             if (counter >= nooftracklets):
                       padaout=padaout.append(padaouttrackletcoll, ignore_index=True)

             # For reference, a simple criterion: 3 points in 15 days
             #while(counter==0 or j<=r[-1]-2):
             #     if(subs.at[j+2,'FieldMJD']-subs.at[j,'FieldMJD'] < 15.0):
             #          padaout=padaout.append(subs, ignore_index=True)
             #          counter=counter+1
             #     j=j+1


        i=i+1
   
   return padaout





