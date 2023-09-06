import logging

from .PPModuleRNG import PerModuleRNG
from .PPDropObservations import PPDropObservations
from .PPDetectionProbability import PPDetectionProbability


def PPFadingFunctionFilter(observations, fillfactor, width, module_rngs, verbose=False):
    """
    Wrapper function for PPDetectionProbability and PPDropObservations.

    Calculates detection probability based on a fading function, then drops rows where the
    probabilty of detection is less than sample drawn from a uniform distribution.

    Parameters:
    -----------
    observations (Pandas dataframe): dataframe of observations with a column containing the probability of detection.

    fillFactor (float): fraction of FOV covered by the camera sensor.

    module_rngs (PerModuleRNG): A collection of random number generators (per module).

    Returns:
    ----------
    observations_drop (Pandas dataframe): new dataframe without observations that could not be observed.

    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    verboselog("Calculating probabilities of detections...")
    observations["detection_probability"] = PPDetectionProbability(
        observations, fillFactor=fillfactor, w=width
    )

    verboselog(
        "Number of rows BEFORE applying detection probability threshold: " + str(len(observations.index))
    )

    verboselog("Dropping observations below detection threshold...")
    observations = PPDropObservations(observations, module_rngs, "detection_probability")
    observations_drop = observations.drop("detection_probability", axis=1)
    observations_drop.reset_index(drop=True, inplace=True)

    verboselog(
        "Number of rows AFTER applying detection probability threshold: " + str(len(observations_drop.index))
    )

    return observations_drop
