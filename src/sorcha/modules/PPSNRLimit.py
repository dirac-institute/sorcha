def PPSNRLimit(observations, sigma_limit=2.0):
    """
    Filter that performs a straight SNR cut based on a limit, removing
    observations that are less than a SNR limit

    Parameters
    -----------
    observations : pandas dataframe
        Dataframe of observations. Must have "SNR" column.

    sigma_limit : float, optional.
        Limit for SNR cut.

    Returns
    -----------
    observations : pandas dataframe
        "observations" dataframed modified with entries with SNR < the limit removed.

    """

    observations = observations[observations["SNR"] > sigma_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
