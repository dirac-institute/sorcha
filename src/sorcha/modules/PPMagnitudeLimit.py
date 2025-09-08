def PPMagnitudeLimit(observations, mag_limit, colname="trailedSourceMag"):
    """
    Filter that performs a straight cut on apparent PSF magnitude
    based on a defined threshold.

    Parameters
    -----------
    observations : pandas dataframe
        Dataframe of observations. Must have "observedPSFMag" column.

    mag_limit : float
        Limit for apparent magnitude cut.

    colname : string, default="TrailedSourceMag"
        Column thats used to apply the magnitude cut.

    Returns
    -----------
    observations : pandas dataframe
        "observations" dataframe modified with apparent PSF mag greater than
        or equal to the limit removed.

    """

    observations = observations[observations[colname] < mag_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
