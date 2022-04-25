import numpy as np
import pandas as pd
import time

__all__=['PPDropObservations']

default_rng = np.random.default_rng(int(time.time()))

def PPDropObservations(observations, probability="detection probability", rng=default_rng):
    """
    Drops rows where the probabilty of detection is less than sample drawn
    from a uniform distribution.

    Input
    -----
    observations ... pandas dataframe of observations with a column containing the probability of detection
    probability  ... name of the column containing the probability of detection
    rng          ... Numpy random number generator. If not defined, uses default seeded with system time.

    Returns
    -------
    out ... new dataframe without observations that could not be observed
    """

    num_obs = len(observations.index)

    uniform_distr = rng.random(num_obs)
    drop = observations.loc[observations[probability] - uniform_distr < 0].index
    out = observations.drop(drop)

    return out