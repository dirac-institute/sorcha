import logging
from .PPDropObservations import PPDropObservations
from .PPDetectionProbability import PPDetectionProbability


def PPFilterFadingFunction(observations, fillfactor, rng):
    """Wrapper function for PPDetectionProbability and PPDropObservations.

    Calculates detection probability based on a fading function, then drops rows where the
    probabilty of detection is less than sample drawn from a uniform distribution.

    Input
    -----
    observations ... pandas dataframe of observations with a column containing the probability of detection
    fillfactor  ... float of fill factor for camera footprint
    rng          ... Numpy random number generator.

    Returns
    -------
    observations ... new dataframe without observations that could not be observed

    """

    pplogger = logging.getLogger(__name__)

    pplogger.info('Calculating probabilities of detections...')
    observations["detection_probability"] = PPDetectionProbability(observations, fillFactor=fillfactor)

    pplogger.info('Number of rows BEFORE applying detection probability threshold: ' + str(len(observations.index)))

    pplogger.info('Dropping observations below detection threshold...')
    observations = PPDropObservations(observations, rng, "detection_probability")
    observations_drop = observations.drop("detection_probability", axis=1)
    observations_drop.reset_index(drop=True, inplace=True)

    pplogger.info('Number of rows AFTER applying detection probability threshold: ' + str(len(observations_drop.index)))

    return observations_drop
