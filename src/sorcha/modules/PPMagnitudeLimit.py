def PPMagnitudeLimit(observations, mag_limit):
    """
    Filter that performs a straight magnitude cut based on a defined limit.

    Parameters:
    -----------
    observations (Pandas dataframe) dataframe of observations. Must have
    "observedTrailedSourceMag" column.

    mag_limit (float): limit for magnitude cut.

    Returns:
    -----------
    observations (Pandas dataframe): same as input, but with entries fainter than the limit removed.

    """

    observations = observations[observations["observedPSFMag"] < mag_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
