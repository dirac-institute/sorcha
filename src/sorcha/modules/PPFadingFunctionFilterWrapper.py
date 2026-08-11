from sorcha.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from sorcha.modules.desFadingFunctionFilter import desFadingFunctionFilter

import logging
import sys


def FadingFunctionFilter(
    observations=None,
    fillfactor=None,
    width=None,
    module_rngs=None,
    transient_efficiency=None,
    survey_name=None,
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

    if survey_name in ["rubin_sim", "RUBIN_SIM"]:
        observations = PPFadingFunctionFilter(
            observations,
            fillfactor,
            width,
            module_rngs,
            verbose=verbose,
        )
    elif survey_name in ["DES", "des"]:
        observations = desFadingFunctionFilter(
            observations,
            transient_efficiency,
            module_rngs,
            verbose=verbose,
        )
    else:
        pplogger.error(f"ERROR: Survey {survey_name} does not have a function for Fading functin filter.")
        sys.exit(f"ERROR: Survey {survey_name} does not have a function for Fading functin filter.")
    return observations
