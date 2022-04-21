#!/usr/bin/python

def PPMagnitudeLimit(observations, mag_limit):
    """
    PPMagnitudeLimit.py
    
    Author: Steph Merritt (sort of)
    
    Filter that simply performs a straight magnitude cut based on a limit.
    
    Inputs:
    --------
    observations: Pandas dataframe of simulation data merged with pointing data. Must have
    "SNR" column.
    mag_limit: Float limit for magnitude cut.
    
    Returns:
    ---------
    observations: Pandas dataframe as input but with entries under the SNR limit removed.
    
    """
    
    observations.reset_index(inplace=True)  
    observations_dropped = observations[observations['PSFMag'] < mag_limit]
    observations_dropped.reset_index(drop=True, inplace=True)
    
    return observations_dropped