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
                      minintracklets: integer, minimum number of observations
                      nooftracklets: integer, number of tracklets required for linking
                      interval time: float, interval of time (in days) which should include
                                     nooftracklets to qualify for a detection.
                      inSepThresHoldAsec: float: minimum separation for SSP inside the tracklet
                                     to distinguish between two images to recognise the motion 
                                     between images

   Output:               pandas dataframe


   usage: padafr=PPFilterSSPCriterionEfficiency(padain,minintracklet,nooftracklets,intervaltime, inSepThresHoldAsec)
   """
   
   if (minintracklets<2):
       logger.error('ERROR: PPFilterSSPCriterionEfficiency: minimum number of observations in tracklet should be at least 2.')
       sys.exit('ERROR: PPFilterSSPCriterionEfficiency: minimum number of observations in tracklet should be at least 2.')
       
   if (nooftracklets<1):
       logger.error('ERROR: PPFilterSSPCriterionEfficiency: minimum number of tracklets should be at least 1.')
       sys.exit('ERROR: PPFilterSSPCriterionEfficiency: minimum number of tracklets should be at least 1.')
   
   padain.reset_index(inplace=True)
   cols=padain.columns.tolist()
   cols.append('counter')

   objid_list = padain['ObjID'].unique().tolist() 
   minno=minintracklets*nooftracklets

   padaout=pd.DataFrame(columns=cols)
   
   sepThreshold=inSepThresHoldAsec/3600.
   
   # Here one might think of parallelisation
   i=0
   while(i<len(objid_list)):
        subs=padain[padain['ObjID']==objid_list[i]]

        # The absolute minimum number of observations is two
        if len(subs.index) >= 2:
             counter=0 # of number of tracklets per object
             r=subs.index.tolist()
             padaouttrackletcoll=pd.DataFrame(columns=cols)
             
             #l=0
             #while(l < len(subs.index)):
             #    print(subs.at[l,'FieldID'], subs.at[l,'FieldMJD'])
             #    l=l+1
             j=r[0]
             k=r[0]

             # If criterion becomes satisfied, or data end:
             # first, tracklet
             padaouttracklet=pd.DataFrame()
             #subidx=subs['index'].max()
             subidx=subs.index.values.max()
             #print('subs')
             
             while(j<=r[-1]):

                  # Longest night at LSST site is around 10.8 hours
                  #if(subs.at[j+minintracklets-1,'FieldMJD']-subs.at[j,'FieldMJD'] < 11/24.):

                  #print(subs.at[j,'FieldMJD']-subs.at[k,'FieldMJD'], 11/24.)
                  s=j

                  while(subs.at[s,'FieldMJD']-subs.at[k,'FieldMJD'] < 11/24. and s<=r[-1]): #  
                       # The reason why this is done in a seemingly weird way is because
                       # for some reason the values in pandas columns get mixed up
                       # (if you just put loc[j], instead of # loc[k:j] and removing duplicates
                       # down the line)

                       padaouttracklet=padaouttracklet.append(subs.loc[k:s], sort=False) 
                       padaouttracklet['counter']=counter
                       

                       if (s==subidx):
                            break
                       #j=j+1
                       s=s+1
                  
                  #if(subs.at[j,'FieldMJD']-subs.at[k,'FieldMJD'] < 11/24.):
                  
                  #print(s, k, j)
                  #print(padaouttracklet)
                  
                  if((j-k+1)>=minintracklets and len(padaouttracklet.index.values)>1):

                       #j=j-1
                       
                       # see comment above why this is done weirdly
                       padaouttracklet=padaouttracklet.drop_duplicates(subset=['FieldID'])#.reset_index(drop=True)
                       #print(padaouttracklet[cols])
                       #padaouttracklet=padaouttracklet.append(subs.loc[j:j+minintracklets-1])#, ignore_index=True)
                       #padaouttracklet=padaouttracklet.append(subs.loc[k:j])#, ignore_index=True) 
                       #padaouttracklet['counter']=counter                      
                       # Check if observations within tracklets are not too close to each other
                       #firstCoordTracklet=SkyCoord(padaouttracklet.at[j,'AstRA(deg)']*u.degree, padaouttracklet.at[j,'AstDec(deg)']*u.degree)
                       #lastCoordTracklet=SkyCoord(padaouttracklet['AstRA(deg)'].iloc[-1]*u.degree, padaouttracklet['AstDec(deg)'].iloc[-1]*u.degree)
                       firstCoordTracklet=SkyCoord(padaouttracklet.at[k,'AstRA(deg)']*u.degree, padaouttracklet.at[k,'AstDec(deg)']*u.degree)
                       lastCoordTracklet=SkyCoord(padaouttracklet.at[j,'AstRA(deg)']*u.degree, padaouttracklet.at[j,'AstDec(deg)']*u.degree)
                                              
                       sep=firstCoordTracklet.separation(lastCoordTracklet).degree
                       if not isinstance(sep,float):
                           # sometimes, the output of astropy SkyCoord.separation is a size 2 ndarray wth identical values, and not a float
                           sep=float(sep[0])
                       #if (counter>0):
                       #    print(counter, padaouttrackletcoll.at[counter,'FieldMJD']-padaouttrackletcoll.at[0,'FieldMJD'], intervaltime)
                       #print(padaouttrackletcoll)
                       #print(j,k, j-k, minintracklets)
                       #print(padaouttracklet)
                       if (sep>sepThreshold):
                           padaouttrackletcoll=padaouttrackletcoll.append(padaouttracklet, ignore_index=True, sort=False)
                           counter=counter+1
                       #j=j+1
                       k=j

                       padaouttracklet=pd.DataFrame()
                       #else:
                       #j=j+1
                  elif ((len(padaouttracklet.index.values)<=1) and s!=j):
                       pass
                  else:
                       k=j
                       #counter=counter+1
                       padaouttracklet=pd.DataFrame()
                       #j=j+1
                  j=j+1     


                  #j=j+minintracklets
             # This is the collection of all tracklets for a single object

             padaouttrackletcoll=padaouttrackletcoll[cols]
             padaouttrackletcoll=padaouttrackletcoll.drop(['index'], axis=1)
             padaouttrackletcoll=padaouttrackletcoll.drop_duplicates(subset=['FieldID']).reset_index(drop=True)
             
             #print(padaouttrackletcoll['FieldMJD'].to_string())
             ms = pd.unique(padaouttrackletcoll['counter'])

             m=0
             g=0
             #print()
             #while(m<=counter-nooftracklets):
             while(m<=ms[-nooftracklets]):
                  if (m in padaouttrackletcoll['counter'].values):
                      #print('m: ', m, ' nooftracklets: ', nooftracklets, ' m+nooftracklets: ', m+nooftracklets)
                      flindex=padaouttrackletcoll.loc[padaouttrackletcoll['counter'] == m].head(1).index[0]
                      llindex=padaouttrackletcoll.loc[padaouttrackletcoll['counter'] == ms[g+nooftracklets-1]].tail(1).index[0]
                      #print('Indices: flindex: ', flindex, ' llindex: ', llindex)
                      #print(padaouttrackletcoll[flindex:llindex+1])
                      if (padaouttrackletcoll.at[llindex,'FieldMJD'] - padaouttrackletcoll.at[flindex,'FieldMJD'] < intervaltime):
                            #print(llindex,flindex, padaouttrackletcoll.at[llindex,'FieldMJD'] - padaouttrackletcoll.at[flindex,'FieldMJD'], intervaltime)
                            #print(padaouttrackletcoll[flindex:llindex])
                            padaout=padaout.append(padaouttrackletcoll[flindex:llindex+1], ignore_index=True, sort=False)
                      g=g+1
                  m=m+1
             #trkcntahead=0
             #trkcntbhind=0
             #while(trkcntahead<len(padaouttrackletcoll.index)):
             #    print(trkcntbhind,trkcntahead)
             #    print(padaouttrackletcoll.iloc[trkcntbhind:trkcntahead])
             #    if (padaouttrackletcoll.at[trkcntahead,'FieldMJD'] - padaouttrackletcoll.at[trkcntbhind,'FieldMJD'] > intervaltime):
             #        # output and nullify
             #        if ((trkcntahead-trkcntbhind+1>=minno) and (padaouttrackletcoll.at[trkcntahead-1,'FieldMJD'] - padaouttrackletcoll.at[trkcntbhind,'FieldMJD'] < intervaltime)):
             #            # The previous collection is ok to add to the main output
             #            padaout=padaout.append(padaouttrackletcoll.iloc[trkcntbhind:trkcntahead-1], ignore_index=True)
             #            trkcntbhind=trkcntahead
             #        else:
             #            trkcntbhind=trkcntahead
             #    trkcntahead=trkcntahead+1
             
             # (trkcntahead-trkcntbhind>=minno) and
             #if (counter >= nooftracklets):
             #          padaout=padaout.append(padaouttrackletcoll, ignore_index=True)
             

             padaout=padaout.drop_duplicates(subset=['FieldID']).reset_index(drop=True)

             # For reference, a simple criterion: 3 points in 15 days
             #while(counter==0 or j<=r[-1]-2):
             #     if(subs.at[j+2,'FieldMJD']-subs.at[j,'FieldMJD'] < 15.0):
             #          padaout=padaout.append(subs, ignore_index=True)
             #          counter=counter+1
             #     j=j+1


        i=i+1
   
   return padaout





