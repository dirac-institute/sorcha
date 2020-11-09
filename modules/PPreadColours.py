#!/bin/python

import pandas as pd

"""
PPreadColours.py

Author: Grigori Fedorets

Description: This task reads in the colours file and puts it into a 
single pandas dataframe for further use downstream by other tasks.

The format of the colours is:

id   colour1 colour2 etc


Mandatory input:      Output from colour file in text file

Output:               pandas dataframe


usage: padafr=PPreadColours(clr_datafile)
"""


def PPreadColours(clr_datafile):

    padafr=pd.read_csv(clr_datafile, sep='\s+')
    
    return padafr
