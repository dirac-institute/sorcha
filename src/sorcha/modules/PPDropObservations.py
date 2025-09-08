from sorcha.utilities.sorchaModuleRNG import PerModuleRNG


def PPDropObservations(observations, module_rngs, probability="detection probability"):
    """
    Drops rows where the probabilty of detection is less than sample drawn
    from a uniform distribution. Used by PPFadingFunctionFilter.

    Parameters
    -----------
    observations : Pandas dataframe
        Dataframe of observations with a column containing the probability of detection.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    probability : string, default="detection probability"
        Name of column containing detection probability.

    Returns
    ----------
    out : Pandas dataframe
        New dataframe of 'observations' modified to remove observations that could not be observed.

    """
    # Set the module specific seed as an offset from the base seed.
    rng = module_rngs.getModuleRNG(__name__)

    num_obs = len(observations.index)

    uniform_distr = rng.random(num_obs)
    out = observations[observations[probability] >= uniform_distr]

    return out
