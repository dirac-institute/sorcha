#!/usr/bin/python

from . import PPFootprintFilter
import logging


def PPApplyFOVFilter(observations, camera_model, footprint_path):

    """
    PPApplyFootprint.py
    
    Author: Steph Merritt
    
    Wrapper function for PPFootprintFilter and PPFilterDetectionEfficiency. Checks to see 
    whether a camera footprint filter should be applied or if a simple fraction of the 
    circular footprint should be used, then applies the required filter.
    
    Input:
    --------
    observations: Pandas dataframe of simulation data joined with pointing info.
    configs: 

 
    """

    pplogger = logging.getLogger(__name__)
    
    if camera_model == "circle":
        pplogger.info('Applying detection efficiency threshold...')
        observations=PPFilterDetectionEfficiencyThreshold.PPFilterDetectionEfficiencyThreshold(observations,configs['SSPDetectionEfficiency'])

    elif camera_model == "footprint":
        pplogger.info('Applying sensor footprint filter...')
        footprintf = PPFootprintFilter.Footprint(footprint_path)
        onSensor, detectorIDs = footprintf.applyFootprint(observations)

        observations=observations.iloc[onSensor].copy()
        observations["detectorID"] = detectorIDs

        observations = observations.sort_index()

    return observations
        
        