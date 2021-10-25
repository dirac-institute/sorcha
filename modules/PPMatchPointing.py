#!/usr/bin/python
import sqlite3
import pandas as pd

#Author: Grigori Fedorets

def PPMatchPointing(bsdbname,resfilters):

    """
    PPMatchPointing.py



    Description: This task reads in the main baseline database, and extracts observationID,
    observationsStartMJD, used filter and three seeing parameters at a given pointing and outputs a 6*n pandas dataframe. 


    Mandatory input:      bsdbname:   name of database
                          resfilters: filters required for output

    Output:               8*n pandas dataframe


    usage: padafr=PPMatchPointing(bsdbname,resfilters)
    """



    con = sqlite3.connect(bsdbname)
    df = pd.read_sql_query('SELECT observationId, observationStartMJD, filter, seeingFwhmGeom, seeingFwhmEff, fiveSigmaDepth, fieldRA, fieldDec FROM SummaryAllProps order by observationId', con)
    df=df.rename(columns={'observationId': 'FieldID'})
    df=df.rename(columns={'filter': 'optFilter'}) # not to confuse with the pandas filter command   
    #print(df)
    dfo=df[df.optFilter.isin(resfilters)]
    #print(dfo)
    return dfo
    