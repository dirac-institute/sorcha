import logging
from .PPDetectionProbability import PPDetectionProbability

from sorcha.modules.PPModuleRNG import getModuleRNG


def PPFadingFunctionFilter(observations, fillfactor, width, base_seed, verbose=False):
    """
    Calculates detection probability based on a fading function, then drops rows where the
    probabilty of detection is less than sample drawn from a uniform distribution.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations with a column containing the probability of detection.

    fillFactor (float): fraction of FOV covered by the camera sensor.

    base_seed (int): The base seed for the random number generator.

    Returns:
    ----------
    observations_drop (Pandas dataframe): new dataframe without observations that could not be observed.

    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    # Set the module specific seed as an offset from the base seed.
    rng = getModuleRNG(base_seed, __name__)

    verboselog("Calculating probabilities of detections...")
    observations["detection_probability"] = PPDetectionProbability(
        observations, fillFactor=fillfactor, w=width
    )

    verboselog(
        "Number of rows BEFORE applying detection probability threshold: " + str(len(observations.index))
    )

    verboselog("Dropping observations below detection threshold...")
    uniform_distr = rng.random(len(observations.index))
    observations = observations[observations["detection_probability"] >= uniform_distr]

    observations_drop = observations.drop("detection_probability", axis=1)
    observations_drop.reset_index(drop=True, inplace=True)

    verboselog(
        "Number of rows AFTER applying detection probability threshold: " + str(len(observations_drop.index))
    )

    return observations_drop
