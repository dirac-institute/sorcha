import logging
import numpy as np

from sorcha.modules.PPApplyFOVFilter import PPCircleFootprint, PPSimpleSensorArea


def DESApplyFOVFilter(observations, sconfigs, module_rngs, footprint=None, verbose=False):
    """
    Wrapper function for DESFootprintFilter and PPFilterDetectionEfficiency that checks to see
    whether a camera footprint filter should be applied or if a simple fraction of the
    circular footprint should be used, then applies the required filter where rows are
     are removed from the inputted pandas dataframevfor moving objects that land outside of
     their associated observation's footprint.


    Parameters
    -----------
    observations: Pandas dataframe
    dataframe of observations.

    sconfigs: dataclass
        Dataclass of configuration file arguments.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    footprint: Footprint
        A Footprint class object that represents the boundaries of the detector(s).
        Default: None.

    verbose: boolean
        Controls whether logging in verbose mode is on or off.
        Default: False

    Returns
    -----------
    observations :  Pandas dataframe
        dataframe of observations updated after field-of-view filters have been applied.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if sconfigs.fov.camera_model == "footprint":
        verboselog("Applying sensor footprint filter...")

        onSensor = footprint.applyDESFootprint(observations)

        observations = observations.iloc[onSensor].copy()

        observations = observations.sort_index()

    if sconfigs.fov.camera_model == "circle":
        verboselog("FOV is circular...")
        if sconfigs.fov.circle_radius:
            verboselog("Circle radius is set. Applying circular footprint filter...")
            observations = PPCircleFootprint(observations, sconfigs.fov.circle_radius)
        if sconfigs.fov.fill_factor:
            verboselog("Fill factor is set. Removing random observations to mimic chip gaps.")
            observations = PPSimpleSensorArea(observations, module_rngs, sconfigs.fov.fill_factor)

    return observations
