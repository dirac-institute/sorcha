import logging
import numpy as np
from astropy.coordinates import SkyCoord

from sorcha.utilities.sorchaModuleRNG import PerModuleRNG


def PPApplyFOVFilter(observations, sconfigs, module_rngs, footprint=None, verbose=False):
    """
    Wrapper function for PPFootprintFilter and PPFilterDetectionEfficiency that checks to see
    whether a camera footprint filter should be applied or if a simple fraction of the
    circular footprint should be used, then applies the required filter where rows are
     are removed from the inputted pandas dataframevfor moving objects that land outside of
     their associated observation's footprint.

    Adds the following columns to the observations dataframe:

    - detectorId (if full camera footprint is used)

    Parameters
    -----------
    observations: Pandas dataframe
    dataframe of observations.

    sconfigs: dataclass
        Dataclass of configuration file arguments.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    footprint: Footprint, default=None
        A Footprint class object that represents the boundaries of the detector(s).

    verbose: boolean, default=False
        Controls whether logging in verbose mode is on or off.

    Returns
    -----------
    observations :  Pandas dataframe
        dataframe of observations updated after field-of-view filters have been applied.
    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if sconfigs.fov.camera_model == "footprint":
        verboselog("Applying sensor footprint filter...")
        onSensor, detectorIDs = footprint.applyFootprint(
            observations, edge_thresh=sconfigs.fov.footprint_edge_threshold
        )

        observations = observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

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


def PPGetSeparation(obj_RA, obj_Dec, cen_RA, cen_Dec):
    """
    Function to calculate the distance of an object from the field centre.

    Parameters
    -----------
    obj_RA : float
        RA of object in decimal degrees.

    obj_Dec: float
        Dec of object in decimal degrees.

    cen_RA : float
        RA of field centre in decimal degrees.

    cen_Dec : float
        Dec of field centre in decimal degrees.

    Returns
    -----------
    sep_degree : float
        The separation of the object from the centre of the field, in decimal
        degrees.

    """

    obj_coord = SkyCoord(ra=obj_RA, dec=obj_Dec, unit="deg")
    cen_coord = SkyCoord(ra=cen_RA, dec=cen_Dec, unit="deg")

    sep = obj_coord.separation(cen_coord)

    return sep.degree


def PPCircleFootprint(observations, circle_radius):
    """
    Simple function which removes objects which lay outside of a circle
    of given radius centred on the field centre.

    Parameters
    -----------
    observations : Pandas dataframe
        dataframe of observations.

    circle_radius : float
        radius of circle footprint in degrees.

    Returns
    ----------
    new_observations : Pandas dataframe
        dataframe of observations with all lying beyond the circle radius dropped.

    """

    data_coords = SkyCoord(ra=observations["RA_deg"].values, dec=observations["Dec_deg"].values, unit="deg")

    field_coords = SkyCoord(
        ra=observations["fieldRA_deg"].values, dec=observations["fieldDec_deg"].values, unit="deg"
    )

    separations = data_coords.separation(field_coords).degree
    observations["object_separation"] = separations

    new_observations = observations[observations["object_separation"] < circle_radius]

    new_observations.reset_index(drop=True, inplace=True)
    new_observations = new_observations.drop("object_separation", axis=1)

    return new_observations


def PPSimpleSensorArea(ephemsdf, module_rngs, fillfactor=0.9):
    """
    Randomly removes a number of observations proportional to the
    fraction of the field not covered by the detector.

    Parameters
    -----------
    ephemsdf : Pandas dataframe
        Dataframe containing observations.

    module_rngs : PerModuleRNG
        A collection of random number generators (per module).

    fillfactor : float, default=0.9
        fraction of FOV covered by the sensor.

    Returns
    ----------
    ephemsOut : Pandas dataframe
        Dataframe of observations with 1- fillfactor fraction of objects
        removed per on-sky observation pointing.

    """
    # Set the module specific seed as an offset from the base seed.
    rng = module_rngs.getModuleRNG(__name__)

    n = len(ephemsdf)

    randomNum = rng.random(n)
    fillArray = np.zeros(n) + fillfactor
    dropObs = np.where(randomNum > fillArray)[0]

    ephemsOut = ephemsdf.drop(dropObs)
    ephemsOut = ephemsOut.reset_index(drop=True)

    return ephemsOut
