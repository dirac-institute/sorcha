def PPDropObservations(observations, rng, probability="detection probability"):
    """
    Drops rows where the probabilty of detection is less than sample drawn
    from a uniform distribution. Used by PPFadingFunctionFilter.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations with a column containing the probability of detection.

    rng (numpy Generator): numpy random number Generator object.

    probability (string): name of column containing detection probability.

    Returns:
    ----------
    out (Pandas dataframe): new dataframe without observations that could not be observed.

    """

    num_obs = len(observations.index)

    uniform_distr = rng.random(num_obs)
    out = observations[observations[probability] >= uniform_distr]

    return out
