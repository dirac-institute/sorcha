import logging

from ..utilities.sorchaModuleRNG import PerModuleRNG
from .PPDropObservations import PPDropObservations
from .DESDetectionProbability import DESDetectionProbability


def DESFadingFunctionFilter(
    observations,
    transient_efficiency,
    module_rngs,
    verbose=False,
):
    """
    Wrapper function for DESDetectionProbability and PPDropObservations.

    Calculates detection probability based on a fading function, then drops rows where the
    probabilty of detection is less than sample drawn from a uniform distribution.

    Parameters
    -----------
    observations : Pandas dataframe
        Dataframe of observations with a column containing the probability of detection.

    transient_efficiency: float
        overall transient efficiency for moving object detection

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    verbose : boolean, optional
        Verbose logging flag. Default = False

    Returns
    ----------
    observations_drop : Pandas dataframe)
        Modified 'observations' dataframe without observations that could not be observed.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    verboselog("Calculating probabilities of detections...")
    observations["detection_probability"] = DESDetectionProbability(observations, transient_efficiency)

    verboselog("Dropping observations below detection threshold...")
    observations = PPDropObservations(observations, module_rngs, "detection_probability")
    observations_drop = observations.drop("detection_probability", axis=1)
    observations_drop.reset_index(drop=True, inplace=True)

    return observations_drop
