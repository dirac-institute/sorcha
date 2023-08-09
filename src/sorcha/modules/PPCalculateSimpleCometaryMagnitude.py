from sorcha.activity.activity_registration import CA_METHODS
import pandas as pd
from typing import List


def PPCalculateSimpleCometaryMagnitude(
    padain: pd.DataFrame,
    observing_filters: List[str],
    rho: List[float],
    delta: List[float],
    alpha: List[float],
    activity_choice: str = None,
) -> pd.DataFrame:
    """This task calculates the brightness of the comet at a given pointing
    using the model specified by `activity_choice`

    The brightness is calculated first in the main filter, and the colour offset is
    applied afterwards.

    Parameters
    ----------
    padain : pd.DataFrame
        The input ``observations`` dataframe
    observing_filters : List[str]
        The photometric filters the observation is taken in (the filter
        requested that the coma magnitude be calculated for)
    rho : List[float]
        Heliocentric distance [units au]
    delta : List[float]
        Distance to Earth [units au]
    alpha : List[float]
        Phase angle [units degrees]
    activity_choice : str, optional
        The activity model to use, by default None

    Returns
    -------
    pd.DataFrame
            The ``observations`` dataframe with updated brightness values.
    """

    if activity_choice and CA_METHODS.get(activity_choice, False):
        ca_model = CA_METHODS.get(activity_choice)()
        return ca_model.compute(padain, observing_filters, rho, delta, alpha)
    else:
        return padain
