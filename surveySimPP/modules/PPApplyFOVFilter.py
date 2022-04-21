#!/usr/bin/python

from . import PPFootprintFilter
import logging

def PPApplyFOVFilter(observations, configs):
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

    if configs['cameraModel'] == 'circle':
        pplogger.info('FOV is circular. Skipping...')

    elif configs['cameraModel'] == 'footprint':
        pplogger.info('Applying sensor footprint filter...')
        footprintf = PPFootprintFilter.Footprint(configs['footprintPath'])
        onSensor, detectorIDs = footprintf.applyFootprint(observations)

        observations = observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

        observations = observations.sort_index()

    return observations
