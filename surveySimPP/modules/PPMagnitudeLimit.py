#!/usr/bin/python

def PPMagnitudeLimit(observations, mag_limit):
    """
    PPMagnitudeLimit.py

    Author: Steph Merritt (sort of)

    Filter that simply performs a straight magnitude cut based on a limit.

    Inputs:
    --------
    observations: Pandas dataframe of simulation data merged with pointing data. Must have
    "observedTrailedSourceMag" column.
    mag_limit: Float limit for magnitude cut.

    Returns:
    ---------
    observations: Pandas dataframe as input but with entries fainter than the limit removed.

    """

    observations = observations[observations['observedTrailedSourceMag'] < mag_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
