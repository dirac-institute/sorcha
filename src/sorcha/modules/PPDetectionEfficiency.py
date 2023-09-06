import sys
import logging

from sorcha.modules.PPModuleRNG import PerModuleRNG


def PPDetectionEfficiency(padain, threshold, module_rngs):
    """
    Applies a random cut to the observations dataframe based on an efficiency
    threshold: if the threshold is 0.95, for example, 5% of observations will be
    randomly dropped. Used by PPLinkingFilter.

    Parameters:
    -----------
    padain (Pandas dataframe): dataframe of observations.

    threshold (float): Fraction between 0 and 1 of detections retained in the dataframe.

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    Returns:
    ----------
    padain_drop: dataframe of observations with a fraction equal to 1-threshold
    randomly dropped.

    """

    pplogger = logging.getLogger(__name__)

    # Set the module specific seed as an offset from the base seed.
    rng = module_rngs.getModuleRNG(__name__)

    padain.reset_index(drop=True, inplace=True)

    if threshold > 1.0 or threshold < 0.0:
        pplogger.error("ERROR: PPDetectionEfficiency: threshold out of bounds.")
        sys.exit("ERROR: PPDetectionEfficiency: threshold out of bounds.")

    num_obs = len(padain.index)

    uniform_distr = rng.random(num_obs)

    return padain[uniform_distr <= threshold]
