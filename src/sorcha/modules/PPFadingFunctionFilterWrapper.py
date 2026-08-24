from sorcha.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from sorcha.modules.desFadingFunctionFilter import desFadingFunctionFilter

import logging
import sys


def FadingFunctionFilter(
    observations=None,
    fillfactor=None,
    width=None,
    transient_efficiency=None,
    fading_function_type=None,
    module_rngs=None,
    verbose=False,
):
    """
    Wrapper function for PPFadingFunctionFilter and desFadingFunctionFilter.
    This checks whether to use the Rubin_sim or DES fading filter.


    Parameters
    -----------
    observations : Pandas dataframe
        Dataframe of observations with a column containing the probability of detection.

    fillfactor : float
        Rubin_sim fraction of camera field-of-view covered by detectors

    transient_efficiency: float
        DES overall transient efficiency for moving object detection


    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    surveyname : string
          "Name of survey being simulated"

    verbose : boolean, default=False
        Verbose logging flag.

    Returns
    ----------
    observations_drop : Pandas dataframe)
        Modified 'observations' dataframe without observations that could not be observed.
    """
    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if fading_function_type == "general":
        observations = PPFadingFunctionFilter(
            observations,
            fillfactor,
            width,
            module_rngs,
            verbose=verbose,
        )
    elif fading_function_type == "per_obs":
        observations = desFadingFunctionFilter(
            observations,
            transient_efficiency,
            module_rngs,
            verbose=verbose,
        )
    else:
        pplogger.error(
            f"ERROR: fading function type {fading_function_type} does not have a function for Fading functin filter."
        )
        sys.exit(
            f"ERROR: fading function type {fading_function_type} does not have a function for Fading functin filter."
        )
    return observations
