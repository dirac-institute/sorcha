#!/usr/bin/python


import pandas as pd
import numpy as np
import random
import logging
import os, sys

# Author: Grigori Fedorets


def PPMatchPointingsAndColours(padain,pointfildb):
    """
    PPMatchPointingsAndColours.py



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


    resdf=padain.join(pointfildb.set_index('FieldID'), on='FieldID')
            
    colour_values=resdf.optFilter.unique()
    colour_values=pd.Series(colour_values).dropna()
        
    resdf=resdf.dropna(subset=['optFilter']).reset_index(drop=True)
    resdf['TrailedSourceMag'] = resdf.melt(id_vars='optFilter', value_vars=colour_values, ignore_index=False).query('optFilter == variable').loc[resdf.index, 'value']
    # Check if observation dates in joined dataframes match
    
    chktruemjd=np.isclose(resdf['observationStartMJD'], resdf['FieldMJD'])
    chktrueid=np.isclose(resdf['observationId_'], resdf['FieldID'])
    
    if not chktruemjd.all():
           logging.error('ERROR: PPMatchPointingsAndColours: mismatch in pointing database and pointing output times.')
           sys.exit('ERROR: PPMatchPointingsAndColours: mismatch in pointing database and pointing output times.')

    if not chktrueid.all():
           logging.error('ERROR: PPMatchPointingsAndColours: mismatch in pointing database and pointing output id:s.')
           sys.exit('ERROR: PPMatchPointingsAndColours: mismatch in pointing database and pointing output id:s.')
    

    resdf=resdf.drop(columns='observationId_')

    return resdf

        
