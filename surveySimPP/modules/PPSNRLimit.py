#!/usr/bin/python

import numpy as np

def PPSNRLimit(observations, sigma_limit=2.):
    """
    PPSNRLimit.py
    
    Author: Steph Merritt (sort of)
    
    Filter that simply performs a straight SNR cut based on a limit. Currently hardcoded
    to 2, but an option can be added in the config file for the user to specify this in
    the future.
    
    Inputs:
    --------
    observations: Pandas dataframe of simulation data merged with pointing data. Must have
    "SNR" column.
    sigma_limit: Float limit for SNR cut, default 2.0.
    
    Returns:
    ---------
    observations: Pandas dataframe as input but with entries under the SNR limit removed.
    
    """

    observations.drop( np.where(observations["SNR"] <= sigma_limit)[0], inplace=True)
    observations.reset_index(drop=True, inplace=True)
    
    return observations