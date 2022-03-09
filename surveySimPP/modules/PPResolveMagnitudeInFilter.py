#!/usr/bin/python

import pandas as pd
import numpy as np

# Author: Grigori Fedorets, Meg Schwamb


def PPResolveMagnitudeInFilter(padain,mainfilter,othercolours,resfilters):
    """
    PPResolveMagnitudeInFilter.py
    
    Description: This tasks selects a colour offset relevant to each filter at each given pointing
    and calculates the colour in each given filter. The apparent magnitude has already been
    calculated in the main filter.
    
    
    Mandatory input: string, padain, name of input pandas dataframe
                     string, mainfilter, name of the main filter in which the apparent magnitude has been calculated
                     array of strings, othercolours, names of colour offsets (e.g. r-i)
                     array of strings, resfilters, names of resulting colours, main filter is the first one, followed 
                     in order by resolved colours, such as, e.g. 'r'+'g-r'='g'. They should be given in the following order: 
                     main filter, resolved filters in the same order as respective other colours.
    
    Output: updated padain
    
    Usage: padaout=PPResolveMagnitudeInFilter(padain,mainfilter,othercolours,resfilters)
    
    """
    
    apparent_mag=np.zeros(len(padain), dtype=float)
    
    i=0
    while(i<len(resfilters)):
        inRelevantFilterList=(padain['optFilter']==resfilters[i])
        inRelevantFilter=padain[inRelevantFilterList]
        if(len(inRelevantFilter)>0):
            if(resfilters[i]==mainfilter):
               apparent_mag[inRelevantFilterList]=0.0
            else:
               apparent_mag[inRelevantFilterList]=inRelevantFilter[othercolours[i-1]]
        i=i+1
    padain['apparent_mag']=apparent_mag
    padain['MagnitudeInFilter'] = padain[mainfilter] + padain['apparent_mag']
    
    padain=padain.drop(['apparent_mag'], axis=1, errors='ignore')
      
    return padain 

