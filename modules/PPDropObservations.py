import numpy as np
import pandas as pd

__all__=['PPDropObservations']

def PPDropObservations(observations, probability):
    """
    Drops rows where the probabilty of detection is less than sample drawn
    from a uniform distribution.

    Input
    -----
    observations ... pandas dataframe of observations with a column containing the probability of detection
    probability  ... name of the column containing the probability of detection

    Returns
    -------
    dropped      ... observations that were droppped
    """

    num_obs = len(observations.index)
    chance  = np.random.random(num_obs)
    
    drop = np.where(probability < chance)[0]
    observations.drop(drop, inplace=True)
    observations.reset_index(drop=True, inplace=True)
    
    #return observations.iloc[drop]