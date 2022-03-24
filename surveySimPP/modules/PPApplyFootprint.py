#!/usr/bin/python

from . import PPFootprintFilter
import logging


def PPApplyFootprint(observations, configs):

    """
    PPApplyFootprint.py

 
    """

    pplogger = logging.getLogger(__name__)
    
    if (configs['cameraModel'] == "circle"):
        pplogger.info('Applying detection efficiency threshold...')
        observations=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(observations,configs['SSPDetectionEfficiency'])

    elif (configs['cameraModel'] == "footprint"):
        pplogger.info('Applying sensor footprint filter...')
        footprintf = PPFootprintFilter.Footprint(configs['footprintPath'])
        onSensor, detectorIDs = footprintf.applyFootprint(observations)

        observations=observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

        observations = observations.sort_index()

    return observations
        
        