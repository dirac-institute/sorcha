#!/bin/python

import pandas as pd

"""
readOif.py

Author: Grigori Fedorets

Description: This task reads in the output of oif (objectsInField) and puts it into a 
single pandas dataframe for further use downstream by other tasks.

This task should be used as the first one in the collection of subsequent tasks
called recipes.

Any other relevant data (e.g. magnitudes and colours) are read and amended to the
main pandas dataframe by separate tasks.



Mandatory input:      Output from objectsInField (oif) in text file

Output:               pandas dataframe


usage: padafr=readOif(oif_output)
"""


def readOif(oif_output):

    padafr=pd.read_csv(oif_output, sep='\s+')
    
    return padafr

    
