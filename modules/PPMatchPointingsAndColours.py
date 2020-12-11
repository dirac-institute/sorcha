#!/usr/bin/python


import pandas as pd
import numpy as np
import random

"""
PPMatchPointingsAndColours.py

Author: Grigori Fedorets

Description: This task takes two pandas dataframes: one is output that includes all 
relevant colours, the other is a two-column database that includes all the fieldId:s
and the filters at the given pointing.

The task cross-matches the two databases, matches the pre-calculated colour in each 
pointing with the relevant filter. Then it leaves only the relevant colour and the
filter, and erases all the obsolete colours.

Mandatory input:      Output from objectsInField (oif) with additional relevant colour
                      columns (pandas dataframes)
                      pointing and filter dataframe (pandas dataframe)

Output:               pandas dataframe


usage: padafr=PPMatchPointingsAndColours(padain,pointfildb)
"""


def PPMatchPointingsAndColours(padain,pointfildb):
    
    possible_colours=pd.Series(['u','g','r','i','z','y'])
    

    resdf=padain.join(pointfildb.set_index('FieldID'), on='FieldID')
    
    for colour in possible_colours:
         if colour not in resdf:
              resdf[colour]=np.nan
        
    
    #resdf['ColinFil']=resdf.optFilter.isin(resdf.columns) # on track, gives true to correct values
    resdf['ColinFil']=resdf.lookup(resdf.index,resdf['optFilter']) 

    # Do some cleaning
    resdf.drop(['u','g','r','i','z','y'], axis=1, inplace=True)
    

    
    return resdf

        
