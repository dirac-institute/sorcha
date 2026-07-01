def PPSNRLimit(observations, sigma_limit=2.0, snr_name = "SNRPSFMag"):
    """
    Filter that performs a straight SNR cut based on a limit, removing
    observations that are less than a SNR limit

    Parameters
    -----------
    observations : pandas dataframe
        Dataframe of observations. Must have equivalent SNR column (see snr_name).

    sigma_limit : float, default=2.0
        Limit for SNR cut.
    
    snr_name : string, default="SNRPSFMag"
        name of the SNR column


    Returns
    -----------
    observations : pandas dataframe
        "observations" dataframed modified with entries with SNR < the limit removed.

    """
    
    # By default we filter on the SNR of the PSFMag as this is the measured SNR
    #the transient detection pipelines measure for each source

    observations = observations[observations[snr_name] > sigma_limit]
    observations.reset_index(drop=True, inplace=True)

    return observations
