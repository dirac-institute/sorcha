#!/usr/bin/python

import pandas as pd

#Author: Grigori Fedorets

def PPFilterSSPCriterionEfficiency(padain):
    """
    PPFilterSSPCriterionEfficiency.py
    
    
    Description: This task reads in the modified pandas dataframe
    (including colours), checks against the SSP detection criterion
    (three detections over 15 nights), and outputs only the objects
    that satisfy that criterion.
    
    Generally, to be applied after detection threshold.
    
    
    Mandatory input:      modified pandas dataframe
    
    Output:               pandas dataframe
    
    
    usage: pa
    """

    objid_list = padain['ObjID'].unique().tolist() 
    
    padaout=pd.DataFrame()

    # Here one might think of parallelisation
    i=0
    while(i<len(objid_list)):
        subs=padain[padain['ObjID']==objid_list[i]]
        if len(subs.index) > 2:
             counter=0
             r=subs.index.tolist()

             j=r[0]
             # If criterion becomes satisfied, or data end:
             while(counter==0 or j<=r[-1]-2):
                  if(subs.at[j+2,'FieldMJD']-subs.at[j,'FieldMJD'] < 15.0):
                       padaout=padaout.append(subs, ignore_index=True)
                       counter=counter+1
                  j=j+1
        i=i+1
    return padaout





