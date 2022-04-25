#!/usr/bin/python

import pandas as pd
import sys
import logging
import numpy as np
import time

# Author: Grigori Fedorets

default_rng = np.random.default_rng(int(time.time()))

def PPDetectionEfficiency(padain, threshold, rng=default_rng):
    """
    Task: PPDetectionEfficiency
    
    Input: padain: pandas dataframe, in objectsInField (oif) format, 
           threshold: float, between 0 and 1
           rng: Numpy random number generator. If not specified, will use default seeded with system time.
    
    Action: Goes through every row in pandas dataframe and accepts/declines based on
    pre-determined acceptance threshold (between 0 and 1).
    
    Output: pandas dataframe (modified)
    
    
    """
    
    pplogger = logging.getLogger(__name__)
    
    padain=padain.reset_index(drop=True)

    if (threshold > 1.0 or threshold < 0.0):
         pplogger.error('ERROR: PPDetectionEfficiency: threshold out of bounds.')
         sys.exit('ERROR: PPDetectionEfficiency: threshold out of bounds.')
         
    num_obs = len(padain.index)

    uniform_distr = rng.random(num_obs)
    
    padain_drop = padain.drop(padain[uniform_distr > threshold].index)
    
    #nrows=len(padain.index)
    #i=0
    #while(i<nrows):
    #     randn=random.random()
    #     if (randn>threshold):
    #         padain = padain[padain.index != i]
    #     i=i+1
    
    # After dropping some lines, the indices should be updated.
    padain_drop=padain_drop.reset_index(drop=True)    

    return padain_drop
    
    
    
    
