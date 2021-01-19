#!/usr/bin/python
import sqlite3
import pandas as pd


# Author: Grigori Fedorets

def PPMatchPointing(bsdbname):

    """
        
    Description: This task reads in the main baseline database, and extracts observationID
    and used filter at a given pointing and outputs a 2*n pandas dataframe.
    
    
    Mandatory input:      name of database
    
    Output:               2*n pandas dataframe
    
    
    usage: padafr=PPMatchPointing(bsdbname)
    """

    con = sqlite3.connect(bsdbname)
    df = pd.read_sql_query('SELECT observationId, filter FROM SummaryAllProps order by observationId', con)
    df=df.rename(columns={'observationId': 'FieldID'})
    df=df.rename(columns={'filter': 'optFilter'}) # not to confuse with the pandas filter command   
    return df
    
