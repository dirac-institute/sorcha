#!/usr/bin/python

from . import PPFootprintFilter
import logging
import numpy as np
from astropy.coordinates import SkyCoord


def PPApplyFOVFilter(observations, configs, rng, verbose=False):
    """
    PPApplyFootprint.py

    Author: Steph Merritt

    Wrapper function for PPFootprintFilter and PPFilterDetectionEfficiency. Checks to see
    whether a camera footprint filter should be applied or if a simple fraction of the
    circular footprint should be used, then applies the required filter.

    Input:
    --------
    observations: Pandas dataframe of simulation data joined with pointing info.
    configs: dictionary of config variables


    """

    pplogger = logging.getLogger(__name__)
    verboselog = pplogger.info if verbose else lambda *a, **k: None

    if configs['cameraModel'] == 'circle' and not configs['fadingFunctionOn']:
        verboselog('FOV is circular and fading function is off. Removing random observations.')

        observations = PPSimpleSensorArea(observations, rng, configs['fillfactor'])

    elif configs['cameraModel'] == 'footprint':
        verboselog('Applying sensor footprint filter...')
        footprintf = PPFootprintFilter.Footprint(configs['footprintPath'])
        onSensor, detectorIDs = footprintf.applyFootprint(observations)

        observations = observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

        observations = observations.sort_index()

    elif configs['cameraModel'] == 'circle' and configs['fadingFunctionOn']:
        verboselog('Applying circular footprint filter...')
        observations = PPCircleFootprint(observations, configs['circleRadius'])

    return observations


def PPGetSeparation(obj_RA, obj_Dec, cen_RA, cen_Dec):
    """Function to calculate the distance of
    an object from the field centre if given RA and Dec for them both.

    Parameters:
    -----------
    obj_RA: float of RA of object in decimal degrees
    obj_Dec: float of Dec of object in decimal degrees
    cen_RA: float of RA of field centre in decimal degrees
    cen_Dec: float of Dec of field centre in decimal degrees

    Returns:
    ----------
    sep_degree: The separation of the object from the centre of the field, in decimal
    degrees, as a float.

    """

    obj_coord = SkyCoord(ra=obj_RA, dec=obj_Dec, unit="deg")
    cen_coord = SkyCoord(ra=cen_RA, dec=cen_Dec, unit="deg")

    sep = obj_coord.separation(cen_coord)

    return sep.degree


def PPCircleFootprint(observations, circle_radius):
    """Simple function which removes objects which lay outside of a circle
    of given radius centred on the field centre.

    Parameters:
    -----------
    observations: Pandas dataframe of observations
    circle_radius: Radius of circle footprint in degrees (int)

    Returns:
    ----------
    Pandas dataframe of observations with all lying beyond the circle radius dropped.

    """

    # note the slightly convoluted syntax in this function seems to be necessary
    # to avoid the dreaded chained indexing Pandas warnings.

    object_separation = observations.apply(lambda x: PPGetSeparation(x["AstRA(deg)"],
                                                                     x["AstDec(deg)"],
                                                                     x.fieldRA,
                                                                     x.fieldDec),
                                           axis=1)

    observations['object_separation'] = object_separation
    new_observations = observations[observations['object_separation'] < circle_radius]

    new_observations.reset_index(drop=True, inplace=True)
    new_observations = new_observations.drop('object_separation', axis=1)

    return new_observations


def PPSimpleSensorArea(ephemsdf, rng, fillfactor=0.9):
    '''Randomly removes a number of observations proportional to the
    fraction of the field not covered by the detector.

    Parameters:
    ----------
    ephemsdf   ... pandas dataFrame containing observations
    fillfactor ... fraction of FOV covered by the sensor

    Returns
    -------
    ephemsOut  ... pandas dataFrame

    '''
    n = len(ephemsdf)

    randomNum = rng.random(n)
    fillArray = np.zeros(n) + fillfactor
    dropObs = np.where(randomNum > fillArray)[0]

    ephemsOut = ephemsdf.drop(dropObs)
    ephemsOut = ephemsOut.reset_index(drop=True)

    return ephemsOut
