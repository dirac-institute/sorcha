#!/usr/bin/python

from . import PPFootprintFilter
import logging
import numpy as np


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

    else:
        verboselog('FOV is circular and fading function is on. Skipping FOV filter.')

    return observations


def PPSimpleSensorArea(ephemsdf, rng, fillfactor=0.9):

    '''Randomly removes a number of observations proportional to the
    fraction of the field not covered by the detector.

    Parameters
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
