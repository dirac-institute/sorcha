from sorcha.modules.PPFadingFunctionFilter import PPFadingFunctionFilter
from sorcha.modules.desFadingFunctionFilter import desFadingFunctionFilter
from sorcha.configs.fovConfigs import fovConfigs
from sorcha.configs.fadingfunctionConfigs import fadingfunctionConfigs
import logging
import sys


def FadingFunctionFilter(
    observations=None,
    fadingfunc_configs: fadingfunctionConfigs = None,
    fov_configs: fovConfigs = None,
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

    fadingfunc_configs: fadingfunctionConfigs
        Fading Function Dataclass of fading function configuration file arguments.

    fov_configs: fovConfigs
        FOV Dataclass of fov configuration file arguments.

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
    fading_function_type = fadingfunc_configs.fading_function_type

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if fov_configs.camera_model == "visits_footprint":
        limiting_magnitude_name = "limMag_perChip"
    else:
        limiting_magnitude_name = "fiveSigmaDepth_mag"

    if fading_function_type == "general":
        observations = PPFadingFunctionFilter(
            observations,
            fillfactor=fadingfunc_configs.fading_function_peak_efficiency,
            width=fadingfunc_configs.fading_function_width,
            module_rngs=module_rngs,
            verbose=verbose,
            limiting_magnitude_name=limiting_magnitude_name,
        )
    elif fading_function_type == "des_per_obs":
        observations = desFadingFunctionFilter(
            observations,
            transient_efficiency=fadingfunc_configs.des_transient_efficency,
            module_rngs=module_rngs,
            verbose=verbose,
            limiting_magnitude_name=limiting_magnitude_name,
        )
    else:
        pplogger.error(
            f"ERROR: fading function type {fading_function_type} does not have a function for Fading functin filter."
        )
        sys.exit(
            f"ERROR: fading function type {fading_function_type} does not have a function for Fading functin filter."
        )
    return observations
