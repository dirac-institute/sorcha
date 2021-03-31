#!/usr/bin/python

import pandas as pd
import random
import sys

# Author: Grigori Fedorets

def PPFilterDetectionEfficiencyThreshold(padain, threshold):
    """
    Task: PPFilterDetectionEfficiencyThreshold
    
    Input: padain: pandas dataframe, in objectsInField (oif) format, 
           threshold: float, between 0 and 1
    
    Action: Goes through every row in pandas dataframe and accepts/declines based on
    pre-determined acceptance threshold (between 0 and 1).
    
    Output: pandas dataframe (modified)
    
    
    """
    
    padain=padain.reset_index(drop=True)

    if (threshold > 1.0 or threshold < 0.0):
         logging.error('ERROR: PPFilterDetectionEfficiencyThreshold: threshold out of bounds.')
         sys.exit('ERROR: PPFilterDetectionEfficiencyThreshold: threshold out of bounds.')
    
    nrows=len(padain.index)
    i=0
    while(i<nrows):
         randn=random.random()
         if (randn>threshold):
             padain = padain[padain.index != i]
         i=i+1
    
    # After drooping some lines, the indices should be updated.
    padain=padain.reset_index(drop=True)    

    return padain
    
    
    
    
