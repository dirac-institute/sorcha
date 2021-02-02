import numpy as np
import pandas as pd

__all__=['PPDropObservations']

def PPDropObservations(observations, probability="detection probability"):
    """
    Drops rows where the probabilty of detection is less than sample drawn
    from a uniform distribution.

    Input
    -----
    observations ... pandas dataframe of observations with a column containing the probability of detection
    probability  ... name of the column containing the probability of detection

    Returns
    -------
    out ... new dataframe without observations that could not be observed
    """

    num_obs = len(observations.index)

    uniform_distr = np.random.random(num_obs)
    out = observations.drop(observations.loc[observations[probability] - uniform_distr < 0], axis=1)

    return out