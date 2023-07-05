def PPSNRLimit(observations, sigma_limit=2.0):
    """
    Filter that performs a straight SNR cut based on a limit.

    Parameters:
    -----------
    observations (Pandas dataframe) dataframe of observations. Must have
    "SNR" column.

    sigma_limit (float): limit for SNR cut.

    Returns:
    -----------
    observations (Pandas dataframe): same as input, but with entries with SNR < the limit removed.

    """

    observations = observations[observations["SNR"] > sigma_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
